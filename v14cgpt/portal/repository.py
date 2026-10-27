"""Repositori data portal KREASI.

Frontend lama mengirim satu snapshot state JavaScript. Untuk mempertahankan renderer,
state domain UI tetap disimpan sebagai agregat JSON pada `AppState`, sedangkan kredensial
akun dan metadata berkas disimpan melalui model relasional Django.

DESAIN ENKAPSULASI: view memakai antarmuka publik `get_state()`, `get_state_for()`, dan
`save_state()`. Detail pemilihan record, validasi struktur, pemfilteran akses, dan penggabungan
perubahan disimpan di metode `__...`. Nama ganda memicu name-mangling Python, tetapi bukan
mekanisme keamanan; kontrol akses sebenarnya dilakukan oleh logika validasi metode ini.
"""
from copy import deepcopy
import json

from django.core.exceptions import ValidationError
from django.db import transaction

from .models import AppState, UploadedDocument
from .services import AccountServiceFactory

DEFAULT_CATEGORIES = [
    "Informatika untuk Masyarakat", "Proyek Mata Kuliah", "Kompetisi", "Magang",
    "Wirausaha", "Organisasi & Kepemimpinan", "Minat & Bakat",
    "Internasionalisasi & Summit", "Rekognisi", "Penelitian & Hibah",
]
DEFAULT_COURSES = [
    "Rekayasa Perangkat Lunak", "Jaringan Komputer", "Basis Data",
    "Kecerdasan Buatan", "Jaringan & Keamanan Siber", "Sistem Informasi",
    "Kerja Praktik / Magang", "Skripsi / Tugas Akhir", "KKN / Informatika untuk Masyarakat",
]


def empty_portal_state():
    """Buat bentuk state awal dengan struktur yang diharapkan frontend.

    Ini fungsi pembentuk data, bukan class/model OOP. Daftar domain dimulai kosong agar
    tidak ada akun/proyek/prestasi contoh; nilai master dipertahankan untuk konfigurasi awal.
    """
    return {
        "users": [], "announcements": [], "talentPool": [], "projects": [],
        "achievements": [], "portfolios": [], "invitations": [], "notifications": [],
        "skpiFinalizations": [], "studentProfiles": {},
        "studentProfile": {"phone": "", "bio": "", "skills": []},
        "masterData": {
            "projectCategories": deepcopy(DEFAULT_CATEGORIES), "courses": deepcopy(DEFAULT_COURSES),
            "classes": ["A", "B", "C"], "courseOfferings": [],
            "achievementCategories": [], "mexsThreshold": 1000,
        },
    }


