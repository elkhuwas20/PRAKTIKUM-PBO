# LAPORAN POSTTEST 2

Proyek ini adalah sistem aplikasi manajemen bengkel motor (lanjutan) menggunakan bahasa Python dengan konsep Object Oriented Programming (OOP) yang berfokus pada Relasi UML dan Inheritance.

## Identitas

**Nama**: Nuril Akmal  
**NIM**: 2509106074

---

## Deskripsi Program

Program ini merupakan pengembangan lanjutan dari sistem manajemen bengkel motor "Bengkel Mas Ambasukiii" yang dibuat menggunakan bahasa pemrograman Python. Program ini menerapkan dua konsep utama yaitu **Relasi UML** (Asosiasi, Agregasi, Komposisi) dan **Inheritance** (Pewarisan).

### Fitur Utama:

- Terdapat 5 class: `Kendaraan` (superclass), `MotorMatik`, `MotorManual` (subclass), `Mekanik`, `Servis`, `SparePart`, dan `Bengkel`
- Menerapkan **Inheritance**: `MotorMatik` dan `MotorManual` mewarisi `Kendaraan`
- Menerapkan **Komposisi**: `Bengkel` membuat dan memiliki `Servis` secara penuh
- Menerapkan **Agregasi**: `Bengkel` menggunakan `SparePart` yang bisa hidup mandiri
- Menerapkan **Asosiasi**: `Mekanik` mengetahui `Servis` tanpa saling bergantung
- Menggunakan atribut `protected` (`_nama`) dan `private` (`__nama`) sesuai tingkat akses

---

## Penerapan Konsep OOP

### 1. Relasi UML

Program ini menerapkan 3 jenis relasi UML antara class-class yang ada:

#### a) Asosiasi (Association)

Asosiasi adalah relasi "menggunakan" atau "mengetahui" antar dua class yang masing-masing bisa exist secara mandiri. Pada program ini, relasi Asosiasi terjadi antara **Mekanik** dan **Servis**.

```
Mekanik ─────────────── Servis
         (asosiasi)
```

Mekanik bisa exist tanpa Servis, dan Servis bisa exist tanpa Mekanik. Mereka hanya saling dihubungkan melalui method `tambah_servis()`.

**Implementasi:**
```python
class Mekanik:
    def __init__(self, nama, spesialisasi):
        self.nama = nama
        self.spesialisasi = spesialisasi
        self._daftar_servis = []  # Asosiasi ke Servis

    # ASOSIASI: Mekanik dihubungkan ke servis dari luar
    def tambah_servis(self, servis):
        self._daftar_servis.append(servis)
```

**Bukti Asosiasi:** Object `s1`, `s2`, `s3` sudah dibuat terlebih dahulu oleh Bengkel, kemudian di-link ke Mekanik. Keduanya tidak saling bergantung untuk exist.

```python
mek1.tambah_servis(s1)  # Link dari luar — keduanya sudah ada
mek1.tambah_servis(s3)
mek2.tambah_servis(s2)
```

---

#### b) Agregasi (Aggregation)

Agregasi adalah relasi "memiliki" namun bagian (part) bisa hidup mandiri tanpa keseluruhan (whole). Pada program ini, relasi Agregasi terjadi antara **Bengkel** dan **SparePart**.

```
Bengkel ◇────────────── SparePart
         (agregasi)
```

`SparePart` dibuat di luar `Bengkel` dan tetap bisa diakses meskipun tidak lagi berada di dalam bengkel.

**Implementasi:**
```python
class Bengkel:
    def __init__(self, nama_bengkel, alamat):
        # AGREGASI: SparePart di-inject dari luar, bisa exist sendiri
        self._daftar_sparepart = []

    def tambah_sparepart(self, sparepart):
        self._daftar_sparepart.append(sparepart)
```

**Bukti Agregasi:** `SparePart` dibuat secara mandiri di luar `Bengkel`, kemudian ditambahkan. Setelah program selesai, object `sp1` dan `sp2` masih bisa diakses sendiri.

