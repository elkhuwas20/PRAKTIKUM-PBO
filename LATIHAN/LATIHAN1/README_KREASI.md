# KREASI - Sistem Kolaborasi dan Rekam Jejak Mahasiswa Informatika

## 📋 Deskripsi Program

**KREASI** adalah platform akademik yang mendukung kolaborasi antara mahasiswa dan dosen. Sistem ini digunakan untuk menyimpan dan memvalidasi portofolio mahasiswa, sekaligus membantu mahasiswa mencari rekan tim maupun dosen mencari mahasiswa yang sesuai untuk berbagai proyek seperti lomba, seminar, penelitian, pengabdian masyarakat, dan asisten laboratorium.

Program ini dibangun menggunakan Python dengan konsep **Object-Oriented Programming (OOP)** yang menerapkan:
- **Inheritance** (Pewarisan)
- **Encapsulation** (Enkapsulasi)
- **Polymorphism** (Polimorfisme)
- **Abstraction** (Abstraksi)

---

## 🎯 Fitur-Fitur Utama

### A. Manajemen Peran Kolaboratif
Sistem mengatur hak akses berdasarkan peran pengguna. Mahasiswa dapat membuat dan mendaftar proyek, sedangkan dosen dapat membuat proyek akademik serta melakukan validasi data mahasiswa.

### B. Katalog Talenta Terintegrasi (Talent Pool)
Sistem menyimpan profil, keahlian, pengalaman, portofolio, prestasi, dan nilai akademik mahasiswa dalam satu database talenta. Data dapat dikelola dan diperbarui oleh mahasiswa sebagai informasi profil mereka.

### C. Validasi Pencapaian
Sistem menyediakan alur pengajuan dan pemeriksaan prestasi mahasiswa. Mahasiswa mengajukan data prestasi beserta bukti pendukung, kemudian dosen memeriksa dan memberikan status disetujui atau ditolak.

### D. Bursa Proyek Terpusat
Sistem menyediakan satu tempat untuk menampilkan seluruh proyek yang tersedia. Proyek dapat dibuat oleh mahasiswa maupun dosen dan memuat informasi seperti nama proyek, deskripsi, periode, jumlah anggota, serta persyaratan pendaftaran.

### E. Rekrutmen Berdasarkan Portofolio
Sistem menampilkan informasi kandidat yang mendaftar kepada pembuat proyek. Pembuat proyek dapat menggunakan data portofolio dan informasi profil sebagai bahan pertimbangan dalam menentukan anggota proyek.

### F. Undangan Kolaborasi
Sistem memungkinkan pembuat proyek, khususnya dosen, mengirim undangan bergabung kepada mahasiswa tertentu. Mahasiswa dapat menerima atau menolak undangan tersebut melalui sistem.

### G. Konversi Poin (Gamifikasi)
Sistem memberikan poin berdasarkan aktivitas atau pencapaian mahasiswa. Jumlah poin dapat digunakan untuk memantau pemenuhan target aktivitas, seperti TAK/SAT, persyaratan kelulusan, atau persyaratan beasiswa.

### H. Cross-Department Teaming
Sistem memungkinkan satu proyek atau prestasi memiliki beberapa anggota dari program studi atau departemen yang berbeda. Setiap anggota tercatat dalam proyek yang sama sehingga kolaborasi lintas program studi dapat terdokumentasi dengan baik.

### I. Output SKPI Otomatis
Sistem mengumpulkan seluruh rekam aktivitas mahasiswa yang telah tercatat dan tervalidasi selama masa studi, kemudian menyusunnya menjadi data yang dapat digunakan untuk menghasilkan SKPI secara otomatis.

---

## 🏗️ Penerapan Konsep OOP

### 1. Abstraction (Abstract Class)

Program menggunakan **Abstract Base Class (ABC)** untuk mendefinisikan blueprint user:

```python
from abc import ABC, abstractmethod

class User(ABC):
    """Parent class abstract untuk semua pengguna"""
    total_users = 0
    
    def __init__(self, user_id, nama, email):
        self.__user_id = user_id
        self.nama = nama
        self.__email = email
        User.total_users += 1
    
    @abstractmethod
    def tampilkan_info(self):
        """Method abstract yang HARUS diimplementasi oleh child class"""
        pass
```