class KreasiStateRepository:
    """Mengelola baca, filter, validasi, dan simpan state KREASI.

    `STATE_KEY` mengidentifikasi record agregat tunggal, sedangkan `MAX_STATE_BYTES`
    membatasi besar payload. Kelas ini menjadi batas data backend agar view tidak mengubah
    `AppState` secara langsung dan agar pembatasan peran diterapkan sebelum penyimpanan.
    """
    STATE_KEY = "main"
    MAX_STATE_BYTES = 8 * 1024 * 1024

    def __state_record(self):
        """Metode privat (`__...`) mengenkapsulasi pemilihan record singleton."""
        record = AppState.objects.filter(key=self.STATE_KEY).first()
        return record

    def __validate_payload(self, payload):
        """Validasi internal sebelum JSON disimpan ke basis data."""
        if not isinstance(payload, dict):
            raise ValueError("Format data sistem tidak valid.")
        # Frontend mengirim snapshot lengkap. Menolak array/objek utama yang hilang atau
        # bertipe salah mencegah payload parsial menghapus data tanpa sengaja.
        expected = {
            "users": list, "announcements": list, "talentPool": list, "projects": list,
            "achievements": list, "portfolios": list, "invitations": list, "notifications": list,
            "skpiFinalizations": list, "studentProfiles": dict, "studentProfile": dict, "masterData": dict,
        }
        for field, expected_type in expected.items():
            if field not in payload or not isinstance(payload[field], expected_type):
                raise ValueError(f"Struktur data '{field}' tidak valid atau tidak lengkap.")
        try:
            encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise ValueError("Data sistem tidak dapat diserialisasi.") from exc
        if len(encoded) > self.MAX_STATE_BYTES:
            raise ValueError("Data sistem terlalu besar untuk disimpan sekaligus.")

    def get_state(self):
        """Antarmuka baca internal-server untuk memperoleh salinan snapshot penuh."""
        record = self.__state_record()
        return deepcopy(record.data) if record else empty_portal_state()

    def get_state_for(self, actor):
        """Kembalikan subset state yang boleh dilihat pengguna yang sedang login.

        Admin mendapat state yang sudah dibersihkan dari field password; mahasiswa dan
        dosen memperoleh kumpulan user, proyek, notifikasi, dan profil sesuai role/identitas.
        Hasilnya adalah salinan data, sehingga filter tidak mengubah snapshot asli di DB.
        """
        state = self.get_state()
        if actor.role == "admin":
            self.__remove_password_fields(state)
            return state

        role = actor.role
        identity = str(actor.identifier or "")
        profile = actor.profile_data if isinstance(actor.profile_data, dict) else {}
        identity_fields = {
            "id", "username", "role", "name", "nim", "nip", "prodi", "angkatan", "kelas",
            "active", "avatar", "mataKuliahDiambil", "mataKuliahDiampu", "semester", "poin",
            "prestasi", "jabatan", "skills", "mexs", "portfolioCount", "achievementCount",
        }
        state["users"] = [
            {key: deepcopy(value) for key, value in row.items() if key in identity_fields}
            for row in state.get("users", [])
            if isinstance(row, dict) and row.get("role") in {"student", "lecturer"}
            and row.get("active", True)
        ]
        state["projects"] = self.__visible_projects(state, actor, profile)
        state["notifications"] = [
            item for item in state.get("notifications", [])
            if isinstance(item, dict)
            and (not item.get("recipientRole") or item.get("recipientRole") == role)
            and (not item.get("recipientNim") or str(item.get("recipientNim")) == identity)
            and (not item.get("recipientNip") or str(item.get("recipientNip")) == identity)
        ]

        if role == "student":
            state["achievements"] = [row for row in state.get("achievements", [])
                                     if str(row.get("nim", "")) == identity]
            state["portfolios"] = [row for row in state.get("portfolios", [])
                                   if str(row.get("nim", "")) == identity]
            state["talentPool"] = [row for row in state.get("talentPool", [])
                                   if str(row.get("nim", "")) == identity]
            profiles = state.get("studentProfiles", {})
            own_profile = profiles.get(identity, {}) if isinstance(profiles, dict) else {}
            state["studentProfiles"] = {identity: deepcopy(own_profile)} if own_profile else {}
            state["studentProfile"] = deepcopy(own_profile) if isinstance(own_profile, dict) else {}
            state["invitations"] = [row for row in state.get("invitations", [])
                                    if str(row.get("nim", "")) == identity]
            state["skpiFinalizations"] = [row for row in state.get("skpiFinalizations", [])
                                          if str(row.get("nim", "")) == identity]
        elif role == "lecturer":
            # Talent pool, portofolio dan profil publik diperlukan pada katalog talenta.
            # Nomor telepon mahasiswa lain tidak ikut diekspos ke akun dosen.
            profiles = state.get("studentProfiles", {})
            state["studentProfiles"] = {
                str(nim): {key: deepcopy(value) for key, value in row.items() if key in {"bio", "skills"}}
                for nim, row in profiles.items() if isinstance(row, dict)
            } if isinstance(profiles, dict) else {}
            state["studentProfile"] = {}
            state["skpiFinalizations"] = []
            state["invitations"] = [row for row in state.get("invitations", [])
                                    if str(row.get("sender", "")) == str(actor.full_name or "")
                                    or str(row.get("senderNip", row.get("lecturerNip", ""))) == identity]
        self.__remove_password_fields(state)
        return state

    def __remove_password_fields(self, state):
        """Helper privat yang membuang password legacy dari data profil browser.

        Kredensial autentikasi tetap disimpan/hash oleh `PortalUser`; field password pada
        snapshot UI lama tidak boleh dikirim kembali dalam respons JSON.
        """
        for row in state.get("users", []) if isinstance(state.get("users"), list) else []:
            if isinstance(row, dict):
                row.pop("password", None)

    def __visible_projects(self, state, actor, profile):
        """Helper privat untuk menerapkan aturan visibilitas proyek menurut role.

        Proyek umum tersedia sesuai kategori master; kategori Proyek Mata Kuliah dan
        Informatika untuk Masyarakat memiliki aturan keterkaitan dengan akun/proyek/kelas.
        """
        role = actor.role
        identity = str(actor.identifier or "")
        master = state.get("masterData", {}) if isinstance(state.get("masterData"), dict) else {}
        configured = set(master.get("projectCategories", DEFAULT_CATEGORIES))
        private_categories = {"Proyek Mata Kuliah", "Informatika untuk Masyarakat"}
        public_categories = configured - private_categories
        courses = profile.get("mataKuliahDiambil")
        projects = state.get("projects", [])
        visible = []
        for project in projects:
            if not isinstance(project, dict):
                continue
            category = project.get("category")
            if role == "lecturer":
                if (category in public_categories
                        or str(project.get("supervisorNip", "")) == identity
                        or str(project.get("creatorNip", "")) == identity
                        or str(project.get("ownerNip", "")) == identity):
                    visible.append(project)
                continue

            related = str(project.get("creatorNim", "")) == identity
            for member in project.get("members", []) if isinstance(project.get("members"), list) else []:
                related = related or (isinstance(member, dict) and str(member.get("nim", "")) == identity)
            for applicant in project.get("applicants", []) if isinstance(project.get("applicants"), list) else []:
                related = related or (isinstance(applicant, dict) and str(applicant.get("nim", "")) == identity)
            groups = project.get("groups", []) if isinstance(project.get("groups"), list) else []
            for group in groups:
                for member in group.get("members", []) if isinstance(group.get("members"), list) else []:
                    related = related or (isinstance(member, dict) and str(member.get("nim", "")) == identity)

            if related or category in public_categories:
                visible.append(project)
                continue
            if category == "Proyek Mata Kuliah" and project.get("status") == "Active" and not project.get("studentCreated"):
                cohort = str(profile.get("angkatan") or "")
                klass = str(profile.get("kelas") or "")
                project_cohort = str(project.get("angkatan") or "")
                project_classes = project.get("kelas", [])
                class_ok = not project_classes or (isinstance(project_classes, list) and klass in project_classes)
                course_ok = courses is None or not isinstance(courses, list) or project.get("course") in courses
                if (not project_cohort or project_cohort == cohort) and class_ok and course_ok:
                    visible.append(project)
        return visible

    @transaction.atomic
    def save_state(self, payload: dict, actor):
        """Validasi, terapkan batas role, lalu simpan snapshot dalam satu transaksi.

        Proses utamanya: validasi bentuk data -> salin data -> terapkan kebijakan role ->
        bila Admin mengubah daftar akun, sinkronkan tabel PortalUser -> hapus password dari
        snapshot -> simpan/increment versi AppState. Atomic mencegah simpan setengah jalan.
        """
        self.__validate_payload(payload)
        # Kunci record snapshot selama perubahan agar dua request yang bersamaan tidak
        # membaca versi lama lalu menulis bersamaan di DB yang mendukung row locking.
        # get_or_create juga menangani inisialisasi pertama ketika AppState belum ada.
        record, _created = AppState.objects.select_for_update().get_or_create(
            key=self.STATE_KEY, defaults={"data": empty_portal_state(), "version": 1}
        )
        previous = deepcopy(record.data) if isinstance(record.data, dict) else empty_portal_state()
        incoming = deepcopy(payload)
        incoming = self.__apply_role_boundaries(previous, incoming, actor)

        # Sinkronkan kredensial akun hanya ketika administrator mengirim daftar akun.
        # Data yang disimpan di JSON tidak pernah berisi kata sandi mentah.
        if actor.role == "admin" and isinstance(payload.get("users"), list):
            AccountServiceFactory.sync_records(payload["users"])

        incoming.setdefault("users", previous.get("users", []))
        incoming.setdefault("masterData", previous.get("masterData", empty_portal_state()["masterData"]))
        for field in ("users",):
            for user_row in incoming.get(field, []):
                if isinstance(user_row, dict):
                    user_row.pop("password", None)
        record.data = incoming
        record.version += 1
        record.save(update_fields=["data", "version", "updated_at"])
        return deepcopy(record.data), record.version

    def __apply_role_boundaries(self, old: dict, new: dict, actor):
        """Pusat pembatasan perubahan state sisi server.

        Metode privat ini mencegah otorisasi hanya bergantung pada tombol/menu UI:
        Admin mengelola akun/master; dosen mengelola proyek terkait; mahasiswa hanya
        mengubah data miliknya dan tidak dapat memberi persetujuan sendiri.
        """
        new.setdefault("users", old.get("users", []))
        if actor.role != "admin":
            # Akun, data master, pengumuman, dan finalisasi SKPI hanya dikelola Admin.
            for key in ("users", "masterData", "announcements", "skpiFinalizations"):
                new[key] = deepcopy(old.get(key, empty_portal_state().get(key, [])))

        if actor.role == "admin":
            # Admin tidak mengedit isi proyek dari halaman monitor. Namun, perubahan
            # identitas akun dan penghapusan akun harus diselaraskan dengan referensi proyek.
            new["projects"] = self.__admin_project_changes(
                old.get("projects", []), new.get("projects", []),
                old.get("users", []), new.get("users", []),
            )
            # Operasi Manajemen Akun memperbarui NIM/profil talenta dan menghapus baris
            # milik akun yang dihapus. Data SKPI/prestasi dan master data dikelola Admin.
            new["studentProfile"] = deepcopy(old.get("studentProfile", {}))
            return new

        if actor.role == "lecturer":
            # Dosen dapat mengelola proyek yang menjadi ruang kerjanya; profil/prestasi
            # mahasiswa, portofolio, dan finalisasi SKPI tidak diubah dari sesi dosen.
            for key in ("achievements", "portfolios", "studentProfiles", "studentProfile", "talentPool", "skpiFinalizations"):
                new[key] = deepcopy(old.get(key, empty_portal_state().get(key, [])))
            new["announcements"] = deepcopy(old.get("announcements", []))
            new["users"] = deepcopy(old.get("users", []))
            new["masterData"] = deepcopy(old.get("masterData", empty_portal_state()["masterData"]))
            new["projects"] = self.__lecturer_project_changes(old.get("projects", []), new.get("projects", []), actor.identifier)
            new["invitations"] = self.__merge_invitations(old.get("invitations", []), new.get("invitations", []), actor)
            new["notifications"] = self.__merge_notifications(old.get("notifications", []), new.get("notifications", []), actor)
            return new

        if actor.role == "student":
            nim = str(actor.identifier or "")
            new["projects"] = self.__student_project_changes(
                old.get("projects", []), new.get("projects", []), actor, old,
                old.get("invitations", []), new.get("invitations", []),
            )
            new["portfolios"] = self.__merge_owned_rows(old.get("portfolios", []), new.get("portfolios", []), "nim", nim)
            new["talentPool"] = self.__merge_owned_rows(old.get("talentPool", []), new.get("talentPool", []), "nim", nim)
            new["achievements"] = self.__student_achievement_changes(old.get("achievements", []), new.get("achievements", []), nim)
            new["studentProfiles"] = self.__merge_profile_map(old.get("studentProfiles", {}), new.get("studentProfiles", {}), nim)
            new["invitations"] = self.__merge_invitations(old.get("invitations", []), new.get("invitations", []), actor)
            new["notifications"] = self.__merge_notifications(old.get("notifications", []), new.get("notifications", []), actor)
            old_profiles = old.get("studentProfiles", {})
            new_profiles = new.get("studentProfiles", {})
            new["studentProfile"] = deepcopy(new_profiles.get(nim, old_profiles.get(nim, new.get("studentProfile", {}))) or {})
            # Pengumuman, pengguna, master data, dan finalisasi dilindungi pada blok di atas.
            return new

        return old

    def __admin_project_changes(self, old_projects, new_projects, old_users, new_users):
        """Sesuaikan referensi identitas anggota saat Admin mengubah akun; jaga isi proyek."""
        old_user_by_id = {str(row.get("id", "")): row for row in old_users if isinstance(row, dict)}
        new_user_by_id = {str(row.get("id", "")): row for row in new_users if isinstance(row, dict)}
        removed = [row for uid, row in old_user_by_id.items() if uid not in new_user_by_id]
        removed_nims = {str(row.get("nim") or row.get("username") or "") for row in removed if row.get("role") == "student"}
        removed_nips = {str(row.get("nip") or row.get("username") or "") for row in removed if row.get("role") == "lecturer"}
        removed_names = {str(row.get("name") or "") for row in removed if row.get("role") == "lecturer"}

        student_updates, lecturer_updates = [], []
        for uid, old_user in old_user_by_id.items():
            current = new_user_by_id.get(uid)
            if not current or current.get("role") != old_user.get("role"):
                continue
            if old_user.get("role") == "student":
                student_updates.append((str(old_user.get("nim") or old_user.get("username") or ""), current))
            elif old_user.get("role") == "lecturer":
                lecturer_updates.append((str(old_user.get("nip") or old_user.get("username") or ""), old_user, current))

        incoming_ids = {str(row.get("id", "")) for row in new_projects if isinstance(row, dict)}
        incoming_ids.discard("")
        output = []
        for original in old_projects:
            if not isinstance(original, dict):
                continue
            project = deepcopy(original)
            pid = str(project.get("id", ""))
            if pid not in incoming_ids:
                deleted_student_project = str(project.get("creatorNim", "")) in removed_nims
                deleted_lecturer_project = (
                    str(project.get("creatorNip", "")) in removed_nips
                    or str(project.get("ownerNip", "")) in removed_nips
                    or str(project.get("supervisorNip", "")) in removed_nips
                    or (not project.get("supervisorNip") and str(project.get("supervisor", "")) in removed_names)
                    or (not project.get("creatorNip") and str(project.get("creator", "")) in removed_names and "dosen" in str(project.get("creatorRole", "")).lower())
                )
                if deleted_student_project or deleted_lecturer_project:
                    continue

            # Perubahan identitas hanya memperbarui referensi; judul, status, nilai, dan dokumen tetap dikelola server.
            creator_nim = str(project.get("creatorNim", ""))
            for old_nim, current in student_updates:
                new_nim = str(current.get("nim") or current.get("username") or "")
                if creator_nim and creator_nim == old_nim:
                    project["creatorNim"] = new_nim
                    project["creator"] = current.get("name", project.get("creator", ""))
                    project["department"] = current.get("prodi", project.get("department", ""))
                for collection_key in ("members", "applicants"):
                    rows = project.get(collection_key, []) if isinstance(project.get(collection_key), list) else []
                    for member in rows:
                        if isinstance(member, dict) and str(member.get("nim", "")) == old_nim:
                            member["nim"] = new_nim
                            member["name"] = current.get("name", member.get("name", ""))
                            member["prodi"] = current.get("prodi", member.get("prodi", ""))
                groups = project.get("groups", []) if isinstance(project.get("groups"), list) else []
                for group in groups:
                    members = group.get("members", []) if isinstance(group, dict) and isinstance(group.get("members"), list) else []
                    for member in members:
                        if isinstance(member, dict) and str(member.get("nim", "")) == old_nim:
                            member["nim"] = new_nim
                            member["name"] = current.get("name", member.get("name", ""))
                            member["prodi"] = current.get("prodi", member.get("prodi", ""))

            # Menghapus akun mahasiswa hanya menghapus keanggotaan/pengajuannya, bukan anggota lain.
            project["members"] = [m for m in project.get("members", []) if not isinstance(m, dict) or str(m.get("nim", "")) not in removed_nims]
            project["applicants"] = [m for m in project.get("applicants", []) if not isinstance(m, dict) or str(m.get("nim", "")) not in removed_nims]
            for group in project.get("groups", []) if isinstance(project.get("groups"), list) else []:
                if isinstance(group, dict) and isinstance(group.get("members"), list):
                    group["members"] = [m for m in group["members"] if not isinstance(m, dict) or str(m.get("nim", "")) not in removed_nims]

            for old_nip, old_user, current in lecturer_updates:
                new_nip = str(current.get("nip") or current.get("username") or "")
                for field in ("supervisorNip", "creatorNip", "ownerNip"):
                    if str(project.get(field, "")) == old_nip:
                        project[field] = new_nip
                old_name = str(old_user.get("name", ""))
                new_name = str(current.get("name", old_name))
                if str(project.get("supervisor", "")) == old_name:
                    project["supervisor"] = new_name
                if str(project.get("creator", "")) == old_name and "dosen" in str(project.get("creatorRole", "")).lower():
                    project["creator"] = new_name
            output.append(project)
        return output

    def __merge_invitations(self, old_rows, new_rows, actor):
        """Gabungkan undangan yang dikirim/diterima oleh akun aktif saja.

        Data undangan milik pengguna lain dipertahankan agar satu role tidak dapat
        menghapus atau mengganti undangan dari tampilan state yang telah difilter.
        """
        identity = str(actor.identifier or "")
        name = str(actor.full_name or "")

        def owned(row):
            if actor.role == "student":
                return str(row.get("nim", "")) == identity
            if actor.role == "lecturer":
                return (str(row.get("senderNip", row.get("lecturerNip", ""))) == identity
                        or (bool(name) and str(row.get("sender", "")) == name))
            return False

        old_rows = [deepcopy(row) for row in old_rows if isinstance(row, dict)]
        new_rows = [deepcopy(row) for row in new_rows if isinstance(row, dict)]
        incoming_by_id = {str(row.get("id", "")): row for row in new_rows}
        old_ids = {str(row.get("id", "")) for row in old_rows}
        output = []
        for old in old_rows:
            rid = str(old.get("id", ""))
            incoming = incoming_by_id.get(rid)
            if owned(old) and incoming and owned(incoming):
                output.append(incoming)
            elif owned(old) and incoming is None:
                # Hilangnya undangan dari tampilan terfilter milik pemanggil berarti undangan itu ditangani/dihapus.
                continue
            else:
                output.append(old)
        for row in new_rows:
            rid = str(row.get("id", ""))
            if rid not in old_ids and owned(row):
                output.append(row)
        return output

    def __merge_notifications(self, old_rows, new_rows, actor):
        """Pertahankan isi notifikasi; izinkan perubahan status baca untuk akun sendiri.

        Kunci `readBy` dibedakan menurut role dan identitas agar status baca pengguna lain
        tidak tertimpa oleh snapshot yang dikirim dari browser.
        """
        identity = str(actor.identifier or "")
        if actor.role == "admin":
            account_key = f"admin:{identity or 'admin'}"
        elif actor.role == "lecturer":
            account_key = f"lecturer:{identity}"
        else:
            account_key = f"student:{identity}"
        old_rows = [deepcopy(row) for row in old_rows if isinstance(row, dict)]
        new_rows = [deepcopy(row) for row in new_rows if isinstance(row, dict)]
        incoming_by_id = {str(row.get("id", "")): row for row in new_rows}
        old_ids = {str(row.get("id", "")) for row in old_rows}
        output = []
        for old in old_rows:
            incoming = incoming_by_id.get(str(old.get("id", "")))
            if incoming is not None:
                original_read = old.get("readBy") if isinstance(old.get("readBy"), dict) else {}
                incoming_read = incoming.get("readBy") if isinstance(incoming.get("readBy"), dict) else {}
                if account_key in incoming_read:
                    original_read[account_key] = bool(incoming_read[account_key])
                old["readBy"] = original_read
            # Notifikasi yang tidak muncul pada respons terfilter tetap dipertahankan bagi pemiliknya.
            output.append(old)
        # Notifikasi baru dapat ditambahkan; isi notifikasi lama tidak dapat diubah klien.
        for row in new_rows:
            if str(row.get("id", "")) not in old_ids:
                output.append(row)
        return output

    def __merge_owned_rows(self, old_rows, new_rows, owner_key, owner_value):
        """Ganti hanya baris milik identitas tertentu dan pertahankan baris lain."""
        retained = [deepcopy(row) for row in old_rows if str(row.get(owner_key, "")) != owner_value]
        changed = [deepcopy(row) for row in new_rows if str(row.get(owner_key, "")) == owner_value]
        return retained + changed

    def __merge_profile_map(self, old_map, new_map, owner_value):
        """Perbarui satu profil mahasiswa tanpa menimpa profil mahasiswa lain."""
        result = deepcopy(old_map if isinstance(old_map, dict) else {})
        if isinstance(new_map, dict) and owner_value in new_map:
            result[owner_value] = deepcopy(new_map[owner_value])
        return result

    def __student_achievement_changes(self, old_rows, new_rows, nim):
        """Izinkan pengajuan prestasi mahasiswa, tetapi pertahankan hasil validasi Admin."""
        old_by_id = {str(row.get("id")): row for row in old_rows if str(row.get("nim", "")) == nim}
        retained = [deepcopy(row) for row in old_rows if str(row.get("nim", "")) != nim]
        changed = []
        for row in new_rows:
            if str(row.get("nim", "")) != nim:
                continue
            row = deepcopy(row)
            old_row = old_by_id.get(str(row.get("id")))
            if old_row:
                # Mahasiswa boleh memperbarui metadata pengajuan, tetapi tidak dapat
                # mengubah hasil validasi yang hanya boleh ditetapkan Admin.
                for key in ("status", "validatedBy", "validatedAt"):
                    row[key] = old_row.get(key, "Menunggu Validasi" if key == "status" else "-")
            else:
                row["status"] = "Menunggu Validasi"
                row["validatedBy"] = "-"
                row["validatedAt"] = "-"
            changed.append(row)
        return retained + changed

    def __student_project_changes(self, old_projects, new_projects, actor, old_state, old_invitations, new_invitations):
        """Gabungkan perubahan proyek mahasiswa sesuai tindakan yang diizinkan.

        Mahasiswa dapat membuat/mengedit proposalnya sebelum ditinjau, mendaftar ke
        proyek umum yang terbuka, menerima undangan yang sah, mengusulkan anggota, dan
        mengunggah berkas untuk tahap yang sudah ditetapkan dosen. Identitas pemilik,
        struktur tahap, status verifikasi, dan proyek milik pihak lain tetap dijaga server.
        """
        nim = str(actor.identifier or "")
        old_by_id = {str(item.get("id")): item for item in old_projects if isinstance(item, dict)}
        master = old_state.get("masterData", {}) if isinstance(old_state.get("masterData"), dict) else {}
        configured = set(master.get("projectCategories") or DEFAULT_CATEGORIES)
        output = []
        seen = set()

        for candidate in new_projects:
            if not isinstance(candidate, dict):
                continue
            pid = str(candidate.get("id", "")).strip()
            # ID kosong/duplikat tidak boleh membuat duplikasi atau mengganti proyek lain.
            if not pid or pid in seen:
                continue
            old = old_by_id.get(pid)
            seen.add(pid)

            if old is None:
                # Hanya proyek baru yang benar-benar dibuat oleh mahasiswa aktif yang
                # boleh masuk sebagai proposal. Status/pemilik berasal dari server.
                if str(candidate.get("creatorNim", "")) != nim:
                    continue
                category = str(candidate.get("category", ""))
                if category not in configured:
                    continue
                account = self.__student_account_record(old_state, nim, actor) or {}
                item = deepcopy(candidate)
                item["creatorNim"] = nim
                item["creator"] = str(account.get("name") or actor.full_name or actor.username)[:150]
                item["creatorRole"] = "Ketua Tim Mahasiswa"
                item["creatorAngkatan"] = str(account.get("angkatan") or "")
                item["department"] = str(account.get("prodi") or "-")[:150]
                item["status"] = "Diajukan"
                item["isGroup"] = item.get("isGroup") is True
                supervisor = self.__student_supervisor_record(old_state, item)
                if category == "Proyek Mata Kuliah" and supervisor is None:
                    # Proyek mata kuliah harus berada di bawah dosen yang benar-benar
                    # tercatat mengampu mata kuliah terpilih.
                    continue
                if supervisor is not None:
                    item["supervisorNip"] = str(supervisor.get("nip") or supervisor.get("username") or "")
                    item["supervisor"] = str(supervisor.get("name") or "Dosen")[:150]
                else:
                    item["supervisorNip"] = ""
                    item["supervisor"] = ""
                item.pop("creatorNip", None)
                for key in ("ownerNip", "ownerName", "ownedAt"):
                    item.pop(key, None)
                if category == "Proyek Mata Kuliah":
                    item["studentCreated"] = True
                    if not self.__student_matches_course_scope(old_state, item, nim, actor):
                        continue
                else:
                    item.pop("studentCreated", None)
                    if category == "Informatika untuk Masyarakat" and not self.__student_matches_project_member_scope(old_state, item, nim):
                        continue
                # Tahap dokumentasi ditentukan dosen setelah proposal diterima.
                item["milestones"] = []
                if item.get("isGroup"):
                    try:
                        capacity = max(1, min(20, int(item.get("membersPerGroup") or 1)))
                    except (TypeError, ValueError):
                        capacity = 1
                    item["membersPerGroup"] = capacity
                    clean_groups = []
                    seen_members = set()
                    candidate_groups = item.get("groups", []) if isinstance(item.get("groups"), list) else []
                    for original_group in candidate_groups[:20]:
                        if not isinstance(original_group, dict):
                            continue
                        group = deepcopy(original_group)
                        group["milestones"] = []
                        safe_members = []
                        for member in group.get("members", []) if isinstance(group.get("members"), list) else []:
                            if not isinstance(member, dict) or len(safe_members) >= capacity:
                                continue
                            target_nim = str(member.get("nim", ""))
                            if not target_nim or target_nim in seen_members:
                                continue
                            target_account = self.__student_account_record(old_state, target_nim, actor if target_nim == nim else None)
                            if not target_account or not self.__student_matches_project_member_scope(old_state, item, target_nim):
                                continue
                            safe_members.append({
                                "nim": target_nim,
                                "name": str(target_account.get("name") or target_nim)[:150],
                                "prodi": str(target_account.get("prodi") or "-")[:150],
                                "role": str(member.get("role") or "Anggota")[:80],
                                "approved": False,
                            })
                            seen_members.add(target_nim)
                        group["members"] = safe_members
                        clean_groups.append(group)
                    item["groups"] = clean_groups
                    item["groupCount"] = len(clean_groups)
                    if category in {"Proyek Mata Kuliah", "Informatika untuk Masyarakat"} and not clean_groups:
                        continue
                else:
                    item["groups"] = []
                    item["groupCount"] = 0
                    item["membersPerGroup"] = 0
                if isinstance(item.get("members"), list):
                    safe_members = []
                    for member in item["members"]:
                        if not isinstance(member, dict):
                            continue
                        target_nim = str(member.get("nim", ""))
                        target_account = self.__student_account_record(old_state, target_nim, actor if target_nim == nim else None)
                        if not target_nim or not target_account:
                            continue
                        if target_nim != nim and not self.__student_matches_project_member_scope(old_state, item, target_nim):
                            continue
                        safe_members.append({
                            "nim": target_nim,
                            "name": str(target_account.get("name") or target_nim)[:150],
                            "prodi": str(target_account.get("prodi") or "-")[:150],
                            "role": str(member.get("role") or ("Ketua Tim" if target_nim == nim else "Anggota Tim"))[:80],
                            "approved": False,
                        })
                    # Identitas mahasiswa tidak boleh terduplikasi sebagai anggota.
                    unique_members = []
                    direct_nims = set()
                    for member in safe_members:
                        if member["nim"] in direct_nims:
                            continue
                        direct_nims.add(member["nim"])
                        unique_members.append(member)
                    item["members"] = unique_members
                if category in {"Proyek Mata Kuliah", "Informatika untuk Masyarakat"}:
                    try:
                        item["membersNeeded"] = max(1, int(item.get("membersNeeded") or 1))
                    except (TypeError, ValueError):
                        item["membersNeeded"] = 1
                else:
                    try:
                        needed = int(item.get("membersNeeded"))
                    except (TypeError, ValueError):
                        continue
                    if needed < 1 or needed > 40:
                        continue
                    item["membersNeeded"] = needed
                    if item.get("isGroup"):
                        assigned_count = sum(len(group.get("members", [])) for group in item.get("groups", []))
                        if assigned_count > needed or needed > len(item.get("groups", [])) * item["membersPerGroup"]:
                            continue
                    elif len(item.get("members", [])) > needed:
                        continue
                output.append(item)
                continue

            if str(old.get("creatorNim", "")) == nim:
                if old.get("status") == "Diajukan":
                    # Edit proposal sendiri sebelum ditinjau. Identitas, status dan
                    # definisi tahap tetap berasal dari server.
                    item = deepcopy(candidate)
                    item["status"] = old.get("status", "Diajukan")
                    for key in ("creatorNim", "creatorNip", "creator", "creatorRole", "creatorAngkatan",
                                "department", "ownerNip", "ownerName", "ownedAt"):
                        if key in old:
                            item[key] = deepcopy(old[key])
                        else:
                            item.pop(key, None)
                    item["isGroup"] = item.get("isGroup") is True
                    if item.get("category") not in configured:
                        item["category"] = old.get("category", "")
                        item["course"] = old.get("course", "")
                        item["angkatan"] = old.get("angkatan", "")
                        item["kelas"] = deepcopy(old.get("kelas", []))
                    if item.get("category") == "Proyek Mata Kuliah":
                        item["studentCreated"] = True
                        if (self.__student_supervisor_record(old_state, item) is None
                                or not self.__student_matches_course_scope(old_state, item, nim, actor)):
                            output.append(deepcopy(old))
                            continue
                    elif item.get("category") == "Informatika untuk Masyarakat":
                        item.pop("studentCreated", None)
                        if not self.__student_matches_project_member_scope(old_state, item, nim):
                            output.append(deepcopy(old))
                            continue
                    else:
                        item.pop("studentCreated", None)

                    item["milestones"] = deepcopy(old.get("milestones", [])) if isinstance(old.get("milestones"), list) else []
                    old_groups = {str(row.get("id", "")): row for row in old.get("groups", []) if isinstance(row, dict)} if isinstance(old.get("groups"), list) else {}
                    clean_groups = []
                    seen_member_nims = set()
                    try:
                        capacity = max(1, min(20, int(item.get("membersPerGroup") or 1)))
                    except (TypeError, ValueError):
                        capacity = 1
                    candidate_groups = item.get("groups", []) if isinstance(item.get("groups"), list) else []
                    for group in candidate_groups[:20]:
                        if not isinstance(group, dict):
                            continue
                        prior = old_groups.get(str(group.get("id", "")), {})
                        group["milestones"] = deepcopy(prior.get("milestones", [])) if isinstance(prior.get("milestones"), list) else []
                        safe_members = []
                        for member in group.get("members", []) if isinstance(group.get("members"), list) else []:
                            if not isinstance(member, dict) or len(safe_members) >= capacity:
                                continue
                            target_nim = str(member.get("nim", ""))
                            if not target_nim or target_nim in seen_member_nims:
                                continue
                            target_account = self.__student_account_record(old_state, target_nim, actor if target_nim == nim else None)
                            if not target_account or not self.__student_matches_project_member_scope(old_state, item, target_nim):
                                continue
                            safe_members.append({
                                "nim": target_nim,
                                "name": str(target_account.get("name") or target_nim)[:150],
                                "prodi": str(target_account.get("prodi") or "-")[:150],
                                "role": str(member.get("role") or "Anggota")[:80],
                                "approved": False,
                            })
                            seen_member_nims.add(target_nim)
                        group["members"] = safe_members
                        clean_groups.append(group)
                    item["groups"] = clean_groups if item.get("isGroup") else []
                    item["groupCount"] = len(item["groups"])
                    item["membersPerGroup"] = capacity if item.get("isGroup") else 0
                    safe_direct_members = []
                    for member in item.get("members", []) if isinstance(item.get("members"), list) else []:
                        if not isinstance(member, dict):
                            continue
                        target_nim = str(member.get("nim", ""))
                        if not target_nim or target_nim in seen_member_nims:
                            continue
                        target_account = self.__student_account_record(old_state, target_nim, actor if target_nim == nim else None)
                        if not target_account or (target_nim != nim and not self.__student_matches_project_member_scope(old_state, item, target_nim)):
                            continue
                        safe_direct_members.append({
                            "nim": target_nim, "name": str(target_account.get("name") or target_nim)[:150],
                            "prodi": str(target_account.get("prodi") or "-")[:150],
                            "role": str(member.get("role") or ("Ketua Tim" if target_nim == nim else "Anggota Tim"))[:80],
                            "approved": False,
                        })
                        seen_member_nims.add(target_nim)
                    item["members"] = safe_direct_members
                    if item.get("category") not in {"Proyek Mata Kuliah", "Informatika untuk Masyarakat"}:
                        try:
                            needed = int(item.get("membersNeeded"))
                        except (TypeError, ValueError):
                            output.append(deepcopy(old))
                            continue
                        assigned = sum(len(group.get("members", [])) for group in item["groups"]) if item.get("isGroup") else len(item["members"])
                        if needed < 1 or needed > 40 or assigned > needed or (item.get("isGroup") and needed > len(item["groups"]) * capacity):
                            output.append(deepcopy(old))
                            continue
                    proposed_supervisor = self.__student_supervisor_record(old_state, item)
                    if proposed_supervisor is not None:
                        item["supervisorNip"] = str(proposed_supervisor.get("nip") or proposed_supervisor.get("username") or "")
                        item["supervisor"] = str(proposed_supervisor.get("name") or "Dosen")[:150]
                    else:
                        for key in ("supervisorNip", "supervisor"):
                            if key in old:
                                item[key] = deepcopy(old[key])
                            else:
                                item.pop(key, None)
                else:
                    # Setelah proposal diproses, mahasiswa tidak lagi mengubah metadata
                    # proyek. Ia hanya mengirim dokumen ke tahap yang memang ditetapkan.
                    item = deepcopy(old)
                    if old.get("isGroup"):
                        item["groups"] = self.__merge_student_group_changes(old, candidate, actor, old_state)
                    else:
                        item["milestones"] = self.__merge_student_milestones(
                            old.get("milestones", []), candidate.get("milestones", []),
                            actor, pid, None,
                        )
                output.append(item)
                continue

            # Proyek pihak lain selalu dimulai dari salinan server; klien tidak dapat
            # mengubah judul, kuota, daftar anggota, pemilik, atau konfigurasi proyek.
            item = deepcopy(old)
            item["applicants"] = self.__merge_student_application_rows(old, candidate, actor, old_state)
            accepted_invitation = self.__student_accepted_invitation(
                old, candidate, actor, old_invitations, new_invitations
            )
            item["members"] = deepcopy(old.get("members", [])) if isinstance(old.get("members"), list) else []
            if accepted_invitation and not old.get("isGroup"):
                member_nims = {str(row.get("nim", "")) for row in item["members"] if isinstance(row, dict)}
                if nim not in member_nims:
                    account = self.__student_account_record(old_state, nim, actor) or {}
                    item["members"].append({
                        "nim": nim,
                        "name": str(account.get("name") or actor.full_name or actor.username),
                        "prodi": str(account.get("prodi") or "-"),
                        "role": "Anggota Tim",
                        "approved": True,
                    })

            if old.get("isGroup"):
                item["groups"] = self.__merge_student_group_changes(old, candidate, actor, old_state)
            elif self.__student_has_approved_membership(old, nim) or accepted_invitation:
                item["milestones"] = self.__merge_student_milestones(
                    old.get("milestones", []), candidate.get("milestones", []), actor, pid, None
                )
            output.append(item)

        # Menghapus proposal sendiri diizinkan hanya sebelum Dosen memprosesnya.
        # Proyek aktif/ditolak dan proyek pihak lain tidak dapat dihapus melalui snapshot.
        for old in old_projects:
            if not isinstance(old, dict) or str(old.get("id", "")) in seen:
                continue
            if str(old.get("creatorNim", "")) == nim and old.get("status") == "Diajukan":
                continue
            output.append(deepcopy(old))
        return output

    def __student_supervisor_record(self, state, project):
        """Cari dosen aktif yang dipilih dan pastikan ia mengampu mata kuliah terkait."""
        supervisor_nip = str(project.get("supervisorNip") or "").strip()
        if not supervisor_nip:
            return None
        users = state.get("users", []) if isinstance(state, dict) else []
        lecturer = next((row for row in users if isinstance(row, dict)
                         and row.get("role") == "lecturer"
                         and row.get("active", True) is not False
                         and supervisor_nip == str(row.get("nip") or row.get("username") or "")), None) if isinstance(users, list) else None
        if lecturer is None:
            return None
        if str(project.get("category") or "") == "Proyek Mata Kuliah":
            courses = lecturer.get("mataKuliahDiampu", [])
            if not isinstance(courses, list) or str(project.get("course") or "") not in {str(value) for value in courses}:
                return None
        return lecturer

    def __student_account_record(self, state, nim, actor=None):
        """Temukan data mahasiswa aktif yang diperlukan untuk memvalidasi keanggotaan."""
        users = state.get("users", []) if isinstance(state, dict) else []
        for row in users if isinstance(users, list) else []:
            if (isinstance(row, dict) and row.get("role") == "student"
                    and str(row.get("nim") or row.get("username") or "") == str(nim)
                    and row.get("active", True) is not False):
                return row
        if actor is not None and str(actor.identifier or "") == str(nim):
            profile = deepcopy(actor.profile_data) if isinstance(actor.profile_data, dict) else {}
            profile.update({
                "role": "student", "nim": str(actor.identifier or ""),
                "name": actor.full_name or profile.get("name") or actor.username,
                "email": actor.email or profile.get("email", ""),
                "active": bool(actor.is_active),
            })
            return profile
        return None

    def __student_matches_course_scope(self, state, project, nim, actor=None):
        """Periksa angkatan, kelas, dan mata kuliah sesuai cakupan proyek kuliah."""
        account = self.__student_account_record(state, nim, actor)
        if not account:
            return False
        cohort = str(account.get("angkatan") or "")
        project_cohort = str(project.get("angkatan") or "")
        if project_cohort and cohort != project_cohort:
            return False
        project_classes = project.get("kelas", [])
        student_class = str(account.get("kelas") or "")
        if isinstance(project_classes, list) and project_classes and student_class not in {str(value) for value in project_classes}:
            return False
        courses = account.get("mataKuliahDiambil")
        if isinstance(courses, list) and str(project.get("course") or "") not in {str(value) for value in courses}:
            return False
        if courses is not None and not isinstance(courses, list):
            return False
        return True

    def __student_matches_project_member_scope(self, state, project, nim):
        """Validasi akun target pengusulan anggota sesuai kategori dan angkatan."""
        account = self.__student_account_record(state, nim)
        if not account:
            return False
        category = str(project.get("category") or "")
        courses = account.get("mataKuliahDiambil", [])
        if category == "Proyek Mata Kuliah":
            return self.__student_matches_course_scope(state, project, nim)
        if category == "Informatika untuk Masyarakat":
            enrolled = isinstance(courses, list) and any(
                "informatika untuk masyarakat" in str(course).lower() for course in courses
            )
            if not enrolled:
                return False
        creator_nim = str(project.get("creatorNim") or "")
        if project.get("studentCreated") or creator_nim:
            creator = self.__student_account_record(state, creator_nim) if creator_nim else None
            creator_cohort = str(project.get("creatorAngkatan") or (creator or {}).get("angkatan") or "").strip()
            if creator_cohort and str(account.get("angkatan") or "").strip() != creator_cohort:
                return False
            if not creator_cohort:
                return False
        return True

    def __student_has_approved_membership(self, project, nim):
        """True jika mahasiswa merupakan anggota aktif yang telah disetujui."""
        rows = project.get("members", []) if isinstance(project.get("members"), list) else []
        if any(isinstance(row, dict) and str(row.get("nim", "")) == nim and row.get("approved", True) is not False for row in rows):
            return True
        groups = project.get("groups", []) if isinstance(project.get("groups"), list) else []
        return any(
            isinstance(member, dict) and str(member.get("nim", "")) == nim and member.get("approved", True) is not False
            for group in groups if isinstance(group, dict)
            for member in (group.get("members", []) if isinstance(group.get("members"), list) else [])
        )

    def __merge_student_application_rows(self, old_project, candidate, actor, old_state):
        """Terima pendaftaran baru hanya untuk mahasiswa aktif dan proyek umum terbuka."""
        old_rows = [deepcopy(row) for row in old_project.get("applicants", []) if isinstance(row, dict)]
        nim = str(actor.identifier or "")
        if any(str(row.get("nim", "")) == nim for row in old_rows):
            return old_rows
        if self.__student_has_approved_membership(old_project, nim):
            return old_rows
        if old_project.get("status") != "Open" or old_project.get("registrationClosed"):
            return old_rows
        private_categories = {"Proyek Mata Kuliah", "Informatika untuk Masyarakat"}
        master = old_state.get("masterData", {}) if isinstance(old_state.get("masterData"), dict) else {}
        configured = set(master.get("projectCategories") or DEFAULT_CATEGORIES)
        if old_project.get("category") in private_categories or old_project.get("category") not in configured:
            return old_rows
        try:
            limit = int(old_project.get("membersNeeded") or 0)
        except (TypeError, ValueError):
            limit = 0
        old_members = old_project.get("members", [])
        member_count = len(old_members) if isinstance(old_members, list) else 0
        if old_project.get("isGroup"):
            old_groups = old_project.get("groups", [])
            member_count = sum(
                len(group.get("members", []))
                for group in old_groups if isinstance(group, dict) and isinstance(group.get("members"), list)
            ) if isinstance(old_groups, list) else 0
        if limit > 0 and member_count >= limit:
            return old_rows

        rows = candidate.get("applicants", []) if isinstance(candidate.get("applicants"), list) else []
        existing_ids = {str(row.get("id", "")) for row in old_rows}
        account = self.__student_account_record(old_state, nim, actor) or {}
        for row in rows:
            if not isinstance(row, dict) or str(row.get("nim", "")) != nim:
                continue
            row_id = str(row.get("id", ""))[:100]
            if not row_id or row_id in existing_ids:
                continue
            # Identitas dan status lamaran dibuat oleh server; field bebas dibatasi panjangnya.
            old_rows.append({
                "id": row_id, "nim": nim,
                "name": str(account.get("name") or actor.full_name or actor.username)[:150],
                "prodi": str(account.get("prodi") or "-")[:150],
                "skills": str(row.get("skills") or "")[:250],
                "role": str(row.get("role") or "Anggota Tim")[:80],
                "motivation": str(row.get("motivation") or "")[:1000],
                "status": "Pending",
            })
            break
        return old_rows

    def __student_accepted_invitation(self, project, candidate, actor, old_invitations, new_invitations):
        """Kenali penambahan anggota langsung hanya jika ada undangan sah yang diterima."""
        if not isinstance(old_invitations, list):
            return False
        if project.get("isGroup"):
            return False
        nim = str(actor.identifier or "")
        old_members = project.get("members", []) if isinstance(project.get("members"), list) else []
        if any(isinstance(row, dict) and str(row.get("nim", "")) == nim for row in old_members):
            return False
        rows = candidate.get("members", []) if isinstance(candidate.get("members"), list) else []
        if not any(isinstance(row, dict) and str(row.get("nim", "")) == nim and row.get("approved", True) is not False for row in rows):
            return False
        active_invitation_ids = {
            str(row.get("id", "")) for row in new_invitations if isinstance(row, dict)
        } if isinstance(new_invitations, list) else set()
        return any(
            isinstance(invitation, dict)
            and str(invitation.get("nim", "")) == nim
            and str(invitation.get("projectId", "")) == str(project.get("id", ""))
            and invitation.get("status", "Menunggu Respon") == "Menunggu Respon"
            and str(invitation.get("id", "")) not in active_invitation_ids
            for invitation in old_invitations
        )

    def __merge_student_milestones(self, old_rows, new_rows, actor, project_id, group_id=None):
        """Terima pengiriman berkas untuk tahap yang telah dibuat dosen, tanpa mengubah definisinya."""
        old_rows = [deepcopy(row) for row in old_rows if isinstance(row, dict)] if isinstance(old_rows, list) else []
        new_rows = [row for row in new_rows if isinstance(row, dict)] if isinstance(new_rows, list) else []
        incoming_by_key = {
            str(row.get("key", row.get("id", ""))): row
            for row in new_rows if str(row.get("key", row.get("id", "")))
        }
        merged = []
        for original in old_rows:
            stage_key = str(original.get("key", original.get("id", "")))
            item = deepcopy(original)
            incoming = incoming_by_key.get(stage_key)
            old_status = str(original.get("status", "Belum Dimulai"))
            if incoming and old_status in {"Belum Dimulai", "Revisi"} and incoming.get("status") == "Menunggu Verifikasi":
                # ID berkas harus benar-benar diunggah oleh akun ini untuk proyek dan
                # tahap yang sama. Mengetahui ID dokumen saja tidak memberi hak pakai.
                file_id = str(incoming.get("fileId", ""))
                document = self.__student_milestone_document(actor, file_id, project_id, group_id, stage_key)
                if document is not None:
                    item["fileId"] = str(document.id)
                    item["fileName"] = document.original_name
                    item["fileType"] = document.content_type
                    item["fileSize"] = document.size
                    item["submittedAt"] = str(incoming.get("submittedAt", ""))[:80]
                    item["note"] = str(incoming.get("note", ""))[:2000]
                    item["status"] = "Menunggu Verifikasi"
                    item["reviewNote"] = ""
                    item["verifiedBy"] = ""
                    item["verifiedAt"] = ""
                    try:
                        revision_count = max(0, int(original.get("revisionCount", 0) or 0))
                    except (TypeError, ValueError):
                        revision_count = 0
                    item["revisionCount"] = revision_count + 1 if old_status == "Revisi" else revision_count
            # Tahap yang dihilangkan dari request tetap dipertahankan. Definisi tahap,
            # status validasi, catatan dosen, dan status selesai tidak berasal dari klien.
            merged.append(item)
        return merged

    def __student_milestone_document(self, actor, file_id, project_id, group_id, stage_key):
        """Pastikan ID berkas mengarah ke unggahan milestone milik pengusul dan konteks yang tepat."""
        if not file_id:
            return None
        try:
            document = UploadedDocument.objects.filter(pk=file_id, uploaded_by=actor).first()
        except (ValueError, TypeError, ValidationError):
            return None
        if document is None or not isinstance(document.metadata, dict):
            return None
        metadata = document.metadata
        if (metadata.get("purpose") != "milestone"
                or str(metadata.get("projectId", "")) != str(project_id)
                or str(metadata.get("groupId") or "") != str(group_id or "")
                or str(metadata.get("milestoneKey", "")) != str(stage_key)):
            return None
        return document

    def __merge_student_group_changes(self, old_project, candidate, actor, old_state):
        """Izinkan usulan anggota tertunda dan dokumentasi pada kelompok milik mahasiswa."""
        nim = str(actor.identifier or "")
        old_groups = old_project.get("groups", []) if isinstance(old_project.get("groups"), list) else []
        incoming_groups = candidate.get("groups", []) if isinstance(candidate.get("groups"), list) else []
        incoming_by_id = {str(group.get("id", "")): group for group in incoming_groups if isinstance(group, dict)}
        actor_memberships = {}
        for group in old_groups:
            if not isinstance(group, dict):
                continue
            for member in group.get("members", []) if isinstance(group.get("members"), list) else []:
                if isinstance(member, dict) and str(member.get("nim", "")) == nim:
                    actor_memberships[str(group.get("id", ""))] = member.get("approved", True) is not False
        category = str(old_project.get("category") or "")
        course_project = category == "Proyek Mata Kuliah"
        course_scope_ok = (course_project and old_project.get("status") == "Active"
                           and not old_project.get("studentCreated")
                           and self.__student_matches_course_scope(old_state, old_project, nim, actor))
        all_existing_nims = set()
        direct_members = old_project.get("members", []) if isinstance(old_project.get("members"), list) else []
        for member in direct_members:
            if isinstance(member, dict):
                all_existing_nims.add(str(member.get("nim", "")))
        for group in old_groups:
            if isinstance(group, dict):
                for member in group.get("members", []) if isinstance(group.get("members"), list) else []:
                    if isinstance(member, dict):
                        all_existing_nims.add(str(member.get("nim", "")))
        output = []
        for original_group in old_groups:
            if not isinstance(original_group, dict):
                continue
            group = deepcopy(original_group)
            incoming = incoming_by_id.get(str(group.get("id", "")), {})
            group_id = str(group.get("id", ""))
            actor_is_approved_here = actor_memberships.get(group_id, False)
            if actor_is_approved_here:
                group["milestones"] = self.__merge_student_milestones(
                    original_group.get("milestones", []), incoming.get("milestones", []),
                    actor, old_project.get("id", ""), group_id,
                )

            if course_project:
                can_propose = course_scope_ok and (
                    (not actor_memberships) or actor_is_approved_here
                ) and not any(not approved for approved in actor_memberships.values())
            else:
                can_propose = (actor_is_approved_here and old_project.get("status") not in {"Diajukan", "Ditolak", "Closed"})
            if can_propose:
                current_members = group.get("members", []) if isinstance(group.get("members"), list) else []
                try:
                    capacity = max(1, int(old_project.get("membersPerGroup") or 1))
                except (TypeError, ValueError):
                    capacity = 1
                for proposed in incoming.get("members", []) if isinstance(incoming.get("members"), list) else []:
                    if not isinstance(proposed, dict):
                        continue
                    target_nim = str(proposed.get("nim", ""))
                    if (not target_nim or target_nim in all_existing_nims
                            or str(proposed.get("proposedBy", "")) != nim
                            or proposed.get("approved") is not False
                            or len(current_members) >= capacity):
                        continue
                    target_account = self.__student_account_record(old_state, target_nim)
                    if not target_account:
                        continue
                    if not self.__student_matches_project_member_scope(old_state, old_project, target_nim):
                        continue
                    trusted_proposal = {
                        "nim": target_nim,
                        "name": str(target_account.get("name") or target_nim)[:150],
                        "prodi": str(target_account.get("prodi") or "-")[:150],
                        "role": str(proposed.get("role") or "Anggota")[:80],
                        "approved": False,
                        "proposedBy": nim,
                        "proposedByName": str(actor.full_name or actor.username)[:150],
                    }
                    current_members.append(trusted_proposal)
                    all_existing_nims.add(target_nim)
                group["members"] = current_members
            output.append(group)
        # Dosen/Admin, bukan mahasiswa, mengatur struktur dan jumlah kelompok.
        return output

    def __keep_student_milestone_status(self, old_project, new_project):
        """Pulihkan status verifikasi dari server agar mahasiswa tidak menyetujui dokumen sendiri."""
        def keep(old_rows, new_rows):
            old_by_key = {
                str(row.get("key", row.get("id", ""))): row
                for row in old_rows if isinstance(row, dict)
            }
            for row in new_rows:
                if not isinstance(row, dict):
                    continue
                prior = old_by_key.get(str(row.get("key", row.get("id", ""))))
                if not prior:
                    # Tahap baru belum pernah diverifikasi; jangan menerima status
                    # persetujuan yang dikirim sendiri oleh mahasiswa.
                    if row.get("status") == "Disetujui":
                        row["status"] = "Menunggu Verifikasi"
                    for key in ("verifiedBy", "verifiedAt", "reviewNote"):
                        row[key] = ""
                    continue
                prior_status = prior.get("status", "Belum Dimulai")
                if prior_status == "Disetujui" or row.get("status") == "Disetujui":
                    # Mahasiswa tidak boleh membatalkan status persetujuan dosen dan
                    # juga tidak bisa menyetujui tahap sendiri.
                    row["status"] = prior_status if prior_status == "Disetujui" else "Menunggu Verifikasi"
                for key in ("verifiedBy", "verifiedAt", "reviewNote"):
                    row[key] = prior.get(key, "")
        keep(old_project.get("milestones", []) if isinstance(old_project.get("milestones"), list) else [],
             new_project.get("milestones", []) if isinstance(new_project.get("milestones"), list) else [])
        old_groups = {
            str(group.get("id")): group
            for group in (old_project.get("groups", []) if isinstance(old_project.get("groups"), list) else [])
            if isinstance(group, dict)
        }
        for group in new_project.get("groups", []) if isinstance(new_project.get("groups"), list) else []:
            if not isinstance(group, dict):
                continue
            old_group = old_groups.get(str(group.get("id")))
            if not old_group:
                continue
            keep(old_group.get("milestones", []) if isinstance(old_group.get("milestones"), list) else [],
                 group.get("milestones", []) if isinstance(group.get("milestones"), list) else [])

    def __lecturer_project_changes(self, old_projects, new_projects, nip):
        """Terima perubahan hanya pada proyek yang dapat dikelola dosen yang aktif."""
        old_by_id = {str(item.get("id")): item for item in old_projects}
        output, seen = [], set()
        for candidate in new_projects:
            if not isinstance(candidate, dict):
                continue
            pid = str(candidate.get("id", ""))
            old = old_by_id.get(pid)
            seen.add(pid)
            if old is None:
                if str(candidate.get("creatorNip", "")) == nip:
                    output.append(deepcopy(candidate))
                continue
            owner_nip = str(old.get("ownerNip", ""))
            # Bila pemilik sudah ditetapkan, hanya pemilik yang boleh mengubah/menghapus proyek.
            if owner_nip:
                permitted = owner_nip == nip
            else:
                permitted = (str(old.get("supervisorNip", "")) == nip
                             or str(old.get("creatorNip", "")) == nip
                             or (old.get("status") == "Diajukan"
                                 and old.get("category") not in {"Proyek Mata Kuliah", "Informatika untuk Masyarakat"}))
            output.append(deepcopy(candidate if permitted else old))
        for old in old_projects:
            if str(old.get("id", "")) not in seen:
                owner_nip = str(old.get("ownerNip", ""))
                owned = owner_nip == nip if owner_nip else nip in {
                    str(old.get("creatorNip", "")), str(old.get("supervisorNip", ""))
                }
                if not owned:
                    output.append(deepcopy(old))
        return output