```python
# SparePart dibuat MANDIRI di luar Bengkel
sp1 = SparePart("Oli Mesin MPX2", 20, 35_000)
sp2 = SparePart("Ban Tubeless IRC 80/90", 10, 95_000)

bengkel.tambah_sparepart(sp1)  # Ditambahkan ke bengkel

# sp1 masih exist dan bisa diakses tanpa bengkel
print(sp1.info())  # Bukti Agregasi
```

---

#### c) Komposisi (Composition)

Komposisi adalah relasi "terdiri dari" yang paling kuat, di mana bagian (part) tidak bisa hidup tanpa keseluruhan (whole). Pada program ini, relasi Komposisi terjadi antara **Bengkel** dan **Servis**.

```
Bengkel ◆────────────── Servis
         (komposisi)
```

`Servis` dibuat **di dalam** method `Bengkel.tambah_servis()`. Servis tidak pernah dibuat secara mandiri dari luar — dia lahir dan mati bersama Bengkel.

**Implementasi:**
```python
class Bengkel:
    def __init__(self, nama_bengkel, alamat):
        # KOMPOSISI: List Servis dimiliki penuh oleh Bengkel
        self._daftar_servis = []

    # KOMPOSISI: Servis dibuat dan dikelola DI DALAM Bengkel
    def tambah_servis(self, kendaraan, jenis_servis, biaya):
        servis_baru = Servis(kendaraan, jenis_servis, biaya)  # Dibuat di sini
        self._daftar_servis.append(servis_baru)
        return servis_baru
```

**Bukti Komposisi:** Tidak ada satu pun `Servis` yang dibuat dengan `Servis(...)` langsung di `main`. Semua servis dibuat melalui `bengkel.tambah_servis(...)`.

```python
s1 = bengkel.tambah_servis(k1, "Ganti oli mesin", 50_000)   # Dibuat oleh Bengkel
s2 = bengkel.tambah_servis(k2, "Servis karburator", 75_000)
s3 = bengkel.tambah_servis(k3, "Ganti ban depan", 120_000)
```

---

### 2. Inheritance (Pewarisan)

#### Struktur Inheritance

```
        Kendaraan          (Superclass / Parent Class)
        /       \
  MotorMatik  MotorManual  (Subclass / Child Class)
```

---

#### a) Superclass: `Kendaraan`

Superclass berisi atribut dan method umum yang diwarisi oleh semua subclass.

```python
class Kendaraan:
    total_kendaraan = 0  # Class variable

    def __init__(self, plat_nomor, merek, tahun):
        self._plat_nomor = plat_nomor.upper()  # Protected — bisa diakses subclass
        self._merek = merek                    # Protected — bisa diakses subclass
        self.__tahun = tahun                   # Private — eksklusif superclass saja
        Kendaraan.total_kendaraan += 1

    @property
    def tahun(self):
        return self.__tahun  # Akses __tahun hanya lewat property

    def info_kendaraan(self):
        return (f"Plat: {self._plat_nomor} | Merek: {self._merek} "
                f"| Tahun: {self.__tahun}")

    def jenis(self):
        return "Kendaraan Umum"
```

---

#### b) Subclass 1: `MotorMatik`

`MotorMatik` mewarisi `Kendaraan` dan menambahkan atribut spesifik `kapasitas_cc`.

```python
class MotorMatik(Kendaraan):
    def __init__(self, plat_nomor, merek, tahun, kapasitas_cc):
        super().__init__(plat_nomor, merek, tahun)  # Panggil constructor superclass
        self.kapasitas_cc = kapasitas_cc             # Atribut spesifik MotorMatik

    # Override method info_kendaraan — tambah info CC
    def info_kendaraan(self):
        dasar = super().info_kendaraan()  # Ambil hasil dari superclass
        return f"{dasar} | Tipe: Matic | CC: {self.kapasitas_cc}cc"

    # Override method jenis
    def jenis(self):
        return "Motor Matic"
```

