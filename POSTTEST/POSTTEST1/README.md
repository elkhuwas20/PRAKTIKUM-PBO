# LAPORAN POSTTEST 1

Proyek ini adalah sistem aplikasi manajemen bengkel motor menggunakan bahasa Python dengan konsep Object Oriented Programming (OOP).

## Identitas

**Nama**: Nuril Akmal  
**NIM**: 2509106074

---

## Deskripsi Program

Program ini merupakan sistem manajemen bengkel motor yang dibuat menggunakan bahasa pemrograman Python dengan menerapkan konsep Object-Oriented Programming (OOP). Program ini dirancang untuk mengelola data pelanggan, kendaraan, dan layanan servis bengkel "Bengkel Mas Ambasukiii".

### Fitur Utama:

- Terdapat 3 class utama: `Pelanggan`, `Kendaraan`, dan `Servis`
- Menggunakan relasi antar class (composition): Pelanggan memiliki Kendaraan, Kendaraan memiliki Servis
- Setiap pelanggan memiliki data: nama dan nomor HP
- Setiap kendaraan memiliki data: pemilik, plat nomor, dan tipe kendaraan
- Setiap servis memiliki data: kendaraan, keluhan, dan biaya
- Nomor HP harus diawali dengan "08" dan hanya berisi angka
- Plat nomor otomatis dikonversi ke huruf kapital (uppercase)
- Biaya servis tidak boleh bernilai negatif
- Terdapat class variable untuk menghitung total pelanggan, kendaraan, dan servis
- Dapat membuat object dari dictionary menggunakan class method
- Validasi data menggunakan static method

---

## Penerapan Konsep OOP

### 1. Encapsulation (Enkapsulasi)

Program ini menerapkan Encapsulation dengan menggunakan atribut private dan property:

#### a) Atribut Private (Name Mangling)

Atribut sensitif dalam setiap class dibuat private menggunakan double underscore:

**Class Pelanggan:**
```python
self.__no_hp = None  # Nomor HP pelanggan (private)
```

**Class Kendaraan:**
```python
self.__plat_nomor = None  # Plat nomor kendaraan (private)
```

**Class Servis:**
```python
self.__biaya = 0  # Biaya servis (private)
```

Dengan menjadikan atribut private, data hanya dapat diakses melalui property getter dan setter. Ini melindungi integritas data dan memungkinkan validasi sebelum penyimpanan.

#### b) Property Decorator (@property)

Property digunakan untuk mengakses atribut private dengan cara yang controlled:

**Getter Property:**
```python
# Class Pelanggan
@property
def no_hp(self):
    return self.__no_hp

# Class Kendaraan
@property
def plat_nomor(self):
    return self.__plat_nomor

# Class Servis
@property
def biaya(self):
    return self.__biaya
```

**Setter Property dengan Validasi:**
```python
# Class Pelanggan - Validasi format nomor HP
@no_hp.setter
def no_hp(self, value):
    if Pelanggan.cek_format_hp(value):
        self.__no_hp = value
    else:
        print(f"Gagal! No HP '{value}' tidak valid")

# Class Kendaraan - Auto-convert ke uppercase
@plat_nomor.setter
def plat_nomor(self, value):
    if Kendaraan.cek_format_plat(value):
        self.__plat_nomor = value.upper()
    else:
        print(f"Gagal! Plat nomor '{value}' tidak valid")

# Class Servis - Validasi tidak boleh negatif
@biaya.setter
def biaya(self, value):
    if value >= 0:
        self.__biaya = value
    else:
        print("Gagal! Biaya tidak boleh negatif")
```

#### c) Atribut Public

Atribut yang tidak sensitif dibuat public untuk akses langsung:

```python
# Class Pelanggan
self.nama = nama  # Public

# Class Kendaraan
self.pemilik = pemilik  # Public (reference ke object Pelanggan)
self.tipe = tipe  # Public

# Class Servis
self.kendaraan = kendaraan  # Public (reference ke object Kendaraan)
self.keluhan = keluhan  # Public
```

---

### 2. Class Variable dan Instance Variable

#### a) Class Variable (Shared antar semua instance)

**Class Pelanggan:**
```python
nama_bengkel = "Bengkel Mas Ambasukiii"  # Nama bengkel (konstan)
total_pelanggan = 0  # Counter total pelanggan
diskon_member = 0.05  # Persentase diskon member
```

**Class Kendaraan:**
```python
total_kendaraan = 0  # Counter total kendaraan
jenis_valid = ["Matic", "Manual", "Bebek"]  # List jenis kendaraan valid
```

