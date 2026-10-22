from abc import ABC, abstractmethod


class Kendaraan(ABC):
    total_kendaraan = 0

    def __init__(self, plat_nomor, merek, tahun):
        self._plat_nomor = plat_nomor.upper()  # Protected
        self._merek = merek                    # Protected
        self.__tahun = tahun                   # Private
        Kendaraan.total_kendaraan += 1

    @property
    def tahun(self):
        return self.__tahun

    @abstractmethod
    def info_kendaraan(self) -> str:
        pass

    @abstractmethod
    def jenis(self) -> str:
        pass

    def cetak_label(self):
        print(f"  [{self.jenis()}] {self._merek} | Plat: {self._plat_nomor} | Tahun: {self.__tahun}")

    def __str__(self):
        return f"{self._merek} ({self._plat_nomor})"


class MotorMatik(Kendaraan):
    def __init__(self, plat_nomor, merek, tahun, kapasitas_cc):
        super().__init__(plat_nomor, merek, tahun)
        self.kapasitas_cc = kapasitas_cc

    def info_kendaraan(self) -> str:
        return f"Plat: {self._plat_nomor} | Merek: {self._merek} | Tahun: {self.tahun} | Tipe: Matic | CC: {self.kapasitas_cc}cc"

    def jenis(self) -> str:
        return "Motor Matic"


class MotorManual(Kendaraan):
    def __init__(self, plat_nomor, merek, tahun, jumlah_gigi):
        super().__init__(plat_nomor, merek, tahun)
        self.jumlah_gigi = jumlah_gigi

    def info_kendaraan(self) -> str:
        return f"Plat: {self._plat_nomor} | Merek: {self._merek} | Tahun: {self.tahun} | Tipe: Manual | Gigi: {self.jumlah_gigi} percepatan"

    def jenis(self) -> str:
        return "Motor Manual"


class Servis:
    def __init__(self, kendaraan, jenis_servis, biaya):
        self.kendaraan = kendaraan
        self.jenis_servis = jenis_servis
        self.__biaya = 0
        self.biaya = biaya

    @property
    def biaya(self):
        return self.__biaya

    @biaya.setter
    def biaya(self, value):
        if value >= 0:
            self.__biaya = value
        else:
            print("  Gagal! Biaya tidak boleh negatif.")

    def tampilkan_nota(self):
        print(f"    Kendaraan : {self.kendaraan.info_kendaraan()}")
        print(f"    Jenis     : {self.jenis_servis}")
        print(f"    Biaya     : Rp{self.__biaya:,.0f}")

    def __add__(self, other):
        return self.__biaya + other.biaya

    def __eq__(self, other):
        return self.__biaya == other.biaya

    def __lt__(self, other):
        return self.__biaya < other.biaya

    def __gt__(self, other):
        return self.__biaya > other.biaya

    def __str__(self):
        return f"Servis({self.jenis_servis}, Rp{self.__biaya:,.0f})"


class SparePart:
    def __init__(self, nama, stok, harga):
        self.nama = nama
        self.stok = stok
        self.harga = harga

    def info(self):
        return f"{self.nama} | Stok: {self.stok} | Harga: Rp{self.harga:,.0f}"

    def __str__(self):
        return self.nama

    def __len__(self):
        return self.stok


class Mekanik:
    total_mekanik = 0

    def __init__(self, nama, spesialisasi):
        self.nama = nama
        self.spesialisasi = spesialisasi
        self._daftar_servis = []
        Mekanik.total_mekanik += 1

    def tambah_servis(self, servis):
        self._daftar_servis.append(servis)

    def laporan_mekanik(self):
        print(f"\n  Mekanik   : {self.nama} | Spesialis: {self.spesialisasi}")
        print(f"  Servis    : {len(self._daftar_servis)} pekerjaan")
        for s in self._daftar_servis:
            print(f"    - {s.jenis_servis} ({s.kendaraan})")

    def __str__(self):
        return self.nama


class Bengkel:
    def __init__(self, nama_bengkel, alamat):
        self.nama_bengkel = nama_bengkel
        self.alamat = alamat
        self._daftar_servis = []    # Komposisi
        self._daftar_sparepart = [] # Agregasi

    def tambah_servis(self, kendaraan, jenis_servis, biaya):
        servis_baru = Servis(kendaraan, jenis_servis, biaya)
        self._daftar_servis.append(servis_baru)
        return servis_baru

    def tambah_sparepart(self, sparepart):
        self._daftar_sparepart.append(sparepart)

    def laporan_servis(self):
        print(f"\n  === Laporan Servis: {self.nama_bengkel} ===")
        if not self._daftar_servis:
            print("  Belum ada servis.")
            return
        for i, s in enumerate(self._daftar_servis, 1):
            print(f"\n  Servis #{i}:")
            s.tampilkan_nota()
        total = sum(s.biaya for s in self._daftar_servis)
        print(f"\n  Total Pendapatan: Rp{total:,.0f}")

    def laporan_stok(self):
        print(f"\n  === Laporan Stok Spare Part ===")
        if not self._daftar_sparepart:
            print("  Stok kosong.")
            return
        for sp in self._daftar_sparepart:
            print(f"  - {sp.info()} | Stok (len): {len(sp)}")