**Perbedaan dari superclass:** Memiliki atribut `kapasitas_cc` dan method `info_kendaraan()` yang menampilkan informasi CC mesin.

---

#### c) Subclass 2: `MotorManual`

`MotorManual` mewarisi `Kendaraan` dan menambahkan atribut spesifik `jumlah_gigi`.

```python
class MotorManual(Kendaraan):
    def __init__(self, plat_nomor, merek, tahun, jumlah_gigi):
        super().__init__(plat_nomor, merek, tahun)  # Panggil constructor superclass
        self.jumlah_gigi = jumlah_gigi               # Atribut spesifik MotorManual

    # Override method info_kendaraan — tambah info jumlah gigi
    def info_kendaraan(self):
        dasar = super().info_kendaraan()
        return f"{dasar} | Tipe: Manual | Gigi: {self.jumlah_gigi} percepatan"

    # Override method jenis
    def jenis(self):
        return "Motor Manual"
```

**Perbedaan dari superclass:** Memiliki atribut `jumlah_gigi` dan method `info_kendaraan()` yang menampilkan informasi jumlah percepatan transmisi.

---

#### d) Penggunaan `super()`

Setiap subclass memanggil `super().__init__()` untuk menginisialisasi atribut milik superclass sebelum menambahkan atribut sendiri:

```python
# Contoh pada MotorMatik
def __init__(self, plat_nomor, merek, tahun, kapasitas_cc):
    super().__init__(plat_nomor, merek, tahun)  # Inisialisasi Kendaraan dulu
    self.kapasitas_cc = kapasitas_cc             # Baru tambah milik sendiri
```

Subclass juga memanggil `super().info_kendaraan()` dalam method override untuk mengambil output dasar dari superclass dan menambahkan informasi spesifik:

```python
def info_kendaraan(self):
    dasar = super().info_kendaraan()  # Ambil output dari Kendaraan
    return f"{dasar} | Tipe: Matic | CC: {self.kapasitas_cc}cc"
```

---

#### e) Tingkat Akses Protected & Private

| Atribut | Tipe | Di mana | Keterangan |
|---------|------|---------|------------|
| `_plat_nomor` | Protected | `Kendaraan` | Dapat diakses oleh subclass |
| `_merek` | Protected | `Kendaraan` | Dapat diakses oleh subclass |
| `__tahun` | Private | `Kendaraan` | Eksklusif superclass, diakses via `@property` |
| `kapasitas_cc` | Public | `MotorMatik` | Atribut spesifik subclass |
| `jumlah_gigi` | Public | `MotorManual` | Atribut spesifik subclass |

**Contoh akses atribut protected dari subclass:**
```python
print(k1._plat_nomor)  # 'KT 1234 AB' — OK karena protected
print(k2._merek)       # 'Yamaha Vixion' — OK karena protected
```

**Contoh akses atribut private melalui property:**
```python
print(k1.tahun)   # 2022 — melalui @property, bukan langsung __tahun
print(k2.tahun)   # 2021
```

---

## Struktur Class

### 1. Class `Kendaraan` (Superclass)

**Atribut Class:**
- `total_kendaraan`: Counter jumlah kendaraan (integer)

**Atribut Instance:**
- `_plat_nomor`: Plat nomor kendaraan (protected)
- `_merek`: Merek kendaraan (protected)
- `__tahun`: Tahun pembuatan (private)

**Method:**
- `__init__(self, plat_nomor, merek, tahun)`: Constructor
- `@property tahun`: Getter untuk atribut private `__tahun`
- `info_kendaraan(self)`: Menampilkan info dasar kendaraan
- `jenis(self)`: Mengembalikan string jenis kendaraan

---

### 2. Class `MotorMatik` (Subclass 1)

**Atribut Tambahan:**
- `kapasitas_cc`: Kapasitas mesin dalam cc (public, khusus MotorMatik)

**Method Override:**
- `info_kendaraan(self)`: Menambahkan info tipe "Matic" dan kapasitas CC
- `jenis(self)`: Mengembalikan `"Motor Matic"`