**Penjelasan:**
- `User` adalah abstract class yang tidak bisa diinstansiasi langsung
- Method `tampilkan_info()` adalah abstract method yang wajib dioverride oleh child class
- Ini memastikan setiap tipe user (Mahasiswa, Dosen) memiliki implementasi `tampilkan_info()` sendiri

---

### 2. Inheritance (Pewarisan)

Program menerapkan inheritance dengan struktur:

```
       User (Abstract Parent Class)
         |
    _____|_____
   |           |
Mahasiswa    Dosen
(Child)      (Child)
```

#### Child Class 1: Mahasiswa
```python
class Mahasiswa(User):
    total_mahasiswa = 0
    
    def __init__(self, user_id, nama, email, nim, prodi):
        super().__init__(user_id, nama, email)  # Memanggil constructor parent
        self.nim = nim
        self.prodi = prodi
        self.__poin = 0
        self.keahlian = []
        self.portofolio = []
        self.prestasi = []
        Mahasiswa.total_mahasiswa += 1
```

**Atribut Tambahan Mahasiswa:**
- `nim`: Nomor Induk Mahasiswa
- `prodi`: Program Studi
- `__poin`: Poin gamifikasi (private)
- `keahlian`: List keahlian mahasiswa
- `portofolio`: List portofolio
- `prestasi`: List prestasi yang diajukan

**Method Khusus Mahasiswa:**
- `tambah_poin()`: Menambah poin mahasiswa
- `tambah_keahlian()`: Menambah keahlian ke profil
- `ajukan_prestasi()`: Mengajukan prestasi untuk validasi
- `lihat_prestasi()`: Menampilkan semua prestasi

#### Child Class 2: Dosen
```python
class Dosen(User):
    total_dosen = 0
    
    def __init__(self, user_id, nama, email, nip, jurusan):
        super().__init__(user_id, nama, email)  # Memanggil constructor parent
        self.nip = nip
        self.jurusan = jurusan
        self.proyek_dibuat = []
        Dosen.total_dosen += 1
```

**Atribut Tambahan Dosen:**
- `nip`: Nomor Induk Pegawai
- `jurusan`: Jurusan dosen
- `proyek_dibuat`: List proyek yang dibuat dosen

**Method Khusus Dosen:**
- `validasi_prestasi()`: Memvalidasi prestasi mahasiswa (approved/rejected)

**Keuntungan Inheritance:**
- Code reusability: atribut `user_id`, `nama`, `email` tidak perlu ditulis ulang
- Mahasiswa dan Dosen mewarisi method `tampilkan_profil()` dari parent
- Setiap child class dapat menambah atribut dan method khususnya sendiri

---

### 3. Encapsulation (Enkapsulasi)

Program menerapkan encapsulation dengan menggunakan **private attributes** dan **property decorator**:

#### a) Private Attributes (Name Mangling)

Atribut sensitif dibuat private menggunakan double underscore (`__`):

**Class User:**
```python
self.__user_id = user_id    # Private - tidak bisa diakses langsung
self.__email = email        # Private - harus via property
```

**Class Mahasiswa:**
```python
self.__poin = 0            # Private - poin tidak bisa diubah sembarangan
```

**Class Proyek:**
```python
self.__id_proyek = id_proyek    # Private - ID tidak boleh diubah
self.__status = "Terbuka"       # Private - status dikelola sistem
```

#### b) Property Decorator (@property)

Property digunakan untuk mengakses dan memodifikasi private attributes dengan controlled manner:

**Getter Property:**
```python
@property
def email(self):
    return self.__email

@property
def poin(self):
    return self.__poin

@property
def status(self):
    return self.__status
```

**Setter Property dengan Validasi:**
```python
@email.setter
def email(self, value):
    if "@" in value and "." in value:
        self.__email = value
    else:
        print(f"Email '{value}' tidak valid!")
```

**Keuntungan Encapsulation:**
- Data sensitif dilindungi dari akses langsung
- Validasi otomatis saat data diubah
- Mencegah perubahan yang tidak valid
- Kontrol penuh terhadap bagaimana data diakses dan dimodifikasi

---

### 4. Polymorphism (Polimorfisme)

Polymorphism diterapkan melalui **method overriding** pada method abstract:

#### Method `tampilkan_info()` - Berbeda untuk setiap class