class LaporanHarian:
    def __init__(self, tanggal, total_servis):
        self.tanggal = tanggal
        self.total_servis = total_servis

    def cetak_laporan(self):
        print(f"  [Laporan Harian] Tanggal: {self.tanggal} | Servis Selesai: {self.total_servis}")


class LaporanBulanan:
    def __init__(self, bulan, total_pendapatan):
        self.bulan = bulan
        self.total_pendapatan = total_pendapatan

    def cetak_laporan(self):
        print(f"  [Laporan Bulanan] Bulan: {self.bulan} | Pendapatan: Rp{self.total_pendapatan:,.0f}")


def tampilkan_laporan(laporan):
    laporan.cetak_laporan()


if __name__ == "__main__":

    print("=" * 58)
    print("  1. BUKTI ABSTRAKSI")
    print("=" * 58)
    try:
        k_abstrak = Kendaraan("KT 0000 XX", "Generik", 2020)
    except TypeError as e:
        print(f"\n  TypeError: {e}")
        print("  Kendaraan (abstract class) tidak bisa diinstansiasi.")

    print("\n" + "=" * 58)
    print("  2. POLIMORFISME via Pewarisan")
    print("=" * 58)

    k1 = MotorMatik("KT 1234 AB", "Honda Beat", 2022, 110)
    k2 = MotorManual("KT 5678 CD", "Yamaha Vixion", 2021, 6)
    k3 = MotorMatik("KT 9999 ZZ", "Honda Scoopy", 2023, 125)

    kendaraan_list = [k1, k2, k3]
    print("\n  Cetak label kendaraan (method konkret dari abstract class):")
    for k in kendaraan_list:
        k.cetak_label()

    print("\n  Info lengkap (method override tiap subclass):")
    for k in kendaraan_list:
        print(f"  {k.info_kendaraan()}")

    print(f"\n  Total Kendaraan: {Kendaraan.total_kendaraan}")

    print("\n" + "=" * 58)
    print("  3. KOMPOSISI & AGREGASI")
    print("=" * 58)

    bengkel = Bengkel("Bengkel Mas Ambasukiii", "Jl. Slamet Riyadi No. 10")

    s1 = bengkel.tambah_servis(k1, "Ganti oli mesin", 50_000)
    s2 = bengkel.tambah_servis(k2, "Servis karburator", 75_000)
    s3 = bengkel.tambah_servis(k3, "Ganti ban depan", 120_000)

    bengkel.laporan_servis()

    sp1 = SparePart("Oli Mesin MPX2", 20, 35_000)
    sp2 = SparePart("Ban Tubeless IRC 80/90", 10, 95_000)
    sp3 = SparePart("Filter Udara Honda Beat", 15, 28_000)

    bengkel.tambah_sparepart(sp1)
    bengkel.tambah_sparepart(sp2)
    bengkel.tambah_sparepart(sp3)

    bengkel.laporan_stok()

    print("\n" + "=" * 58)
    print("  4. OPERATOR OVERLOADING")
    print("=" * 58)

    print(f"\n  s1 + s2  (biaya gabungan) = Rp{s1 + s2:,.0f}")
    print(f"  s1 == s2 (biaya sama?)    = {s1 == s2}")
    print(f"  s1 < s2  (s1 lebih murah?)= {s1 < s2}")
    print(f"  s2 > s3  (s2 lebih mahal?)= {s2 > s3}")
    print(f"  len(sp1) (stok oli)       = {len(sp1)}")
    print(f"  len(sp2) (stok ban)       = {len(sp2)}")

    print("\n" + "=" * 58)
    print("  5. Mekanik & Servis")
    print("=" * 58)

    mek1 = Mekanik("Pak Hendra", "Motor Matic")
    mek2 = Mekanik("Pak Budi", "Motor Manual & Karburator")

    mek1.tambah_servis(s1)
    mek1.tambah_servis(s3)
    mek2.tambah_servis(s2)

    mek1.laporan_mekanik()
    mek2.laporan_mekanik()
    print(f"\n  Total Mekanik: {Mekanik.total_mekanik}")

    print("\n" + "=" * 58)
    print("  6. DUCK TYPING")
    print("=" * 58)

    laporan_list = [
        LaporanHarian("22 Oktober 2026", 5),
        LaporanBulanan("Oktober 2026", 3_450_000),
    ]

    print("\n  Memanggil cetak_laporan() lewat satu fungsi tampilkan_laporan():")
    for lap in laporan_list:
        tampilkan_laporan(lap)
