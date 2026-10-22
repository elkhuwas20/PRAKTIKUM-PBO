# LAPORAN POSTTEST 3

Proyek ini adalah sistem aplikasi manajemen bengkel motor (lanjutan) menggunakan bahasa Python dengan konsep Object Oriented Programming (OOP) yang berfokus pada Abstraksi, Polimorfisme, dan Relasi UML.

## Identitas

**Nama**: Nuril Akmal  
**NIM**: 2509106074

---

## Deskripsi Program

Program ini merupakan pengembangan lanjutan dari sistem manajemen bengkel motor "Bengkel Mas Ambasukiii". Program menerapkan tiga konsep utama: **Relasi UML** (Asosiasi, Agregasi, Komposisi), **Abstraksi** (Abstract Base Class), dan **Polimorfisme** (Pewarisan, Duck Typing, Operator Overloading).

### Fitur Utama:

- `Kendaraan` diubah menjadi **abstract class** dengan 2 `@abstractmethod`
- `MotorMatik` dan `MotorManual` mengimplementasikan seluruh abstract method
- **Polimorfisme via pewarisan**: `info_kendaraan()` dan `jenis()` di-override di kedua subclass, dipanggil lewat satu loop
- **Duck Typing**: `LaporanHarian` dan `LaporanBulanan` punya method `cetak_laporan()` yang sama, dipanggil lewat fungsi `tampilkan_laporan()`
- **Operator Overloading**: `Servis` mengimplementasikan `__add__`, `__eq__`, `__lt__`, `__gt__`; `SparePart` mengimplementasikan `__len__`
- Relasi UML tetap dipertahankan dari Posttest 2

---

## Class Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            CLASS DIAGRAM — Bengkel Motor                            │
└─────────────────────────────────────────────────────────────────────────────────────┘

         <<abstract>>
        ┌────────────────────────────┐
        │         Kendaraan          │
        ├────────────────────────────┤
        │ # _plat_nomor: str         │
        │ # _merek: str              │
        │ - __tahun: int             │
        │ + total_kendaraan: int     │
        ├────────────────────────────┤
        │ + tahun: property          │
        │ + cetak_label()            │  ← method konkret
        │ <<abstract>> info_kendaraan│
        │ <<abstract>> jenis()       │
        └────────────────────────────┘
                    △
          __________|__________
         |                     |
┌────────────────┐    ┌─────────────────┐
│   MotorMatik   │    │   MotorManual   │
├────────────────┤    ├─────────────────┤
│ + kapasitas_cc │    │ + jumlah_gigi   │
├────────────────┤    ├─────────────────┤
│ + info_kend.() │    │ + info_kend.()  │
│ + jenis()      │    │ + jenis()       │
└────────────────┘    └─────────────────┘
         │  (asosiasi)
         │ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
                                                  │
┌──────────────────────┐             ┌────────────┴──────────┐
│       Bengkel        │             │        Mekanik        │
├──────────────────────┤             ├───────────────────────┤
│ + nama_bengkel: str  │             │ + nama: str           │
│ + alamat: str        │             │ + spesialisasi: str   │
│ # _daftar_servis     │◆            │ # _daftar_servis      │
│ # _daftar_sparepart  │◇            │ + total_mekanik: int  │
├──────────────────────┤             ├───────────────────────┤
│ + tambah_servis()    │             │ + tambah_servis()     │
│ + tambah_sparepart() │             │ + laporan_mekanik()   │
│ + laporan_servis()   │             └───────────────────────┘
│ + laporan_stok()     │
└──────────────────────┘
     ◆ (komposisi)    ◇ (agregasi)
          │                │
┌─────────┴──────┐   ┌─────┴──────────────┐
│     Servis     │   │     SparePart      │
├────────────────┤   ├────────────────────┤
│ + kendaraan    │   │ + nama: str        │
│ + jenis_servis │   │ + stok: int        │
│ - __biaya: int │   │ + harga: int       │
├────────────────┤   ├────────────────────┤
│ + biaya: prop  │   │ + info()           │
│ + tampil_nota()│   │ + __str__()        │
│ + __add__()    │   │ + __len__()        │
│ + __eq__()     │   └────────────────────┘
│ + __lt__()     │
│ + __gt__()     │
└────────────────┘

── Duck Typing (tidak berkaitan lewat pewarisan) ──────────────────
┌─────────────────────┐     ┌──────────────────────┐
│   LaporanHarian     │     │   LaporanBulanan     │
├─────────────────────┤     ├──────────────────────┤
│ + tanggal: str      │     │ + bulan: str         │
│ + total_servis: int │     │ + total_pendapatan   │
├─────────────────────┤     ├──────────────────────┤
│ + cetak_laporan()   │     │ + cetak_laporan()    │
└─────────────────────┘     └──────────────────────┘
              ↘                  ↙
         tampilkan_laporan(laporan)   ← fungsi duck typing