---

### 3. Class `MotorManual` (Subclass 2)

**Atribut Tambahan:**
- `jumlah_gigi`: Jumlah percepatan/gigi transmisi (public, khusus MotorManual)

**Method Override:**
- `info_kendaraan(self)`: Menambahkan info tipe "Manual" dan jumlah gigi
- `jenis(self)`: Mengembalikan `"Motor Manual"`

---

### 4. Class `Servis`

**Atribut Instance:**
- `kendaraan`: Reference ke object Kendaraan (Asosiasi)
- `jenis_servis`: Jenis pekerjaan servis (public)
- `__biaya`: Biaya servis (private, diakses via property)

**Method:**
- `@property biaya` / `@biaya.setter`: Getter & setter dengan validasi non-negatif
- `tampilkan_nota(self)`: Mencetak nota servis
- `__str__`: Representasi string object

---

### 5. Class `SparePart`

**Atribut Instance:**
- `nama`: Nama spare part (public)
- `stok`: Jumlah stok (public)
- `harga`: Harga satuan (public)

**Method:**
- `info(self)`: Menampilkan info spare part
- `__str__`: Representasi string object

---

### 6. Class `Mekanik`

**Atribut Class:**
- `total_mekanik`: Counter jumlah mekanik (integer)

**Atribut Instance:**
- `nama`: Nama mekanik (public)
- `spesialisasi`: Bidang spesialisasi (public)
- `_daftar_servis`: List servis yang ditangani (protected, Asosiasi)

**Method:**
- `tambah_servis(self, servis)`: Menghubungkan mekanik ke servis (Asosiasi)
- `laporan_mekanik(self)`: Mencetak laporan mekanik

---

### 7. Class `Bengkel`

**Atribut Instance:**
- `nama_bengkel`: Nama bengkel (public)
- `alamat`: Alamat bengkel (public)
- `_daftar_servis`: List servis (protected, Komposisi)
- `_daftar_sparepart`: List spare part (protected, Agregasi)

**Method:**
- `tambah_servis(self, kendaraan, jenis_servis, biaya)`: Membuat & menyimpan Servis (Komposisi)
- `tambah_sparepart(self, sparepart)`: Menyimpan referensi SparePart (Agregasi)
- `laporan_servis(self)`: Mencetak laporan seluruh servis
- `laporan_stok(self)`: Mencetak laporan stok spare part

---

## Alur Program

### 1. Inheritance — Membuat Objek Kendaraan

Program membuat 3 object kendaraan menggunakan subclass `MotorMatik` dan `MotorManual`:

```python
k1 = MotorMatik("KT 1234 AB", "Honda Beat", 2022, 110)
k2 = MotorManual("KT 5678 CD", "Yamaha Vixion", 2021, 6)
k3 = MotorMatik("KT 9999 ZZ", "Honda Scoopy", 2023, 125)
```

Program menampilkan info masing-masing kendaraan dengan hasil yang berbeda sesuai override:

```
[Motor Matic] Plat: KT 1234 AB | Merek: Honda Beat | Tahun: 2022 | Tipe: Matic | CC: 110cc
[Motor Manual] Plat: KT 5678 CD | Merek: Yamaha Vixion | Tahun: 2021 | Tipe: Manual | Gigi: 6 percepatan
[Motor Matic] Plat: KT 9999 ZZ | Merek: Honda Scoopy | Tahun: 2023 | Tipe: Matic | CC: 125cc
```

---

### 2. Komposisi — Bengkel Membuat Servis

Program membuat object `Bengkel`, lalu menambahkan servis lewat method bengkel (bukan langsung membuat `Servis`):

```python
bengkel = Bengkel("Bengkel Mas Ambasukiii", "Jl. Slamet Riyadi No. 10")
s1 = bengkel.tambah_servis(k1, "Ganti oli mesin", 50_000)
s2 = bengkel.tambah_servis(k2, "Servis karburator", 75_000)
s3 = bengkel.tambah_servis(k3, "Ganti ban depan", 120_000)
```