**Implementasi di Class Mahasiswa:**
```python
def tampilkan_info(self):
    """Override method dari parent class"""
    print(f"\n{'='*50}")
    print(f"PROFIL MAHASISWA")
    print(f"{'='*50}")
    self.tampilkan_profil()
    print(f"NIM: {self.nim}")
    print(f"Program Studi: {self.prodi}")
    print(f"Poin: {self.__poin}")
    print(f"Keahlian: {', '.join(self.keahlian) if self.keahlian else 'Belum ada'}")
    print(f"Jumlah Prestasi: {len(self.prestasi)}")
```

**Implementasi di Class Dosen:**
```python
def tampilkan_info(self):
    """Override method dari parent class"""
    print(f"\n{'='*50}")
    print(f"PROFIL DOSEN")
    print(f"{'='*50}")
    self.tampilkan_profil()
    print(f"NIP: {self.nip}")
    print(f"Jurusan: {self.jurusan}")
    print(f"Proyek yang Dibuat: {len(self.proyek_dibuat)}")
```

**Penggunaan Polymorphism:**
```python
# Satu method, berbagai perilaku tergantung tipe object
for user in sistem.users:
    user.tampilkan_info()  # Akan memanggil versi Mahasiswa atau Dosen
```

**Keuntungan Polymorphism:**
- Satu interface, banyak implementasi
- Code lebih fleksibel dan mudah diperluas
- Tidak perlu cek tipe object secara manual (instanceof)

---

## 📦 Struktur Class

### 1. Class User (Abstract Parent)

**Atribut Class:**
- `total_users`: Counter total user (integer)

**Atribut Instance:**
- `__user_id`: ID user (private)
- `nama`: Nama user (public)
- `__email`: Email user (private)

**Method:**
- `__init__(user_id, nama, email)`: Constructor
- `@property user_id`: Getter untuk user_id
- `@property email`: Getter untuk email
- `@email.setter`: Setter dengan validasi format email
- `@abstractmethod tampilkan_info()`: Abstract method (harus dioverride)
- `tampilkan_profil()`: Menampilkan info dasar user

---

### 2. Class Mahasiswa (extends User)

**Atribut Class:**
- `total_mahasiswa`: Counter total mahasiswa (integer)

**Atribut Instance:**
- `nim`: Nomor Induk Mahasiswa (public)
- `prodi`: Program Studi (public)
- `__poin`: Poin gamifikasi (private)
- `keahlian`: List keahlian (public)
- `portofolio`: List portofolio (public)
- `prestasi`: List prestasi (public)

**Method:**
- `__init__(user_id, nama, email, nim, prodi)`: Constructor
- `@property poin`: Getter untuk poin
- `tambah_poin(jumlah)`: Menambah poin mahasiswa
- `tambah_keahlian(keahlian)`: Menambah keahlian
- `ajukan_prestasi(judul, kategori, bukti)`: Mengajukan prestasi
- `tampilkan_info()`: Override - menampilkan profil mahasiswa
- `lihat_prestasi()`: Menampilkan semua prestasi

---

### 3. Class Dosen (extends User)

**Atribut Class:**
- `total_dosen`: Counter total dosen (integer)

**Atribut Instance:**
- `nip`: Nomor Induk Pegawai (public)
- `jurusan`: Jurusan dosen (public)
- `proyek_dibuat`: List proyek yang dibuat (public)

**Method:**
- `__init__(user_id, nama, email, nip, jurusan)`: Constructor
- `validasi_prestasi(mahasiswa, index, status)`: Validasi prestasi mahasiswa
- `tampilkan_info()`: Override - menampilkan profil dosen

---

### 4. Class Proyek

**Atribut Class:**
- `total_proyek`: Counter total proyek (integer)

**Atribut Instance:**
- `__id_proyek`: ID proyek (private)
- `nama_proyek`: Nama proyek (public)
- `pembuat`: Object User yang membuat proyek (public)
- `deskripsi`: Deskripsi proyek (public)
- `max_anggota`: Maksimal anggota (public)
- `anggota`: List anggota yang diterima (public)
- `pendaftar`: List mahasiswa yang mendaftar (public)
- `__status`: Status proyek (private)

