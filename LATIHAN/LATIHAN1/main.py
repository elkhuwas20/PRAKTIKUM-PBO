"""
KREASI - Sistem Kolaborasi dan Rekam Jejak Mahasiswa Informatika
Dibuat dengan konsep OOP (Object-Oriented Programming)
"""

from datetime import datetime
from abc import ABC, abstractmethod


# ============= PARENT CLASS (ABSTRACT) =============
class User(ABC):
    """Parent class untuk semua pengguna sistem"""
    total_users = 0
    
    def __init__(self, user_id, nama, email):
        self.__user_id = user_id
        self.nama = nama
        self.__email = email
        User.total_users += 1
    
    @property
    def user_id(self):
        return self.__user_id
    
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, value):
        if "@" in value and "." in value:
            self.__email = value
        else:
            print(f"Email '{value}' tidak valid!")
    
    @abstractmethod
    def tampilkan_info(self):
        """Method abstract yang harus diimplementasi oleh child class"""
        pass
    
    def tampilkan_profil(self):
        print(f"ID: {self.__user_id}")
        print(f"Nama: {self.nama}")
        print(f"Email: {self.__email}")


# ============= CHILD CLASS 1: MAHASISWA =============
class Mahasiswa(User):
    """Class untuk mahasiswa dengan portofolio dan prestasi"""
    total_mahasiswa = 0
    
    def __init__(self, user_id, nama, email, nim, prodi):
        super().__init__(user_id, nama, email)
        self.nim = nim
        self.prodi = prodi
        self.__poin = 0
        self.keahlian = []
        self.portofolio = []
        self.prestasi = []
        Mahasiswa.total_mahasiswa += 1
    
    @property
    def poin(self):
        return self.__poin
    
    def tambah_poin(self, jumlah):
        """Menambah poin mahasiswa (Gamifikasi)"""
        if jumlah > 0:
            self.__poin += jumlah
            print(f"✓ Poin bertambah +{jumlah}. Total poin: {self.__poin}")
        else:
            print("Jumlah poin harus positif!")
    
    def tambah_keahlian(self, keahlian):
        """Menambah keahlian mahasiswa"""
        if keahlian not in self.keahlian:
            self.keahlian.append(keahlian)
            print(f"✓ Keahlian '{keahlian}' ditambahkan")
    
    def ajukan_prestasi(self, judul, kategori, bukti):
        """Mengajukan prestasi untuk validasi"""
        prestasi_baru = {
            "judul": judul,
            "kategori": kategori,
            "bukti": bukti,
            "status": "Menunggu Validasi",
            "validator": None
        }
        self.prestasi.append(prestasi_baru)
        print(f"✓ Prestasi '{judul}' diajukan. Status: Menunggu Validasi")
    
    def tampilkan_info(self):
        """Override method abstract dari parent class"""
        print(f"\n{'='*50}")
        print(f"PROFIL MAHASISWA")
        print(f"{'='*50}")
        self.tampilkan_profil()
        print(f"NIM: {self.nim}")
        print(f"Program Studi: {self.prodi}")
        print(f"Poin: {self.__poin}")
        print(f"Keahlian: {', '.join(self.keahlian) if self.keahlian else 'Belum ada'}")
        print(f"Jumlah Prestasi: {len(self.prestasi)}")
    
    def lihat_prestasi(self):
        """Menampilkan semua prestasi mahasiswa"""
        print(f"\n{'='*50}")
        print(f"DAFTAR PRESTASI - {self.nama}")
        print(f"{'='*50}")
        if not self.prestasi:
            print("Belum ada prestasi yang diajukan.")
            return
        
        for i, p in enumerate(self.prestasi, 1):
            print(f"\n{i}. {p['judul']}")
            print(f"   Kategori: {p['kategori']}")
            print(f"   Status: {p['status']}")
            if p['validator']:
                print(f"   Validator: {p['validator']}")