```

---

### Penjelasan Relasi

#### a) Asosiasi — `Mekanik` ↔ `Servis`

`Mekanik` menyimpan referensi ke object `Servis` melalui `_daftar_servis`, namun keduanya dibuat secara terpisah dan dapat exist tanpa satu sama lain. Relasi ini dipilih **Asosiasi** (bukan Agregasi) karena `Servis` tidak "dimiliki" oleh `Mekanik` — `Servis` sudah dibuat lebih dulu oleh `Bengkel`, kemudian di-link ke `Mekanik` dari luar.

#### b) Agregasi — `Bengkel` ◇→ `SparePart`

`Bengkel` menyimpan daftar `SparePart`, tetapi `SparePart` dibuat di luar `Bengkel` dan tetap bisa diakses secara mandiri setelah program selesai. Relasi ini dipilih **Agregasi** (bukan Komposisi) karena `SparePart` bisa hidup tanpa `Bengkel` — stok spare part bisa saja dipinjam, dipindah, atau dipakai di tempat lain.

#### c) Komposisi — `Bengkel` ◆→ `Servis`

`Servis` dibuat **di dalam** method `Bengkel.tambah_servis()` dan tidak pernah dibuat secara mandiri dari luar. Relasi ini dipilih **Komposisi** karena `Servis` lahir dari `Bengkel` dan tidak memiliki makna di luar konteks bengkel — jika `Bengkel` tidak ada, tidak ada alasan `Servis` untuk exist.

---

## Penerapan Abstraksi

### Abstract Class: `Kendaraan`

`Kendaraan` dibuat sebagai abstract class menggunakan `ABC` dengan **2 abstract method**:

```python
from abc import ABC, abstractmethod

class Kendaraan(ABC):
    @abstractmethod
    def info_kendaraan(self) -> str:
        pass

    @abstractmethod
    def jenis(self) -> str:
        pass

    # Method konkret — dipakai bersama semua subclass
    def cetak_label(self):
        print(f"  [{self.jenis()}] {self._merek} | Plat: {self._plat_nomor} | Tahun: {self.__tahun}")
```

### Implementasi pada Subclass

| Abstract Method | `MotorMatik` | `MotorManual` |
|----------------|--------------|---------------|
| `info_kendaraan()` | Menampilkan + CC mesin | Menampilkan + jumlah gigi |
| `jenis()` | Mengembalikan `"Motor Matic"` | Mengembalikan `"Motor Manual"` |

### Bukti Abstraksi

`Kendaraan` tidak dapat diinstansiasi langsung karena merupakan abstract class:

```python
try:
    k_abstrak = Kendaraan("KT 0000 XX", "Generik", 2020)
except TypeError as e:
    print(f"TypeError: {e}")
```

Output:
```
TypeError: Can't instantiate abstract class Kendaraan without an implementation
           for abstract methods 'info_kendaraan', 'jenis'
Kendaraan (abstract class) tidak bisa diinstansiasi.
```

---

## Penerapan Polimorfisme

### 1. Polimorfisme via Pewarisan

Method `info_kendaraan()` dan `jenis()` di-override di `MotorMatik` dan `MotorManual` dengan perilaku berbeda. Keduanya dipanggil lewat satu loop:

```python
kendaraan_list = [k1, k2, k3]  # campuran MotorMatik dan MotorManual

for k in kendaraan_list:
    k.cetak_label()       # method konkret dari abstract class

for k in kendaraan_list:
    print(k.info_kendaraan())  # method yang di-override tiap subclass
```

Output berbeda sesuai tipe objek — tanpa `if/elif type()`:
```
[Motor Matic] Honda Beat | Plat: KT 1234 AB | Tahun: 2022
[Motor Manual] Yamaha Vixion | Plat: KT 5678 CD | Tahun: 2021
[Motor Matic] Honda Scoopy | Plat: KT 9999 ZZ | Tahun: 2023
```

### 2. Duck Typing

`LaporanHarian` dan `LaporanBulanan` tidak berhubungan lewat pewarisan, tapi keduanya punya method `cetak_laporan()`. Fungsi `tampilkan_laporan()` memanggil keduanya tanpa peduli tipenya:

```python
def tampilkan_laporan(laporan):
    laporan.cetak_laporan()   # duck typing — siapapun boleh selama punya method ini

laporan_list = [
    LaporanHarian("22 Oktober 2026", 5),
    LaporanBulanan("Oktober 2026", 3_450_000),
]