**Class Servis:**
```python
total_servis = 0  # Counter total servis
biaya_jasa_dasar = 20000  # Biaya dasar servis (dapat diubah)
```

#### b) Instance Variable (Unique per object)

Setiap object memiliki data instance variable sendiri yang di-inisialisasi melalui constructor `__init__`:

```python
# Class Pelanggan
def __init__(self, nama, no_hp):
    self.nama = nama
    self.__no_hp = None
    self.no_hp = no_hp
    Pelanggan.total_pelanggan += 1

# Class Kendaraan
def __init__(self, pemilik, plat_nomor, tipe):
    self.pemilik = pemilik
    self.tipe = tipe
    self.__plat_nomor = None
    self.plat_nomor = plat_nomor
    Kendaraan.total_kendaraan += 1

# Class Servis
def __init__(self, kendaraan, keluhan):
    self.kendaraan = kendaraan
    self.__biaya = 0
    self.keluhan = keluhan
    Servis.total_servis += 1
```

---

### 3. Class Method dan Static Method

#### a) Class Method (@classmethod)

Class method digunakan untuk operasi yang berkaitan dengan class secara keseluruhan, bukan instance spesifik:

**Alternative Constructor (Factory Method):**
```python
# Class Pelanggan - Membuat object dari dictionary
@classmethod
def dari_dict(cls, data):
    return cls(data["nama"], data["no_hp"])

# Class Kendaraan - Membuat object dari dictionary
@classmethod
def dari_dict(cls, pemilik, data):
    return cls(pemilik, data["plat_nomor"], data["tipe"])

# Class Servis - Mengubah biaya dasar untuk semua servis
@classmethod
def ubah_biaya_dasar(cls, biaya_baru):
    cls.biaya_jasa_dasar = biaya_baru
    print(f"Biaya jasa dasar diubah jadi Rp{biaya_baru:,.0f}")
```

**Contoh Penggunaan:**
```python
# Membuat pelanggan dari dictionary
p2 = Pelanggan.dari_dict({"nama": "Mas Suki", "no_hp": "089876543210"})

# Mengubah biaya dasar servis untuk semua instance
Servis.ubah_biaya_dasar(25000)
```

#### b) Static Method (@staticmethod)

Static method digunakan untuk utility function yang tidak memerlukan akses ke instance atau class:

```python
# Class Pelanggan - Validasi format nomor HP
@staticmethod
def cek_format_hp(no_hp):
    return isinstance(no_hp, str) and no_hp.startswith("08") and no_hp.isdigit()

# Class Kendaraan - Validasi format plat nomor
@staticmethod
def cek_format_plat(plat):
    return isinstance(plat, str) and plat.strip() != ""

# Class Servis - Cek apakah keluhan kosong
@staticmethod
def cek_keluhan_kosong(teks):
    return teks.strip() == ""
```

**Contoh Penggunaan:**
```python
# Validasi tanpa membuat instance
valid = Pelanggan.cek_format_hp("081234567890")  # True
kosong = Servis.cek_keluhan_kosong("")  # True
```

---

### 4. Composition (Relasi Antar Class)

Program ini menggunakan composition untuk merepresentasikan hubungan antar entitas:

```
Pelanggan ──────< Kendaraan ──────< Servis
  (1:N)              (1:N)
```

**Relasi "has-a":**
- Satu Pelanggan dapat memiliki banyak Kendaraan
- Satu Kendaraan dapat memiliki banyak riwayat Servis
- Object Kendaraan menyimpan reference ke object Pelanggan (pemilik)
- Object Servis menyimpan reference ke object Kendaraan

**Implementasi:**
```python
# Membuat pelanggan
p1 = Pelanggan("Mas Amba", "081234567890")

# Membuat kendaraan milik pelanggan p1
k1 = Kendaraan(p1, "KT 1234 AB", "Honda Beat")

# Membuat servis untuk kendaraan k1
s1 = Servis(k1, "Ganti oli dan cek rem")
s1.biaya = 50000

# Akses data berelasi
print(s1.kendaraan.pemilik.nama)  # Output: Mas Amba
```

---

## Struktur Class

### 1. Class Pelanggan

**Atribut Class:**
- `nama_bengkel`: Nama bengkel (string)
- `total_pelanggan`: Counter jumlah pelanggan (integer)
- `diskon_member`: Persentase diskon member (float)

**Atribut Instance:**
- `nama`: Nama pelanggan (public)
- `__no_hp`: Nomor HP pelanggan (private)

