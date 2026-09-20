# Panduan Penggunaan Sistem KREASI

## 🎯 Overview

Sistem KREASI adalah platform akademik untuk kolaborasi mahasiswa-dosen yang menerapkan konsep OOP lengkap (Abstraction, Inheritance, Encapsulation, Polymorphism).

---

## 📁 File-file dalam Project

```
LATIHAN/
├── main.py                  # File program utama
├── README_KREASI.md         # Dokumentasi lengkap
└── CARA_PENGGUNAAN.md       # File ini (panduan penggunaan)
```

---

## 🚀 Cara Menjalankan

### 1. Pastikan Python Terinstall
```bash
python --version
# Minimal Python 3.6
```

### 2. Jalankan Program
```bash
cd "PRAKTIKUM PBO/LATIHAN"
python main.py
```

### 3. Program Akan Menampilkan Demo Lengkap
Program sudah dilengkapi dengan skenario demo otomatis yang menampilkan semua fitur sistem.

---

## 📚 Struktur Program

### Class Hierarchy

```
User (Abstract)
├── Mahasiswa
└── Dosen

Proyek (Independent)
TalentPool (Independent)
SistemKREASI (Main System)
```

---

## 💻 Contoh Penggunaan Manual

Jika ingin menggunakan sistem secara manual, berikut adalah contoh-contoh kode:

### 1. Inisialisasi Sistem
```python
from main import SistemKREASI, Mahasiswa, Dosen, Proyek

# Buat instance sistem
sistem = SistemKREASI()
```

### 2. Registrasi User

**Registrasi Mahasiswa:**
```python
mahasiswa = sistem.registrasi_mahasiswa(
    user_id="M001",
    nama="John Doe",
    email="john@student.ac.id",
    nim="2509106001",
    prodi="Informatika"
)
```

**Registrasi Dosen:**
```python
dosen = sistem.registrasi_dosen(
    user_id="D001",
    nama="Dr. Jane Smith",
    email="jane@lecturer.ac.id",
    nip="198501012010",
    jurusan="Informatika"
)
```

### 3. Mahasiswa Menambah Keahlian
```python
mahasiswa.tambah_keahlian("Python")
mahasiswa.tambah_keahlian("Machine Learning")
mahasiswa.tambah_keahlian("Web Development")
```

### 4. Mahasiswa Mengajukan Prestasi
```python
mahasiswa.ajukan_prestasi(
    judul="Juara 1 Hackathon Nasional 2024",
    kategori="Lomba",
    bukti="sertifikat_hackathon.pdf"
)
```

### 5. Dosen Memvalidasi Prestasi
```python
# Lihat prestasi mahasiswa
mahasiswa.lihat_prestasi()

# Validasi prestasi (index dimulai dari 0)
dosen.validasi_prestasi(
    mahasiswa=mahasiswa,
    index_prestasi=0,
    status_validasi="approved"  # atau "rejected"
)
# Mahasiswa otomatis mendapat +50 poin jika approved
```

### 6. Membuat Proyek

**Proyek oleh Dosen:**
```python
proyek = sistem.buat_proyek(
    id_proyek="PROJ001",
    nama_proyek="Penelitian AI untuk Healthcare",
    pembuat=dosen,
    deskripsi="Penelitian penerapan AI di bidang kesehatan",
    max_anggota=5
)
```

**Proyek oleh Mahasiswa:**
```python
proyek_lomba = sistem.buat_proyek(
    id_proyek="PROJ002",
    nama_proyek="Tim Lomba ICPC 2024",
    pembuat=mahasiswa,
    deskripsi="Tim untuk mengikuti lomba programming ICPC",
    max_anggota=3
)
```

### 7. Mahasiswa Mendaftar Proyek
```python
proyek.daftar_proyek(mahasiswa)
```

### 8. Lihat Kandidat Pendaftar
```python
proyek.tampilkan_info()
# Menampilkan info proyek + daftar pendaftar + keahlian mereka
```

### 9. Pembuat Proyek Menerima Anggota
```python
# Terima mahasiswa dari daftar pendaftar
proyek.terima_anggota(mahasiswa)
# Mahasiswa otomatis mendapat +30 poin
```

### 10. Dosen Mengundang Mahasiswa
```python
# Hanya dosen yang bisa mengundang langsung
proyek.undang_mahasiswa(mahasiswa)
```

### 11. Cari Mahasiswa di Talent Pool

**Berdasarkan Keahlian:**
```python
hasil = sistem.talent_pool.cari_berdasarkan_keahlian("Python")
for mhs in hasil:
    print(f"{mhs.nama} - Poin: {mhs.poin}")
```

**Berdasarkan Program Studi:**
```python
hasil = sistem.talent_pool.cari_berdasarkan_prodi("Informatika")
for mhs in hasil:
    print(f"{mhs.nama} ({mhs.nim})")
```

### 12. Tampilkan Informasi

**Profil Mahasiswa:**
```python
mahasiswa.tampilkan_info()
```

**Profil Dosen:**
```python
dosen.tampilkan_info()
```