**Method:**
- `__init__(id_proyek, nama_proyek, pembuat, deskripsi, max_anggota)`: Constructor
- `@property id_proyek`: Getter untuk ID proyek
- `@property status`: Getter untuk status proyek
- `daftar_proyek(mahasiswa)`: Mahasiswa mendaftar proyek
- `terima_anggota(mahasiswa)`: Pembuat terima anggota dari pendaftar
- `undang_mahasiswa(mahasiswa)`: Dosen mengundang mahasiswa
- `tampilkan_info()`: Menampilkan info proyek dan kandidat

---

### 5. Class TalentPool

**Atribut Instance:**
- `database`: List mahasiswa dalam talent pool

**Method:**
- `tambah_mahasiswa(mahasiswa)`: Menambah mahasiswa ke database
- `cari_berdasarkan_keahlian(keahlian)`: Search mahasiswa by skill
- `cari_berdasarkan_prodi(prodi)`: Search mahasiswa by prodi
- `tampilkan_semua_talenta()`: Menampilkan semua talenta

---

### 6. Class SistemKREASI

**Atribut Instance:**
- `users`: List semua user (mahasiswa + dosen)
- `proyek_list`: List semua proyek
- `talent_pool`: Object TalentPool

**Method:**
- `registrasi_mahasiswa(...)`: Registrasi mahasiswa baru
- `registrasi_dosen(...)`: Registrasi dosen baru
- `buat_proyek(...)`: Membuat proyek baru
- `tampilkan_semua_proyek()`: Menampilkan bursa proyek
- `statistik_sistem()`: Menampilkan statistik sistem

---

## 🔄 Alur Program

### 1. Registrasi Pengguna
```python
# Registrasi Mahasiswa
m1 = sistem.registrasi_mahasiswa("M001", "Budi Santoso", "budi@student.ac.id", "2509106001", "Informatika")

# Registrasi Dosen
d1 = sistem.registrasi_dosen("D001", "Dr. Ahmad Fauzi", "ahmad@lecturer.ac.id", "198501012010", "Informatika")
```

### 2. Mahasiswa Menambah Keahlian
```python
m1.tambah_keahlian("Python")
m1.tambah_keahlian("Machine Learning")
m1.tambah_keahlian("Data Analysis")
```

### 3. Mahasiswa Mengajukan Prestasi
```python
m1.ajukan_prestasi(
    "Juara 1 Hackathon Nasional 2024",
    "Lomba",
    "sertifikat_hackathon.pdf"
)
```

### 4. Dosen Memvalidasi Prestasi
```python
# Dosen melihat prestasi mahasiswa
m1.lihat_prestasi()

# Dosen memvalidasi (approved/rejected)
d1.validasi_prestasi(m1, 0, "approved")
# Mahasiswa otomatis dapat +50 poin
```

### 5. Pembuatan Proyek
```python
# Dosen membuat proyek penelitian
p1 = sistem.buat_proyek(
    "PROJ001",
    "Penelitian AI untuk Smart City",
    d1,
    "Penelitian tentang penerapan AI dalam pengembangan smart city",
    3
)

# Mahasiswa membuat tim lomba
p3 = sistem.buat_proyek(
    "PROJ003",
    "Tim Lomba GEMASTIK 2024",
    m1,
    "Persiapan lomba GEMASTIK kategori Data Mining",
    4
)
```

### 6. Bursa Proyek Terpusat
```python
# Menampilkan semua proyek yang tersedia
sistem.tampilkan_semua_proyek()
```

### 7. Mahasiswa Mendaftar Proyek
```python
p1.daftar_proyek(m2)  # Siti mendaftar proyek AI
p1.daftar_proyek(m3)  # Andi mendaftar proyek AI
```

### 8. Rekrutmen Berdasarkan Portofolio
```python
# Pembuat proyek melihat kandidat dan portofolionya
p1.tampilkan_info()  # Menampilkan info proyek + daftar pendaftar + keahlian mereka

# Dosen mencari mahasiswa dengan keahlian tertentu via Talent Pool
hasil = sistem.talent_pool.cari_berdasarkan_keahlian("Python")
```

### 9. Pembuat Proyek Menerima Anggota
```python
# Dosen menerima anggota berdasarkan portofolio
p1.terima_anggota(m2)  # Terima Siti
p1.terima_anggota(m3)  # Terima Andi
# Mahasiswa otomatis dapat +30 poin
```