# ============= CHILD CLASS 2: DOSEN =============
class Dosen(User):
    """Class untuk dosen dengan kemampuan validasi"""
    total_dosen = 0
    
    def __init__(self, user_id, nama, email, nip, jurusan):
        super().__init__(user_id, nama, email)
        self.nip = nip
        self.jurusan = jurusan
        self.proyek_dibuat = []
        Dosen.total_dosen += 1
    
    def validasi_prestasi(self, mahasiswa, index_prestasi, status_validasi):
        """Memvalidasi prestasi mahasiswa (approved/rejected)"""
        if 0 <= index_prestasi < len(mahasiswa.prestasi):
            prestasi = mahasiswa.prestasi[index_prestasi]
            if status_validasi.lower() == "approved":
                prestasi["status"] = "Disetujui ✓"
                prestasi["validator"] = self.nama
                mahasiswa.tambah_poin(50)  # Reward poin untuk prestasi tervalidasi
                print(f"\n✓ Prestasi '{prestasi['judul']}' DISETUJUI oleh {self.nama}")
            elif status_validasi.lower() == "rejected":
                prestasi["status"] = "Ditolak ✗"
                prestasi["validator"] = self.nama
                print(f"\n✗ Prestasi '{prestasi['judul']}' DITOLAK oleh {self.nama}")
            else:
                print("Status tidak valid! Gunakan 'approved' atau 'rejected'")
        else:
            print("Index prestasi tidak valid!")
    
    def tampilkan_info(self):
        """Override method abstract dari parent class"""
        print(f"\n{'='*50}")
        print(f"PROFIL DOSEN")
        print(f"{'='*50}")
        self.tampilkan_profil()
        print(f"NIP: {self.nip}")
        print(f"Jurusan: {self.jurusan}")
        print(f"Proyek yang Dibuat: {len(self.proyek_dibuat)}")


# ============= CLASS PROYEK =============
class Proyek:
    """Class untuk mengelola proyek kolaborasi"""
    total_proyek = 0
    
    def __init__(self, id_proyek, nama_proyek, pembuat, deskripsi, max_anggota):
        self.__id_proyek = id_proyek
        self.nama_proyek = nama_proyek
        self.pembuat = pembuat  # Object User (Mahasiswa/Dosen)
        self.deskripsi = deskripsi
        self.max_anggota = max_anggota
        self.anggota = []
        self.pendaftar = []
        self.__status = "Terbuka"
        Proyek.total_proyek += 1
        
        # Tambah proyek ke list pembuat
        if isinstance(pembuat, Dosen):
            pembuat.proyek_dibuat.append(self)
    
    @property
    def id_proyek(self):
        return self.__id_proyek
    
    @property
    def status(self):
        return self.__status
    
    def daftar_proyek(self, mahasiswa):
        """Mahasiswa mendaftar ke proyek"""
        if self.__status != "Terbuka":
            print(f"✗ Proyek '{self.nama_proyek}' sudah ditutup!")
            return
        
        if len(self.anggota) >= self.max_anggota:
            print(f"✗ Proyek '{self.nama_proyek}' sudah penuh!")
            return
        
        if mahasiswa in self.pendaftar:
            print(f"✗ Anda sudah mendaftar di proyek ini!")
            return
        
        self.pendaftar.append(mahasiswa)
        print(f"✓ {mahasiswa.nama} berhasil mendaftar di proyek '{self.nama_proyek}'")
    
    def terima_anggota(self, mahasiswa):
        """Pembuat proyek menerima anggota dari daftar pendaftar"""
        if mahasiswa in self.pendaftar:
            if len(self.anggota) < self.max_anggota:
                self.anggota.append(mahasiswa)
                self.pendaftar.remove(mahasiswa)
                mahasiswa.tambah_poin(30)  # Reward poin untuk diterima di proyek
                print(f"✓ {mahasiswa.nama} diterima sebagai anggota proyek '{self.nama_proyek}'")
                
                if len(self.anggota) >= self.max_anggota:
                    self.__status = "Penuh"
                    print(f"⚠ Proyek '{self.nama_proyek}' sudah penuh dan ditutup!")
            else:
                print(f"✗ Proyek sudah penuh!")
        else:
            print(f"✗ {mahasiswa.nama} belum mendaftar di proyek ini!")
    
    def undang_mahasiswa(self, mahasiswa):
        """Dosen mengundang mahasiswa langsung (tanpa perlu daftar)"""
        if isinstance(self.pembuat, Dosen):
            if len(self.anggota) < self.max_anggota:
                print(f"\n📧 Undangan proyek '{self.nama_proyek}' dikirim ke {mahasiswa.nama}")
                print(f"   Dikirim oleh: {self.pembuat.nama} (Dosen)")
                return True
            else:
                print(f"✗ Proyek sudah penuh!")
                return False
        else:
            print("✗ Hanya dosen yang dapat mengirim undangan!")
            return False
    
    def tampilkan_info(self):
        """Menampilkan informasi proyek"""
        print(f"\n{'='*50}")
        print(f"INFORMASI PROYEK")
        print(f"{'='*50}")
        print(f"ID: {self.__id_proyek}")
        print(f"Nama Proyek: {self.nama_proyek}")
        print(f"Pembuat: {self.pembuat.nama} ({'Dosen' if isinstance(self.pembuat, Dosen) else 'Mahasiswa'})")
        print(f"Deskripsi: {self.deskripsi}")
        print(f"Status: {self.__status}")
        print(f"Anggota: {len(self.anggota)}/{self.max_anggota}")
        
        if self.anggota:
            print(f"\nDaftar Anggota:")
            for i, anggota in enumerate(self.anggota, 1):
                print(f"  {i}. {anggota.nama} ({anggota.nim} - {anggota.prodi})")
        
        if self.pendaftar:
            print(f"\nPendaftar ({len(self.pendaftar)}):")
            for i, pendaftar in enumerate(self.pendaftar, 1):
                print(f"  {i}. {pendaftar.nama} ({pendaftar.nim} - {pendaftar.prodi})")
                print(f"     Keahlian: {', '.join(pendaftar.keahlian) if pendaftar.keahlian else 'Belum ada'}")