Bengkel kemudian mencetak laporan:

```
=== Laporan Servis: Bengkel Mas Ambasukiii ===

Servis #1:
  Kendaraan : Plat: KT 1234 AB | Merek: Honda Beat | Tahun: 2022 | Tipe: Matic | CC: 110cc
  Jenis     : Ganti oli mesin
  Biaya     : Rp50,000

Total Pendapatan: Rp245,000
```

---

### 3. Agregasi — SparePart Independen

Program membuat object `SparePart` secara mandiri, lalu menyambungkannya ke bengkel:

```python
sp1 = SparePart("Oli Mesin MPX2", 20, 35_000)
sp2 = SparePart("Ban Tubeless IRC 80/90", 10, 95_000)
bengkel.tambah_sparepart(sp1)
bengkel.tambah_sparepart(sp2)
```

Setelah ditambahkan ke bengkel, `sp1` dan `sp2` tetap dapat diakses secara mandiri — membuktikan sifat agregasi (tidak seperti komposisi).

---

### 4. Asosiasi — Mekanik Dihubungkan ke Servis

Program membuat `Mekanik` dan menghubungkannya ke servis yang sudah ada:

```python
mek1 = Mekanik("Pak Hendra", "Motor Matic")
mek1.tambah_servis(s1)
mek1.tambah_servis(s3)
mek2.tambah_servis(s2)
```

Keduanya (Mekanik dan Servis) bisa exist secara mandiri sebelum dan sesudah dihubungkan.

---

## Output Lengkap Program

```
=== Data Kendaraan ===
[Motor Matic] Plat: KT 1234 AB | Merek: Honda Beat | Tahun: 2022 | Tipe: Matic | CC: 110cc
[Motor Manual] Plat: KT 5678 CD | Merek: Yamaha Vixion | Tahun: 2021 | Tipe: Manual | Gigi: 6 percepatan
[Motor Matic] Plat: KT 9999 ZZ | Merek: Honda Scoopy | Tahun: 2023 | Tipe: Matic | CC: 125cc   
Total Kendaraan: 3

  === Laporan Servis: Bengkel Mas Ambasukiii ===

  Servis #1:
    Kendaraan : Plat: KT 1234 AB | Merek: Honda Beat | Tahun: 2022 | Tipe: Matic | CC: 110cc   
    Jenis     : Ganti oli mesin
    Biaya     : Rp50,000

  Servis #2:
    Kendaraan : Plat: KT 5678 CD | Merek: Yamaha Vixion | Tahun: 2021 | Tipe: Manual | Gigi: 6 percepatan
    Jenis     : Servis karburator
    Biaya     : Rp75,000

  Servis #3:
    Kendaraan : Plat: KT 9999 ZZ | Merek: Honda Scoopy | Tahun: 2023 | Tipe: Matic | CC: 125cc 
    Jenis     : Ganti ban depan
    Biaya     : Rp120,000

  Total Pendapatan: Rp245,000
,000
  - Filter Udara Honda Beat | Stok: 15 | Harga: Rp28,000

  Mekanik  : Pak Hendra | Spesialis: Motor Matic
  Jumlah Servis Ditangani: 2
    - Ganti oli mesin (Honda Beat (KT 1234 AB))
    - Ganti ban depan (Honda Scoopy (KT 9999 ZZ))

  Mekanik  : Pak Budi | Spesialis: Motor Manual & Karburator
,000
  - Filter Udara Honda Beat | Stok: 15 | Harga: Rp28,000

  Mekanik  : Pak Hendra | Spesialis: Motor Matic
  Jumlah Servis Ditangani: 2
    - Ganti oli mesin (Honda Beat (KT 1234 AB))
    - Ganti ban depan (Honda Scoopy (KT 9999 ZZ))

  Mekanik  : Pak Budi | Spesialis: Motor Manual & Karburator
  Jumlah Servis Ditangani: 1
    - Servis karburator (Yamaha Vixion (KT 5678 CD))
,000
  - Filter Udara Honda Beat | Stok: 15 | Harga: Rp28,000

  Mekanik  : Pak Hendra | Spesialis: Motor Matic
  Jumlah Servis Ditangani: 2
    - Ganti oli mesin (Honda Beat (KT 1234 AB))
    - Ganti ban depan (Honda Scoopy (KT 9999 ZZ))

  Mekanik  : Pak Budi | Spesialis: Motor Manual & Karburator
  Jumlah Servis Ditangani: 1
,000
  - Filter Udara Honda Beat | Stok: 15 | Harga: Rp28,000

  Mekanik  : Pak Hendra | Spesialis: Motor Matic
  Jumlah Servis Ditangani: 2
    - Ganti oli mesin (Honda Beat (KT 1234 AB))
    - Ganti ban depan (Honda Scoopy (KT 9999 ZZ))

  Mekanik  : Pak Budi | Spesialis: Motor Manual & Karburator
  - Filter Udara Honda Beat | Stok: 15 | Harga: Rp28,000

  Mekanik  : Pak Hendra | Spesialis: Motor Matic
  Jumlah Servis Ditangani: 2
    - Ganti oli mesin (Honda Beat (KT 1234 AB))
    - Ganti ban depan (Honda Scoopy (KT 9999 ZZ))

  Mekanik  : Pak Budi | Spesialis: Motor Manual & Karburator

  Mekanik  : Pak Hendra | Spesialis: Motor Matic
  Jumlah Servis Ditangani: 2
    - Ganti oli mesin (Honda Beat (KT 1234 AB))
    - Ganti ban depan (Honda Scoopy (KT 9999 ZZ))

  Mekanik  : Pak Budi | Spesialis: Motor Manual & Karburator
    - Ganti oli mesin (Honda Beat (KT 1234 AB))
    - Ganti ban depan (Honda Scoopy (KT 9999 ZZ))

  Mekanik  : Pak Budi | Spesialis: Motor Manual & Karburator

  Mekanik  : Pak Budi | Spesialis: Motor Manual & Karburator
  Jumlah Servis Ditangani: 1
    - Servis karburator (Yamaha Vixion (KT 5678 CD)    - Servis karburator (Yamaha Vixion (KT 5678 CD))

Total Mekanik: 2
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
   python POSTTEST2_2509106074_NurilAkmal.py
   ```