for lap in laporan_list:
    tampilkan_laporan(lap)
```

Output:
```
[Laporan Harian]  Tanggal: 22 Oktober 2026 | Servis Selesai: 5
[Laporan Bulanan] Bulan: Oktober 2026 | Pendapatan: Rp3,450,000
```

### 3. Operator Overloading

Class `Servis` mengimplementasikan magic method untuk operasi perbandingan biaya:

```python
class Servis:
    def __add__(self, other): return self.__biaya + other.biaya   # s1 + s2
    def __eq__(self, other):  return self.__biaya == other.biaya  # s1 == s2
    def __lt__(self, other):  return self.__biaya < other.biaya   # s1 < s2
    def __gt__(self, other):  return self.__biaya > other.biaya   # s1 > s2
```

Class `SparePart` mengimplementasikan `__len__` untuk mengambil jumlah stok:

```python
class SparePart:
    def __len__(self): return self.stok   # len(sp1) → jumlah stok
```

Output:
```
s1 + s2  (biaya gabungan) = Rp125,000
s1 == s2 (biaya sama?)    = False
s1 < s2  (s1 lebih murah?)= True
s2 > s3  (s2 lebih mahal?)= False
len(sp1) (stok oli)       = 20
len(sp2) (stok ban)       = 10
```

---

## Struktur Class

### 1. Class `Kendaraan` (Abstract Class)

**Atribut:**
- `_plat_nomor` (protected), `_merek` (protected), `__tahun` (private)
- `total_kendaraan` (class variable)

**Method:**
- `@abstractmethod info_kendaraan()` — wajib diimplementasikan subclass
- `@abstractmethod jenis()` — wajib diimplementasikan subclass
- `cetak_label()` — method konkret, dipakai bersama semua subclass
- `@property tahun` — getter atribut private

---

### 2. Class `MotorMatik` (Subclass 1)

**Atribut Tambahan:** `kapasitas_cc`

**Method Override:** `info_kendaraan()` → tambah info CC, `jenis()` → `"Motor Matic"`

---

### 3. Class `MotorManual` (Subclass 2)

**Atribut Tambahan:** `jumlah_gigi`

**Method Override:** `info_kendaraan()` → tambah info gigi, `jenis()` → `"Motor Manual"`

---

### 4. Class `Servis` (Komposisi dalam Bengkel)

**Atribut:** `kendaraan`, `jenis_servis`, `__biaya` (private)

**Method:** `tampilkan_nota()`, `@property biaya`, `__add__`, `__eq__`, `__lt__`, `__gt__`, `__str__`

---

### 5. Class `SparePart` (Agregasi dalam Bengkel)

**Atribut:** `nama`, `stok`, `harga`

**Method:** `info()`, `__str__`, `__len__`

---

### 6. Class `Mekanik` (Asosiasi dengan Servis)

**Atribut:** `nama`, `spesialisasi`, `_daftar_servis`, `total_mekanik`

**Method:** `tambah_servis()`, `laporan_mekanik()`

---

### 7. Class `Bengkel`

**Atribut:** `nama_bengkel`, `alamat`, `_daftar_servis` (Komposisi), `_daftar_sparepart` (Agregasi)

**Method:** `tambah_servis()`, `tambah_sparepart()`, `laporan_servis()`, `laporan_stok()`

---

### 8. Class `LaporanHarian` & `LaporanBulanan` (Duck Typing)

Kedua class tidak berkaitan lewat pewarisan tapi memiliki method `cetak_laporan()` yang dipanggil lewat fungsi `tampilkan_laporan()`.

---

## Output Lengkap Program

```
==========================================================
  1. BUKTI ABSTRAKSI
==========================================================

  TypeError: Can't instantiate abstract class Kendaraan without an implementation
             for abstract methods 'info_kendaraan', 'jenis'
  Kendaraan (abstract class) tidak bisa diinstansiasi.

==========================================================
  2. POLIMORFISME via Pewarisan
==========================================================

  Cetak label kendaraan (method konkret dari abstract class):
  [Motor Matic] Honda Beat | Plat: KT 1234 AB | Tahun: 2022
  [Motor Manual] Yamaha Vixion | Plat: KT 5678 CD | Tahun: 2021
  [Motor Matic] Honda Scoopy | Plat: KT 9999 ZZ | Tahun: 2023

  Info lengkap (method override tiap subclass):
  Plat: KT 1234 AB | Merek: Honda Beat | Tahun: 2022 | Tipe: Matic | CC: 110cc
  Plat: KT 5678 CD | Merek: Yamaha Vixion | Tahun: 2021 | Tipe: Manual | Gigi: 6 percepatan
  Plat: KT 9999 ZZ | Merek: Honda Scoopy | Tahun: 2023 | Tipe: Matic | CC: 125cc

  Total Kendaraan: 3