# ============= CLASS TALENT POOL =============
class TalentPool:
    """Class untuk mengelola database talenta mahasiswa"""
    def __init__(self):
        self.database = []
    
    def tambah_mahasiswa(self, mahasiswa):
        """Menambah mahasiswa ke talent pool"""
        if mahasiswa not in self.database:
            self.database.append(mahasiswa)
            print(f"✓ {mahasiswa.nama} ditambahkan ke Talent Pool")
    
    def cari_berdasarkan_keahlian(self, keahlian):
        """Mencari mahasiswa berdasarkan keahlian tertentu"""
        hasil = [m for m in self.database if keahlian.lower() in [k.lower() for k in m.keahlian]]
        return hasil
    
    def cari_berdasarkan_prodi(self, prodi):
        """Mencari mahasiswa berdasarkan program studi"""
        hasil = [m for m in self.database if prodi.lower() in m.prodi.lower()]
        return hasil
    
    def tampilkan_semua_talenta(self):
        """Menampilkan semua talenta di database"""
        print(f"\n{'='*50}")
        print(f"DATABASE TALENT POOL")
        print(f"{'='*50}")
        print(f"Total Mahasiswa: {len(self.database)}\n")
        
        if not self.database:
            print("Database masih kosong.")
            return
        
        for i, m in enumerate(self.database, 1):
            print(f"{i}. {m.nama} ({m.nim})")
            print(f"   Prodi: {m.prodi}")
            print(f"   Poin: {m.poin}")
            print(f"   Keahlian: {', '.join(m.keahlian) if m.keahlian else 'Belum ada'}")
            print(f"   Prestasi: {len(m.prestasi)} prestasi")
            print()