---

## Kesimpulan

Program sistem manajemen bengkel motor lanjutan ini berhasil menerapkan dua konsep OOP utama:

### Relasi UML:

✅ **Asosiasi** — `Mekanik` ↔ `Servis`: Keduanya saling mengetahui namun dapat hidup mandiri. Mekanik dihubungkan ke servis setelah kedua object dibuat secara terpisah.

✅ **Agregasi** — `Bengkel` ◇→ `SparePart`: `SparePart` dibuat di luar `Bengkel` dan tetap bisa diakses secara independen meskipun sudah ditambahkan ke bengkel.

✅ **Komposisi** — `Bengkel` ◆→ `Servis`: `Servis` hanya dibuat melalui method milik `Bengkel`. Servis tidak pernah dibuat secara mandiri di luar Bengkel.

### Inheritance:

✅ **Superclass & Subclass** — `Kendaraan` sebagai parent, `MotorMatik` dan `MotorManual` sebagai child class.

✅ **Penggunaan `super()`** — Setiap subclass memanggil `super().__init__()` dan `super().info_kendaraan()` untuk memanfaatkan kode superclass.

✅ **Atribut Tambahan** — `MotorMatik` memiliki `kapasitas_cc`, `MotorManual` memiliki `jumlah_gigi`.

✅ **Method Overriding** — `info_kendaraan()` dan `jenis()` di-override di kedua subclass dengan perilaku berbeda.

✅ **Tingkat Akses** — `_plat_nomor` dan `_merek` bersifat protected (dapat diakses subclass), `__tahun` bersifat private (hanya lewat `@property`).