### 10. Undangan Kolaborasi (Khusus Dosen)
```python
# Dosen mengundang mahasiswa langsung tanpa perlu daftar
p2.undang_mahasiswa(m1)  # Undang Budi

# Mahasiswa menerima undangan
p2.anggota.append(m1)
m1.tambah_poin(30)
```

### 11. Cross-Department Teaming
```python
# Proyek dapat memiliki anggota dari berbagai prodi
for anggota in p1.anggota:
    print(f"{anggota.nama} dari {anggota.prodi}")
# Output:
# Siti Aminah dari Sistem Informasi
# Andi Wijaya dari Informatika
```

### 12. Konversi Poin (Gamifikasi)
```python
# Sistem otomatis memberikan poin:
# - Prestasi divalidasi: +50 poin
# - Diterima di proyek: +30 poin

# Poin digunakan untuk target:
# - TAK/SAT: 200 poin
# - Beasiswa: 500 poin
```

### 13. Output SKPI Otomatis
```python
# Sistem mengumpulkan semua aktivitas tervalidasi mahasiswa
# dan menyusunnya menjadi format SKPI
```

---

## 🚀 Cara Menjalankan Program

### Persyaratan:
- Python 3.6 atau lebih baru

### Langkah-langkah:
1. Pastikan Python sudah terinstall di sistem
2. Buka terminal/command prompt
3. Navigasi ke direktori file program
4. Jalankan perintah:
   ```bash
   python main.py
   ```

---

## 📊 Sistem Poin (Gamifikasi)

| Aktivitas | Poin |
|-----------|------|
| Prestasi Divalidasi | +50 |
| Diterima di Proyek | +30 |

| Target | Minimal Poin |
|--------|--------------|
| TAK/SAT | 200 |
| Persyaratan Beasiswa | 500 |

---

## 💡 Keunggulan Sistem KREASI

✅ **Manajemen Peran Berbasis OOP** - Inheritance memisahkan peran Mahasiswa dan Dosen  
✅ **Keamanan Data** - Encapsulation melindungi data sensitif dengan private attributes  
✅ **Fleksibilitas** - Polymorphism memungkinkan satu interface untuk berbagai implementasi  
✅ **Talent Pool Terintegrasi** - Database talenta mahasiswa yang mudah dicari  
✅ **Validasi Prestasi** - Sistem approval dari dosen dengan reward poin otomatis  
✅ **Bursa Proyek Terpusat** - Satu tempat untuk semua proyek (mahasiswa & dosen)  
✅ **Rekrutmen Berbasis Portofolio** - Keputusan berdasarkan keahlian dan prestasi  
✅ **Undangan Kolaborasi** - Dosen dapat mengundang mahasiswa langsung  
✅ **Gamifikasi** - Sistem poin untuk memotivasi mahasiswa  
✅ **Cross-Department** - Kolaborasi lintas prodi terdokumentasi  
✅ **SKPI Otomatis** - Generate SKPI dari data tervalidasi  

---

## 🔮 Pengembangan Lebih Lanjut

Program ini dapat dikembangkan dengan:
- **Database Integration** (PostgreSQL/MySQL) untuk penyimpanan permanen
- **Web Framework** (Django/Flask) untuk interface web
- **Authentication System** (JWT) untuk keamanan login
- **Notification System** (Email/Push) untuk notifikasi real-time
- **File Upload** untuk portofolio dan bukti prestasi
- **Analytics Dashboard** untuk visualisasi data
- **Export SKPI to PDF** menggunakan library ReportLab
- **REST API** untuk integrasi dengan sistem lain

---

## 📚 Referensi

- **UI/UX Design**: Dribbble, Figma, Behance, Mobbin
- **Sistem Referensi**:
  - Telkom University (iGracias): https://igracias.telkomuniversity.ac.id/
  - Bina Nusantara University (BINUSmaya): https://binusmaya.binus.ac.id/
  - Institut Teknologi Sepuluh Nopember (myITS): https://my.its.ac.id/
  - Universitas Gadjah Mada (SIMASTER): https://simaster.ugm.ac.id/

---

## 👨‍💻 Kesimpulan

Sistem KREASI berhasil menerapkan 4 pilar OOP (Abstraction, Inheritance, Encapsulation, Polymorphism) dalam platform akademik yang lengkap. Program ini menyediakan solusi terintegrasi untuk kolaborasi mahasiswa-dosen, manajemen portofolio, validasi prestasi, dan rekrutmen berbasis kompetensi.