**Method:**
- `__init__(self, nama, no_hp)`: Constructor
- `@property no_hp`: Getter nomor HP
- `@no_hp.setter`: Setter dengan validasi format HP
- `tampilkan_info(self)`: Menampilkan info pelanggan
- `@classmethod dari_dict(cls, data)`: Factory method dari dictionary
- `@staticmethod cek_format_hp(no_hp)`: Validasi format nomor HP

---

### 2. Class Kendaraan

**Atribut Class:**
- `total_kendaraan`: Counter jumlah kendaraan (integer)
- `jenis_valid`: List jenis kendaraan valid (list)

**Atribut Instance:**
- `pemilik`: Reference ke object Pelanggan (public)
- `tipe`: Tipe/merek kendaraan (public)
- `__plat_nomor`: Plat nomor kendaraan (private)

**Method:**
- `__init__(self, pemilik, plat_nomor, tipe)`: Constructor
- `@property plat_nomor`: Getter plat nomor
- `@plat_nomor.setter`: Setter dengan auto-uppercase
- `tampilkan_info(self)`: Menampilkan info kendaraan
- `@classmethod dari_dict(cls, pemilik, data)`: Factory method dari dictionary
- `@staticmethod cek_format_plat(plat)`: Validasi format plat nomor

---

### 3. Class Servis

**Atribut Class:**
- `total_servis`: Counter jumlah servis (integer)
- `biaya_jasa_dasar`: Biaya dasar servis (integer, default 20000)

**Atribut Instance:**
- `kendaraan`: Reference ke object Kendaraan (public)
- `keluhan`: Deskripsi keluhan/jenis servis (public)
- `__biaya`: Biaya servis (private)

**Method:**
- `__init__(self, kendaraan, keluhan)`: Constructor
- `@property biaya`: Getter biaya servis
- `@biaya.setter`: Setter dengan validasi non-negatif
- `tampilkan_nota(self)`: Menampilkan nota servis
- `@classmethod ubah_biaya_dasar(cls, biaya_baru)`: Mengubah biaya dasar
- `@staticmethod cek_keluhan_kosong(teks)`: Cek keluhan kosong

---

## Alur Program

### 1. Inisialisasi Data Pelanggan

Program dimulai dengan membuat 2 object pelanggan menggunakan 2 cara berbeda:

**a. Constructor Biasa:**
```python
p1 = Pelanggan("Mas Amba", "081234567890")
p1.tampilkan_info()
# Output: Pelanggan: Mas Amba | No HP: 081234567890
```

**b. Class Method (dari dictionary):**
```python
p2 = Pelanggan.dari_dict({"nama": "Mas Suki", "no_hp": "089876543210"})
p2.tampilkan_info()
# Output: Pelanggan: Mas Suki | No HP: 089876543210
```

Program menampilkan total pelanggan yang terdaftar menggunakan class variable.

---

### 2. Pengujian Validasi Setter (no_hp)

Program menguji validasi setter nomor HP:

**Test dengan input invalid (mengandung huruf):**
```python
p1.no_hp = "0812abc"
# Output: Gagal! No HP '0812abc' tidak valid (harus diawali '08' dan hanya angka).
```

**Test dengan input valid:**
```python
p1.no_hp = "081211112222"
p1.tampilkan_info()
# Output: Pelanggan: Mas Amba | No HP: 081211112222
```

Setter berhasil memvalidasi input sebelum menyimpan data.

---

### 3. Inisialisasi Data Kendaraan

Program membuat 2 object kendaraan yang terkait dengan pelanggan:

**a. Constructor dengan reference ke pelanggan:**
```python
k1 = Kendaraan(p1, "KT 1234 AB", "Honda Beat")
k1.tampilkan_info()
# Output: Kendaraan: Honda Beat | Plat: KT 1234 AB | Pemilik: Mas Amba
```

**b. Class Method dari dictionary:**
```python
k2 = Kendaraan.dari_dict(p2, {"plat_nomor": "KT 5678 CD", "tipe": "Yamaha Vixion"})
k2.tampilkan_info()
# Output: Kendaraan: Yamaha Vixion | Plat: KT 5678 CD | Pemilik: Mas Suki
```

---

### 4. Pengujian Validasi Setter (plat_nomor)

Program menguji validasi dan auto-formatting plat nomor:

**Test dengan plat kosong:**
```python
k1.plat_nomor = ""
# Output: Gagal! Plat nomor '' tidak valid.
```