# ============= SISTEM KREASI =============
class SistemKREASI:
    """Main class untuk mengelola sistem KREASI"""
    def __init__(self):
        self.users = []
        self.proyek_list = []
        self.talent_pool = TalentPool()
    
    def registrasi_mahasiswa(self, user_id, nama, email, nim, prodi):
        """Registrasi mahasiswa baru"""
        mahasiswa_baru = Mahasiswa(user_id, nama, email, nim, prodi)
        self.users.append(mahasiswa_baru)
        self.talent_pool.tambah_mahasiswa(mahasiswa_baru)
        print(f"\n✓ Mahasiswa {nama} berhasil terdaftar!")
        return mahasiswa_baru
    
    def registrasi_dosen(self, user_id, nama, email, nip, jurusan):
        """Registrasi dosen baru"""
        dosen_baru = Dosen(user_id, nama, email, nip, jurusan)
        self.users.append(dosen_baru)
        print(f"\n✓ Dosen {nama} berhasil terdaftar!")
        return dosen_baru
    
    def buat_proyek(self, id_proyek, nama_proyek, pembuat, deskripsi, max_anggota):
        """Membuat proyek baru"""
        proyek_baru = Proyek(id_proyek, nama_proyek, pembuat, deskripsi, max_anggota)
        self.proyek_list.append(proyek_baru)
        print(f"\n✓ Proyek '{nama_proyek}' berhasil dibuat!")
        return proyek_baru
    
    def tampilkan_semua_proyek(self):
        """Menampilkan bursa proyek"""
        print(f"\n{'='*50}")
        print(f"BURSA PROYEK TERPUSAT")
        print(f"{'='*50}")
        print(f"Total Proyek: {len(self.proyek_list)}\n")
        
        if not self.proyek_list:
            print("Belum ada proyek tersedia.")
            return
        
        for i, p in enumerate(self.proyek_list, 1):
            print(f"{i}. {p.nama_proyek} (ID: {p.id_proyek})")
            print(f"   Pembuat: {p.pembuat.nama}")
            print(f"   Status: {p.status}")
            print(f"   Anggota: {len(p.anggota)}/{p.max_anggota}")
            print(f"   Deskripsi: {p.deskripsi}")
            print()
    
    def statistik_sistem(self):
        """Menampilkan statistik sistem"""
        print(f"\n{'='*50}")
        print(f"STATISTIK SISTEM KREASI")
        print(f"{'='*50}")
        print(f"Total Users: {User.total_users}")
        print(f"Total Mahasiswa: {Mahasiswa.total_mahasiswa}")
        print(f"Total Dosen: {Dosen.total_dosen}")
        print(f"Total Proyek: {Proyek.total_proyek}")
        print(f"Talent Pool: {len(self.talent_pool.database)} mahasiswa")