**Info Proyek:**
```python
proyek.tampilkan_info()
```

**Bursa Proyek:**
```python
sistem.tampilkan_semua_proyek()
```

**Talent Pool:**
```python
sistem.talent_pool.tampilkan_semua_talenta()
```

**Statistik Sistem:**
```python
sistem.statistik_sistem()
```

---

## 🎮 Sistem Poin (Gamifikasi)

### Cara Mendapat Poin:

| Aktivitas | Poin |
|-----------|------|
| Prestasi divalidasi (approved) | +50 |
| Diterima sebagai anggota proyek | +30 |
| Menerima undangan proyek | +30 |

### Target Poin:

| Target | Minimal Poin |
|--------|--------------|
| TAK/SAT | 200 |
| Persyaratan Beasiswa | 500 |

### Cara Cek Poin:
```python
print(f"Poin {mahasiswa.nama}: {mahasiswa.poin}")
```

---

## 🔐 Akses dan Keamanan (Encapsulation)

### Atribut Private (Tidak Bisa Diakses Langsung)

```python
# ❌ SALAH - Tidak bisa diakses langsung
print(mahasiswa.__poin)  # Error!
print(dosen.__email)     # Error!

# ✅ BENAR - Akses via property
print(mahasiswa.poin)    # Menggunakan getter
print(dosen.email)       # Menggunakan getter
```

### Validasi Otomatis

```python
# Email otomatis divalidasi
mahasiswa.email = "emailtanpa@"  # Ditolak karena tidak valid
mahasiswa.email = "valid@student.ac.id"  # Diterima

# Poin hanya bisa ditambah (tidak bisa dikurangi atau diset manual)
mahasiswa.tambah_poin(50)  # ✅ Benar
# mahasiswa.poin = 1000     # ❌ Error - tidak ada setter
```

---

## 🎭 Polymorphism dalam Action

```python
# Satu method, berbagai implementasi
for user in sistem.users:
    user.tampilkan_info()  
    # Jika Mahasiswa: tampilkan NIM, Prodi, Poin, Keahlian
    # Jika Dosen: tampilkan NIP, Jurusan, Proyek
```

---

## 🌳 Inheritance (Pewarisan)

```python
# Mahasiswa dan Dosen mewarisi dari User
mahasiswa.tampilkan_profil()  # Method dari parent (User)
dosen.tampilkan_profil()      # Method dari parent (User)

# Tapi punya method khusus sendiri
mahasiswa.ajukan_prestasi(...)  # Hanya Mahasiswa
dosen.validasi_prestasi(...)    # Hanya Dosen
```

---

## 📋 Checklist Fitur

- [x] Manajemen Peran Kolaboratif (Mahasiswa & Dosen)
- [x] Katalog Talenta Terintegrasi (Talent Pool)
- [x] Validasi Pencapaian (Approval System)
- [x] Bursa Proyek Terpusat
- [x] Rekrutmen Berdasarkan Portofolio
- [x] Undangan Kolaborasi (Dosen)
- [x] Konversi Poin (Gamifikasi)
- [x] Cross-Department Teaming
- [x] Output SKPI Otomatis

---

## 🔧 Troubleshooting

### Error: "can't instantiate abstract class User"
**Penyebab:** Mencoba membuat instance dari abstract class User  
**Solusi:** Gunakan child class (Mahasiswa atau Dosen)
```python
# ❌ SALAH
user = User("U001", "John", "john@mail.com")

# ✅ BENAR
mahasiswa = Mahasiswa("M001", "John", "john@mail.com", "2509106001", "Informatika")
```

### Error: "AttributeError: can't set attribute"
**Penyebab:** Mencoba mengubah atribut yang tidak punya setter  
**Solusi:** Gunakan method yang disediakan
```python
# ❌ SALAH
mahasiswa.poin = 100

# ✅ BENAR
mahasiswa.tambah_poin(100)
```

---

## 💡 Tips Penggunaan

1. **Registrasi User Terlebih Dahulu**
   - Buat mahasiswa dan dosen sebelum membuat proyek
   
2. **Gunakan Talent Pool untuk Rekrutmen**
   - Cari mahasiswa berdasarkan keahlian sebelum menerima anggota
   
3. **Validasi Prestasi Sesegera Mungkin**
   - Dosen sebaiknya segera memvalidasi prestasi agar mahasiswa mendapat poin
   
4. **Manfaatkan Cross-Department**
   - Tambahkan mahasiswa dari berbagai prodi untuk kolaborasi lebih kaya
   
5. **Monitor Sistem Poin**
   - Cek poin mahasiswa secara berkala untuk memastikan target tercapai

---

## 📞 Informasi Tambahan

Untuk dokumentasi lengkap tentang konsep OOP yang diterapkan, struktur class, dan penjelasan detail, silakan baca file **README_KREASI.md**.

---

## ✅ Kesimpulan

Sistem KREASI berhasil mengimplementasikan semua pilar OOP dengan fitur-fitur lengkap untuk kolaborasi akademik. Program siap digunakan dan dapat dikembangkan lebih lanjut dengan database dan web interface.