**Test dengan huruf kecil (auto-uppercase):**
```python
k1.plat_nomor = "kt 9999 zz"
k1.tampilkan_info()
# Output: Kendaraan: Honda Beat | Plat: KT 9999 ZZ | Pemilik: Mas Amba
```

Setter berhasil mengkonversi input ke uppercase.

---

### 5. Inisialisasi Data Servis

Program membuat 2 object servis untuk kendaraan yang sudah terdaftar:

```python
s1 = Servis(k1, "Ganti oli dan cek rem")
s1.biaya = 50000
s1.tampilkan_nota()
# Output:
# --- Nota Servis ---
# Kendaraan : Honda Beat (KT 9999 ZZ)
# Keluhan   : Ganti oli dan cek rem
# Biaya     : Rp50,000

s2 = Servis(k2, "Servis rutin bulanan")
s2.biaya = 75000
s2.tampilkan_nota()
# Output:
# --- Nota Servis ---
# Kendaraan : Yamaha Vixion (KT 5678 CD)
# Keluhan   : Servis rutin bulanan
# Biaya     : Rp75,000
```

---

### 6. Pengujian Validasi Setter (biaya) dan Static Method

**Test dengan biaya negatif:**
```python
s1.biaya = -10000
# Output: Gagal! Biaya tidak boleh negatif.
```

**Test static method untuk cek keluhan kosong:**
```python
print("Keluhan kosong?", Servis.cek_keluhan_kosong(""))
# Output: Keluhan kosong? True
```

**Test class method untuk ubah biaya dasar:**
```python
Servis.ubah_biaya_dasar(25000)
# Output: Biaya jasa dasar diubah jadi Rp25,000
```

---

## Output Lengkap Program

```
=== Data Pelanggan ===
Pelanggan: Mas Amba | No HP: 081234567890
Pelanggan: Mas Suki | No HP: 089876543210
Total pelanggan: 2

=== Uji Setter no_hp ===
Gagal! No HP '0812abc' tidak valid (harus diawali '08' dan hanya angka).
Pelanggan: Mas Amba | No HP: 081211112222

=== Data Kendaraan ===
Kendaraan: Honda Beat | Plat: KT 1234 AB | Pemilik: Mas Amba
Kendaraan: Yamaha Vixion | Plat: KT 5678 CD | Pemilik: Mas Suki
Total kendaraan: 2

=== Uji Setter plat_nomor ===
Gagal! Plat nomor '' tidak valid.
Kendaraan: Honda Beat | Plat: KT 9999 ZZ | Pemilik: Mas Amba

=== Data Servis ===
--- Nota Servis ---
Kendaraan : Honda Beat (KT 9999 ZZ)
Keluhan   : Ganti oli dan cek rem
Biaya     : Rp50,000
--- Nota Servis ---
Kendaraan : Yamaha Vixion (KT 5678 CD)
Keluhan   : Servis rutin bulanan
Biaya     : Rp75,000
Total servis: 2

=== Uji Setter biaya & static method ===
Gagal! Biaya tidak boleh negatif.
Keluhan kosong? True
Biaya jasa dasar diubah jadi Rp25,000
```

---

## Cara Menjalankan Program

### Persyaratan:
- Python 3.6 atau lebih baru

### Langkah-langkah:
1. Pastikan Python sudah terinstall di sistem
2. Buka terminal/command prompt
3. Navigasi ke direktori file program
4. Jalankan perintah:
   ```bash
   python POSTTEST1_2509106074_NurilAkmal.py
   ```

---

## Kesimpulan

Program sistem manajemen bengkel motor ini berhasil menerapkan konsep-konsep OOP dasar dengan Python, meliputi:

✅ **Encapsulation** - Menggunakan atribut private dengan property getter/setter untuk proteksi data  
✅ **Validasi Data** - Setter memvalidasi input sebelum menyimpan (format HP, plat nomor, biaya)  
✅ **Class Variable** - Menyimpan data shared seperti counter dan konfigurasi bengkel  
✅ **Instance Variable** - Setiap object memiliki data unique sendiri  
✅ **Class Method** - Factory method untuk membuat object dari dictionary dan mengubah konfigurasi class  
✅ **Static Method** - Utility function untuk validasi tanpa memerlukan instance  
✅ **Composition** - Relasi antar class (Pelanggan → Kendaraan → Servis)  
✅ **Auto-formatting** - Plat nomor otomatis dikonversi ke uppercase  

Program ini menjadi fondasi yang solid untuk pengembangan lebih lanjut seperti sistem CRUD interaktif, penyimpanan database, dan antarmuka pengguna grafis (GUI).
