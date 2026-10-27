"""Tes integrasi dasar untuk memastikan batas autentikasi, state, dan berkas."""
import json
import tempfile
from copy import deepcopy
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from .models import AppState, UploadedDocument
from .repository import KreasiStateRepository, empty_portal_state

User = get_user_model()


class KreasiApiTests(TestCase):
    def setUp(self):
        self._media_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._media_dir.cleanup)
        self._media_settings = override_settings(MEDIA_ROOT=Path(self._media_dir.name))
        self._media_settings.enable()
        self.addCleanup(self._media_settings.disable)
        self.student = User.objects.create_user(
            username="mahasiswa1", password="Kreasi-Test-123!", role="student",
            identifier="230001", full_name="Mahasiswa Uji", profile_data={"nim": "230001"},
        )
        self.other_student = User.objects.create_user(
            username="mahasiswa2", password="Kreasi-Test-456!", role="student",
            identifier="230002", full_name="Mahasiswa Uji 2", profile_data={"nim": "230002"},
        )

    def test_state_endpoint_requires_login(self):
        response = self.client.get("/api/state/")
        self.assertEqual(response.status_code, 401)

    def test_wrong_login_returns_generic_account_message(self):
        response = self.client.post(
            "/api/auth/login/",
            data='{"username":"mahasiswa1","password":"salah","role":"student"}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["message"], "Akun tidak terdaftar di sistem")

    def test_student_cannot_overwrite_admin_managed_state(self):
        state = empty_portal_state()
        state["announcements"] = [{"id": "announcement-1", "title": "Pengumuman resmi"}]
        state["masterData"]["classes"] = ["A", "B"]
        AppState.objects.create(key="main", data=state, version=1)

        incoming = empty_portal_state()
        incoming["announcements"] = [{"id": "forged", "title": "Diubah mahasiswa"}]
        incoming["masterData"]["classes"] = ["HACK"]
        KreasiStateRepository().save_state(incoming, self.student)

        stored = AppState.objects.get(key="main").data
        self.assertEqual(stored["announcements"], [{"id": "announcement-1", "title": "Pengumuman resmi"}])
        self.assertEqual(stored["masterData"]["classes"], ["A", "B"])

    def test_uploaded_pdf_uses_server_detected_content_type_and_is_private(self):
        with tempfile.TemporaryDirectory() as media_dir:
            with override_settings(MEDIA_ROOT=Path(media_dir)):
                self.client.force_login(self.student)
                upload = SimpleUploadedFile(
                    "bukti.pdf", b"%PDF-1.4\ncontoh dokumen", content_type="text/html"
                )
                response = self.client.post(
                    "/api/documents/upload/",
                    {"file": upload, "metadata": '{"purpose":"achievement-proof","nim":"230001"}'},
                )
                self.assertEqual(response.status_code, 200, response.content)
                document = UploadedDocument.objects.get(pk=response.json()["id"])
                self.assertEqual(document.content_type, "application/pdf")

                allowed = self.client.get(f"/api/documents/{document.id}/")
                self.assertEqual(allowed.status_code, 200)
                self.assertEqual(allowed["Content-Type"], "application/pdf")
                self.assertTrue(allowed["Content-Disposition"].startswith("inline;"))
                allowed.close()

                self.client.force_login(self.other_student)
                denied = self.client.get(f"/api/documents/{document.id}/")
                self.assertEqual(denied.status_code, 403)


    def test_student_new_proposal_keeps_server_bound_creator_identity(self):
        state = empty_portal_state()
        state["users"] = [{
            "id": "user-1", "role": "student", "nim": "230001", "username": "mahasiswa1",
            "name": "Mahasiswa Uji", "prodi": "Informatika", "angkatan": "2023", "active": True,
        }]
        AppState.objects.create(key="main", data=state, version=1)
        incoming = deepcopy(state)
        incoming["projects"] = [{
            "id": "proposal-new", "title": "Proposal Baru", "category": "Kompetisi",
            "creatorNim": "230001", "creator": "Identitas Palsu", "creatorRole": "Admin",
            "status": "Active", "membersNeeded": 4, "isGroup": False,
            "members": [], "groups": [], "applicants": [], "milestones": [],
        }]

        KreasiStateRepository().save_state(incoming, self.student)
        project = AppState.objects.get(key="main").data["projects"][0]
        self.assertEqual(project["creatorNim"], "230001")
        self.assertEqual(project["creator"], "Mahasiswa Uji")
        self.assertEqual(project["creatorRole"], "Ketua Tim Mahasiswa")
        self.assertEqual(project["status"], "Diajukan")

    def test_student_can_submit_application_to_open_public_project(self):
        state = empty_portal_state()
        state["users"] = [
            {"id": "user-1", "role": "student", "nim": "230001", "username": "mahasiswa1",
             "name": "Mahasiswa Uji", "prodi": "Informatika", "active": True},
        ]
        state["projects"] = [{
            "id": "project-public-1", "title": "Proyek Kompetisi", "category": "Kompetisi",
            "creatorNim": "230099", "status": "Open", "isGroup": False,
            "membersNeeded": 5, "members": [], "applicants": [], "milestones": [],
        }]
        AppState.objects.create(key="main", data=state, version=1)
        incoming = deepcopy(state)
        incoming["projects"][0]["applicants"] = [{
            "id": "application-1", "nim": "230001", "name": "Mahasiswa Uji",
            "skills": "Python", "role": "Backend Developer", "motivation": "Ingin berkontribusi",
            "status": "Diterima",
        }]

        KreasiStateRepository().save_state(incoming, self.student)
        stored = AppState.objects.get(key="main").data["projects"][0]["applicants"]
        self.assertEqual(len(stored), 1)
        self.assertEqual(stored[0]["nim"], "230001")
        self.assertEqual(stored[0]["status"], "Pending")

    def test_student_can_propose_group_member_without_changing_verification(self):
        state = empty_portal_state()
        state["users"] = [
            {"id": "user-1", "role": "student", "nim": "230001", "username": "mahasiswa1",
             "name": "Mahasiswa Uji", "prodi": "Informatika", "angkatan": "2023", "kelas": "A",
             "mataKuliahDiambil": ["Basis Data"], "active": True},
            {"id": "user-2", "role": "student", "nim": "230002", "username": "mahasiswa2",
             "name": "Mahasiswa Uji 2", "prodi": "Informatika", "angkatan": "2023", "kelas": "A",
             "mataKuliahDiambil": ["Basis Data"], "active": True},
        ]
        state["projects"] = [{
            "id": "course-project-1", "title": "Proyek Basis Data", "category": "Proyek Mata Kuliah",
            "course": "Basis Data", "creatorNim": "199001", "creatorNip": "199001",
            "status": "Active", "studentCreated": False, "isGroup": True,
            "angkatan": "2023", "kelas": ["A"], "membersPerGroup": 3,
            "members": [], "applicants": [], "milestones": [],
            "groups": [{
                "id": "group-1", "name": "Kelompok 1", "members": [],
                "milestones": [{"key": "stage-1", "name": "Proposal", "status": "Menunggu Verifikasi",
                                "verifiedBy": "", "verifiedAt": "", "reviewNote": ""}],
            }],
        }]
        AppState.objects.create(key="main", data=state, version=1)
        incoming = deepcopy(state)
        group = incoming["projects"][0]["groups"][0]
        group["members"] = [{
            "nim": "230002", "name": "Nama Palsu", "prodi": "Palsu", "role": "Anggota",
            "approved": False, "proposedBy": "230001", "proposedByName": "Mahasiswa Uji",
        }]
        group["milestones"][0].update({
            "status": "Disetujui", "verifiedBy": "Mahasiswa Uji", "verifiedAt": "hari ini",
            "reviewNote": "disetujui sendiri",
        })

        KreasiStateRepository().save_state(incoming, self.student)
        stored_project = AppState.objects.get(key="main").data["projects"][0]
        proposed = stored_project["groups"][0]["members"]
        milestone = stored_project["groups"][0]["milestones"][0]
        self.assertEqual(len(proposed), 1)
        self.assertEqual(proposed[0]["nim"], "230002")
        self.assertEqual(proposed[0]["name"], "Mahasiswa Uji 2")
        self.assertFalse(proposed[0]["approved"])
        self.assertEqual(milestone["status"], "Menunggu Verifikasi")
        self.assertEqual(milestone["verifiedBy"], "")
        self.assertEqual(milestone["reviewNote"], "")

    def test_student_cannot_remove_or_change_already_approved_milestone(self):
        state = empty_portal_state()
        state["users"] = [
            {"id": "user-1", "role": "student", "nim": "230001", "username": "mahasiswa1",
             "name": "Mahasiswa Uji", "prodi": "Informatika", "active": True},
        ]
        state["projects"] = [{
            "id": "project-member-1", "title": "Proyek Tim", "category": "Kompetisi",
            "creatorNim": "230099", "status": "Active", "isGroup": False,
            "membersNeeded": 5,
            "members": [{"nim": "230001", "name": "Mahasiswa Uji", "approved": True}],
            "applicants": [],
            "milestones": [{"key": "stage-1", "name": "Proposal", "status": "Disetujui",
                            "verifiedBy": "Dosen Uji", "verifiedAt": "2026-10-01", "reviewNote": "OK"}],
        }]
        AppState.objects.create(key="main", data=state, version=1)
        incoming = deepcopy(state)
        incoming["projects"][0]["milestones"][0].update({
            "status": "Ditolak", "verifiedBy": "Mahasiswa Uji", "reviewNote": "palsu",
        })
        incoming["projects"][0]["milestones"].append({"key": "stage-2", "name": "Baru",
            "status": "Disetujui", "verifiedBy": "Mahasiswa Uji", "verifiedAt": "hari ini"})

        KreasiStateRepository().save_state(incoming, self.student)
        milestones = AppState.objects.get(key="main").data["projects"][0]["milestones"]
        self.assertEqual(milestones[0]["status"], "Disetujui")
        self.assertEqual(milestones[0]["verifiedBy"], "Dosen Uji")
        self.assertEqual(milestones[0]["reviewNote"], "OK")
        # Mahasiswa tidak dapat menambahkan tahapan baru; daftar tahap ditetapkan dosen.
        self.assertEqual(len(milestones), 1)


    def test_student_can_delete_only_own_unreviewed_project_proposal(self):
        state = empty_portal_state()
        state["projects"] = [{
            "id": "proposal-owned", "title": "Proposal saya", "category": "Kompetisi",
            "creatorNim": "230001", "status": "Diajukan", "studentCreated": False,
            "members": [], "applicants": [], "milestones": [], "groups": [],
        }, {
            "id": "proposal-other", "title": "Proposal orang lain", "category": "Kompetisi",
            "creatorNim": "230002", "status": "Diajukan", "members": [], "applicants": [],
            "milestones": [], "groups": [],
        }]
        AppState.objects.create(key="main", data=state, version=1)
        incoming = deepcopy(state)
        incoming["projects"] = [state["projects"][1]]

        KreasiStateRepository().save_state(incoming, self.student)
        projects = AppState.objects.get(key="main").data["projects"]
        self.assertEqual([project["id"] for project in projects], ["proposal-other"])

    def test_student_uploads_file_to_existing_stage_without_changing_stage_definition(self):
        state = empty_portal_state()
        state["users"] = [{
            "id": "user-1", "role": "student", "nim": "230001", "username": "mahasiswa1",
            "name": "Mahasiswa Uji", "prodi": "Informatika", "active": True,
        }]
        state["projects"] = [{
            "id": "project-docs-1", "title": "Proyek Dokumentasi", "category": "Kompetisi",
            "creatorNim": "230099", "status": "Active", "isGroup": False, "membersNeeded": 3,
            "members": [{"nim": "230001", "name": "Mahasiswa Uji", "approved": True}],
            "applicants": [], "groups": [],
            "milestones": [
                {"key": "stage-1", "name": "Proposal", "desc": "Dokumen proposal", "status": "Belum Dimulai",
                 "fileId": "", "fileName": "", "fileType": "", "fileSize": 0, "submittedAt": "",
                 "note": "", "revisionCount": 0, "verifiedBy": "", "verifiedAt": "", "reviewNote": ""},
                {"key": "stage-2", "name": "Laporan Akhir", "desc": "Dokumen akhir", "status": "Disetujui",
                 "fileId": "verified-file-id", "verifiedBy": "Dosen Uji", "verifiedAt": "2026-10-01", "reviewNote": "Lengkap"},
            ],
        }]
        AppState.objects.create(key="main", data=state, version=1)
        self.client.force_login(self.student)
        upload = SimpleUploadedFile("proposal.pdf", b"%PDF-1.4\nisi", content_type="application/pdf")
        upload_response = self.client.post(
            "/api/documents/upload/",
            {"file": upload, "metadata": json.dumps({
                "purpose": "milestone", "projectId": "project-docs-1", "groupId": None,
                "milestoneKey": "stage-1",
            })},
        )
        self.assertEqual(upload_response.status_code, 200, upload_response.content)
        document_id = upload_response.json()["id"]

        incoming = deepcopy(state)
        incoming_stage = incoming["projects"][0]["milestones"][0]
        incoming_stage.update({
            "name": "Tahap Palsu", "desc": "Deskripsi Palsu", "status": "Menunggu Verifikasi",
            "fileId": document_id, "fileName": "nama-palsu.html", "fileType": "text/html",
            "fileSize": 999999, "submittedAt": "hari ini", "note": "Catatan mahasiswa",
        })
        incoming["projects"][0]["milestones"] = [incoming_stage, {
            "key": "stage-forged", "name": "Tahap tambahan", "status": "Disetujui",
            "verifiedBy": "Mahasiswa Uji",
        }]
        response = self.client.post(
            "/api/state/", data=json.dumps({"state": incoming}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200, response.content)
        stored = AppState.objects.get(key="main").data["projects"][0]["milestones"]
        self.assertEqual(len(stored), 2)
        self.assertEqual(stored[0]["name"], "Proposal")
        self.assertEqual(stored[0]["desc"], "Dokumen proposal")
        self.assertEqual(stored[0]["status"], "Menunggu Verifikasi")
        self.assertEqual(stored[0]["fileName"], "proposal.pdf")
        self.assertEqual(stored[0]["fileType"], "application/pdf")
        self.assertEqual(stored[0]["fileSize"], len(b"%PDF-1.4\nisi"))
        self.assertEqual(stored[0]["note"], "Catatan mahasiswa")
        self.assertEqual(stored[1]["status"], "Disetujui")
        self.assertEqual(stored[1]["verifiedBy"], "Dosen Uji")

    def test_state_snapshot_version_increments(self):
        AppState.objects.create(key="main", data=empty_portal_state(), version=4)
        incoming = empty_portal_state()
        _, version = KreasiStateRepository().save_state(incoming, self.student)
        self.assertEqual(version, 5)