==========================================================
  3. KOMPOSISI & AGREGASI
==========================================================

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

  === Laporan Stok Spare Part ===
  - Oli Mesin MPX2 | Stok: 20 | Harga: Rp35,000 | Stok (len): 20
  - Ban Tubeless IRC 80/90 | Stok: 10 | Harga: Rp95,000 | Stok (len): 10
  - Filter Udara Honda Beat | Stok: 15 | Harga: Rp28,000 | Stok (len): 15

==========================================================
  4. OPERATOR OVERLOADING
==========================================================

  s1 + s2  (biaya gabungan) = Rp125,000
  s1 == s2 (biaya sama?)    = False
  s1 < s2  (s1 lebih murah?)= True
  s2 > s3  (s2 lebih mahal?)= False
  len(sp1) (stok oli)       = 20
  len(sp2) (stok ban)       = 10

==========================================================
  5. ASOSIASI — Mekanik & Servis
==========================================================

  Mekanik   : Pak Hendra | Spesialis: Motor Matic
  Servis    : 2 pekerjaan
    - Ganti oli mesin (Honda Beat (KT 1234 AB))
    - Ganti ban depan (Honda Scoopy (KT 9999 ZZ))

  Mekanik   : Pak Budi | Spesialis: Motor Manual & Karburator
  Servis    : 1 pekerjaan
    - Servis karburator (Yamaha Vixion (KT 5678 CD))

  Total Mekanik: 2

==========================================================
  6. DUCK TYPING
==========================================================

  Memanggil cetak_laporan() lewat satu fungsi tampilkan_laporan():
  [Laporan Harian] Tanggal: 22 Oktober 2026 | Servis Selesai: 5
  [Laporan Bulanan] Bulan: Oktober 2026 | Pendapatan: Rp3,450,000
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
   python POSTTEST3_2509106074_NurilAkmal.py
   ```

---

## Nilai Plus: Penerapan Prinsip SOLID

Program ini menerapkan **Open/Closed Principle (OCP)** dari prinsip SOLID.

### Open/Closed Principle (OCP)

> "Software entities should be open for extension, but closed for modification."

**Bagian yang menerapkan OCP:** Fungsi `tampilkan_laporan()` dan class `Kendaraan` (abstract).

**Penjelasan:**
- Fungsi `tampilkan_laporan(laporan)` bekerja untuk `LaporanHarian` dan `LaporanBulanan` tanpa perlu diubah. Jika ada tipe laporan baru (misal `LaporanTahunan`), cukup buat class baru dengan method `cetak_laporan()` — fungsi `tampilkan_laporan()` tidak perlu disentuh sama sekali.
- `Kendaraan` sebagai abstract class juga menerapkan OCP: jika ada jenis kendaraan baru (misal `MotorListrik`), cukup buat subclass baru yang mengimplementasikan `info_kendaraan()` dan `jenis()`, tanpa mengubah kode class `Bengkel`, `Servis`, atau `Mekanik` yang sudah ada.

```python
# Contoh: menambah jenis laporan baru tanpa ubah kode lama
class LaporanTahunan:
    def cetak_laporan(self):
        print("[Laporan Tahunan] ...")

# Fungsi tampilkan_laporan() langsung bisa menerimanya tanpa modifikasi
tampilkan_laporan(LaporanTahunan())
```

---

## Kesimpulan

✅ **Relasi UML** — Asosiasi (`Mekanik` ↔ `Servis`), Agregasi (`Bengkel` ◇→ `SparePart`), Komposisi (`Bengkel` ◆→ `Servis`)

✅ **Abstraksi** — `Kendaraan` sebagai abstract class dengan 2 `@abstractmethod` (`info_kendaraan`, `jenis`) dan 1 method konkret (`cetak_label`). Terbukti tidak bisa diinstansiasi langsung.

✅ **Polimorfisme via Pewarisan** — `info_kendaraan()` dan `jenis()` di-override di `MotorMatik` dan `MotorManual`, dipanggil lewat satu loop tanpa `if/elif type()`.

✅ **Duck Typing** — `LaporanHarian` dan `LaporanBulanan` dipanggil lewat fungsi `tampilkan_laporan()` yang sama meski tidak ada hubungan pewarisan.

✅ **Operator Overloading** — `Servis` mengimplementasikan `__add__`, `__eq__`, `__lt__`, `__gt__`; `SparePart` mengimplementasikan `__len__`.

✅ **Nilai Plus OCP (SOLID)** — Kode terbuka untuk ekstensi (tambah subclass/laporan baru) tanpa mengubah kode yang sudah ada.