# ============= MAIN PROGRAM =============
if __name__ == "__main__":
    print("\n" + "="*50)
    print(" SISTEM KREASI ".center(50, "="))
    print(" Kolaborasi & Rekam Jejak Mahasiswa ".center(50))
    print("="*50)
    
    # Inisialisasi sistem
    sistem = SistemKREASI()
    
    # ===== REGISTRASI USERS =====
    print("\n\n### 1. REGISTRASI PENGGUNA ###")
    m1 = sistem.registrasi_mahasiswa("M001", "Budi Santoso", "budi@student.ac.id", "2509106001", "Informatika")
    m2 = sistem.registrasi_mahasiswa("M002", "Siti Aminah", "siti@student.ac.id", "2509106002", "Sistem Informasi")
    m3 = sistem.registrasi_mahasiswa("M003", "Andi Wijaya", "andi@student.ac.id", "2509106003", "Informatika")
    
    d1 = sistem.registrasi_dosen("D001", "Dr. Ahmad Fauzi", "ahmad@lecturer.ac.id", "198501012010", "Informatika")
    d2 = sistem.registrasi_dosen("D002", "Prof. Ratna Sari", "ratna@lecturer.ac.id", "197803052008", "Sistem Informasi")
    
    # ===== MAHASISWA MENAMBAH KEAHLIAN =====
    print("\n\n### 2. MAHASISWA MENAMBAH KEAHLIAN ###")
    m1.tambah_keahlian("Python")
    m1.tambah_keahlian("Machine Learning")
    m1.tambah_keahlian("Data Analysis")
    
    m2.tambah_keahlian("UI/UX Design")
    m2.tambah_keahlian("Figma")
    
    m3.tambah_keahlian("Java")
    m3.tambah_keahlian("Spring Boot")
    
    # ===== MAHASISWA MENGAJUKAN PRESTASI =====
    print("\n\n### 3. MAHASISWA MENGAJUKAN PRESTASI ###")
    m1.ajukan_prestasi(
        "Juara 1 Hackathon Nasional 2024",
        "Lomba",
        "sertifikat_hackathon.pdf"
    )
    m1.ajukan_prestasi(
        "Publikasi Paper di Jurnal Internasional",
        "Penelitian",
        "paper_ijcai2024.pdf"
    )
    
    m2.ajukan_prestasi(
        "Juara 2 UI/UX Competition",
        "Lomba",
        "sertifikat_uiux.pdf"
    )
    
    # ===== DOSEN VALIDASI PRESTASI =====
    print("\n\n### 4. DOSEN MEMVALIDASI PRESTASI ###")
    # Dosen melihat dan memvalidasi prestasi mahasiswa
    m1.lihat_prestasi()
    d1.validasi_prestasi(m1, 0, "approved")  # Validasi prestasi pertama
    d1.validasi_prestasi(m1, 1, "approved")  # Validasi prestasi kedua
    
    m2.lihat_prestasi()
    d2.validasi_prestasi(m2, 0, "approved")
    
    # ===== LIHAT PRESTASI SETELAH VALIDASI =====
    print("\n\n### 5. PRESTASI SETELAH VALIDASI ###")
    m1.lihat_prestasi()
    
    # ===== BUAT PROYEK =====
    print("\n\n### 6. PEMBUATAN PROYEK ###")
    # Proyek dibuat oleh dosen
    p1 = sistem.buat_proyek(
        "PROJ001",
        "Penelitian AI untuk Smart City",
        d1,
        "Penelitian tentang penerapan AI dalam pengembangan smart city",
        3
    )
    
    p2 = sistem.buat_proyek(
        "PROJ002",
        "Pengabdian Masyarakat: Pelatihan Coding",
        d2,
        "Pelatihan coding untuk siswa SMA di daerah terpencil",
        5
    )
    
    # Proyek dibuat oleh mahasiswa
    p3 = sistem.buat_proyek(
        "PROJ003",
        "Tim Lomba GEMASTIK 2024",
        m1,
        "Persiapan lomba GEMASTIK kategori Data Mining",
        4
    )
    
    # ===== TAMPILKAN BURSA PROYEK =====
    print("\n\n### 7. BURSA PROYEK TERPUSAT ###")
    sistem.tampilkan_semua_proyek()
    
    # ===== MAHASISWA MENDAFTAR PROYEK =====
    print("\n\n### 8. MAHASISWA MENDAFTAR PROYEK ###")
    p1.daftar_proyek(m2)  # Siti mendaftar proyek AI
    p1.daftar_proyek(m3)  # Andi mendaftar proyek AI
    
    p3.daftar_proyek(m2)  # Siti mendaftar tim lomba
    p3.daftar_proyek(m3)  # Andi mendaftar tim lomba
    
    # ===== PEMBUAT PROYEK MELIHAT KANDIDAT =====
    print("\n\n### 9. INFORMASI PROYEK & KANDIDAT ###")
    p1.tampilkan_info()
    
    # ===== TALENT POOL: CARI MAHASISWA BERDASARKAN KEAHLIAN =====
    print("\n\n### 10. TALENT POOL - CARI BERDASARKAN KEAHLIAN ###")
    print("\nDosen mencari mahasiswa dengan keahlian 'Python':")
    hasil_python = sistem.talent_pool.cari_berdasarkan_keahlian("Python")
    for m in hasil_python:
        print(f"  - {m.nama} ({m.nim}) | Poin: {m.poin}")
        print(f"    Keahlian: {', '.join(m.keahlian)}")
    
    print("\nDosen mencari mahasiswa dengan keahlian 'UI/UX Design':")
    hasil_uiux = sistem.talent_pool.cari_berdasarkan_keahlian("UI/UX")
    for m in hasil_uiux:
        print(f"  - {m.nama} ({m.nim}) | Poin: {m.poin}")
        print(f"    Keahlian: {', '.join(m.keahlian)}")
    
    # ===== REKRUTMEN: PEMBUAT PROYEK TERIMA ANGGOTA =====
    print("\n\n### 11. REKRUTMEN BERDASARKAN PORTOFOLIO ###")
    print(f"\nDosen {d1.nama} memilih anggota untuk proyek '{p1.nama_proyek}':")
    p1.terima_anggota(m2)  # Terima Siti (punya skill UI/UX)
    p1.terima_anggota(m3)  # Terima Andi (punya skill Java)
    
    print(f"\nMahasiswa {m1.nama} memilih anggota untuk proyek '{p3.nama_proyek}':")
    p3.terima_anggota(m2)  # Terima Siti
    
    # ===== UNDANGAN KOLABORASI (KHUSUS DOSEN) =====
    print("\n\n### 12. UNDANGAN KOLABORASI ###")
    # Dosen mengundang mahasiswa langsung tanpa perlu daftar
    p2.undang_mahasiswa(m1)  # Undang Budi yang punya prestasi bagus
    p2.undang_mahasiswa(m3)  # Undang Andi
    
    # Simulasi: mahasiswa menerima undangan
    print(f"\n{m1.nama} menerima undangan dan bergabung:")
    p2.anggota.append(m1)
    m1.tambah_poin(30)
    
    # ===== CROSS-DEPARTMENT TEAMING =====
    print("\n\n### 13. CROSS-DEPARTMENT TEAMING ###")
    print(f"\nProyek '{p1.nama_proyek}' memiliki anggota lintas prodi:")
    for anggota in p1.anggota:
        print(f"  - {anggota.nama} dari {anggota.prodi}")
    
    # ===== TAMPILKAN PROFIL MAHASISWA =====
    print("\n\n### 14. PROFIL MAHASISWA ###")
    m1.tampilkan_info()
    m2.tampilkan_info()
    
    # ===== TAMPILKAN PROFIL DOSEN =====
    print("\n\n### 15. PROFIL DOSEN ###")
    d1.tampilkan_info()
    
    # ===== TALENT POOL LENGKAP =====
    print("\n\n### 16. DATABASE TALENT POOL ###")
    sistem.talent_pool.tampilkan_semua_talenta()
    
    # ===== KONVERSI POIN (GAMIFIKASI) =====
    print("\n\n### 17. KONVERSI POIN & GAMIFIKASI ###")
    print("Sistem Poin KREASI:")
    print("  - Prestasi divalidasi: +50 poin")
    print("  - Diterima di proyek: +30 poin")
    print("  - Target TAK/SAT: 200 poin")
    print("  - Target Beasiswa: 500 poin")
    
    print(f"\nStatus Poin Mahasiswa:")
    for user in sistem.users:
        if isinstance(user, Mahasiswa):
            status_tak = "✓ Memenuhi" if user.poin >= 200 else "✗ Belum memenuhi"
            status_beasiswa = "✓ Memenuhi" if user.poin >= 500 else "✗ Belum memenuhi"
            print(f"\n  {user.nama}: {user.poin} poin")
            print(f"    TAK/SAT (200 poin): {status_tak}")
            print(f"    Beasiswa (500 poin): {status_beasiswa}")
    
    # ===== OUTPUT SKPI =====
    print("\n\n### 18. OUTPUT SKPI OTOMATIS ###")
    print(f"\nSimulasi SKPI untuk {m1.nama}:")
    print(f"{'='*50}")
    print(f"SURAT KETERANGAN PENDAMPING IJAZAH (SKPI)")
    print(f"{'='*50}")
    print(f"Nama: {m1.nama}")
    print(f"NIM: {m1.nim}")
    print(f"Program Studi: {m1.prodi}")
    print(f"\nPRESTASI & PENCAPAIAN:")
    for i, prestasi in enumerate(m1.prestasi, 1):
        if "Disetujui" in prestasi['status']:
            print(f"{i}. {prestasi['judul']} ({prestasi['kategori']})")
    
    print(f"\nKOMPETENSI & KEAHLIAN:")
    for i, skill in enumerate(m1.keahlian, 1):
        print(f"{i}. {skill}")
    
    print(f"\nTOTAL POIN AKTIVITAS: {m1.poin}")
    
    # ===== STATISTIK SISTEM =====
    print("\n\n### 19. STATISTIK SISTEM ###")
    sistem.statistik_sistem()
    
    # ===== TESTING POLYMORPHISM =====
    print("\n\n### 20. DEMONSTRASI POLYMORPHISM ###")
    print("\nMenampilkan info semua users (Polymorphism):")
    print("Method tampilkan_info() berperilaku berbeda untuk Mahasiswa dan Dosen")
    
    for user in sistem.users[:3]:  # Tampilkan 3 user pertama
        user.tampilkan_info()
    
    print("\n" + "="*50)
    print(" SISTEM KREASI BERJALAN SUKSES ".center(50, "="))
    print("="*50 + "\n")
