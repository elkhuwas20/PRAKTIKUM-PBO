# Superclass
class Kendaraan:
    total_kendaraan = 0

    def __init__(self, plat_nomor, merek, tahun):
        self._plat_nomor = plat_nomor.upper()  
        self._merek = merek                   
        self.__tahun = tahun                   
        Kendaraan.total_kendaraan += 1

    @property
    def tahun(self):
        return self.__tahun

    def info_kendaraan(self):
        return f"Plat: {self._plat_nomor} | Merek: {self._merek} | Tahun: {self.__tahun}"

    def jenis(self):
        return "Kendaraan Umum"

    def __str__(self):
        return f"{self._merek} ({self._plat_nomor})"


# Subclass 1 — atribut tambahan: kapasitas_cc
class MotorMatik(Kendaraan):
    def __init__(self, plat_nomor, merek, tahun, kapasitas_cc):
        super().__init__(plat_nomor, merek, tahun)
        self.kapasitas_cc = kapasitas_cc

    def info_kendaraan(self):
        return f"{super().info_kendaraan()} | Tipe: Matic | CC: {self.kapasitas_cc}cc"

    def jenis(self):
        return "Motor Matic"


# Subclass 2 — atribut tambahan: jumlah_gigi
class MotorManual(Kendaraan):
    def __init__(self, plat_nomor, merek, tahun, jumlah_gigi):
        super().__init__(plat_nomor, merek, tahun)
        self.jumlah_gigi = jumlah_gigi

    def info_kendaraan(self):
        return f"{super().info_kendaraan()} | Tipe: Manual | Gigi: {self.jumlah_gigi} percepatan"

    def jenis(self):
        return "Motor Manual"


# Relasi ASOSIASI dengan Servis
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
        print(f"\n  Mekanik  : {self.nama} | Spesialis: {self.spesialisasi}")
        print(f"  Jumlah Servis Ditangani: {len(self._daftar_servis)}")
        for s in self._daftar_servis:
            print(f"    - {s.jenis_servis} ({s.kendaraan})")

    def __str__(self):
        return self.nama


# Relasi KOMPOSISI dengan Bengkel
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

    def __str__(self):
        return f"Servis({self.jenis_servis}, Rp{self.__biaya:,.0f})"


# Relasi AGREGASI dengan Bengkel
class SparePart:
    def __init__(self, nama, stok, harga):
        self.nama = nama
        self.stok = stok
        self.harga = harga

    def info(self):
        return f"{self.nama} | Stok: {self.stok} | Harga: Rp{self.harga:,.0f}"

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
            print(f"  - {sp.info()}")


if __name__ == "__main__":

    # Data kendaraan
    k1 = MotorMatik("KT 1234 AB", "Honda Beat", 2022, 110)
    k2 = MotorManual("KT 5678 CD", "Yamaha Vixion", 2021, 6)
    k3 = MotorMatik("KT 9999 ZZ", "Honda Scoopy", 2023, 125)

    print("=== Data Kendaraan ===")
    print(f"[{k1.jenis()}] {k1.info_kendaraan()}")
    print(f"[{k2.jenis()}] {k2.info_kendaraan()}")
    print(f"[{k3.jenis()}] {k3.info_kendaraan()}")
    print(f"Total Kendaraan: {Kendaraan.total_kendaraan}")

    # Data bengkel & servis
    bengkel = Bengkel("Bengkel Mas Ambasukiii", "Jl. Slamet Riyadi No. 10")

    s1 = bengkel.tambah_servis(k1, "Ganti oli mesin", 50_000)
    s2 = bengkel.tambah_servis(k2, "Servis karburator", 75_000)
    s3 = bengkel.tambah_servis(k3, "Ganti ban depan", 120_000)

    bengkel.laporan_servis()

    # Data spare part
    sp1 = SparePart("Oli Mesin MPX2", 20, 35_000)
    sp2 = SparePart("Ban Tubeless IRC 80/90", 10, 95_000)
    sp3 = SparePart("Filter Udara Honda Beat", 15, 28_000)

    bengkel.tambah_sparepart(sp1)
    bengkel.tambah_sparepart(sp2)
    bengkel.tambah_sparepart(sp3)

    bengkel.laporan_stok()

    # Data mekanik
    mek1 = Mekanik("Pak Hendra", "Motor Matic")
    mek2 = Mekanik("Pak Budi", "Motor Manual & Karburator")

    mek1.tambah_servis(s1)
    mek1.tambah_servis(s3)
    mek2.tambah_servis(s2)

    mek1.laporan_mekanik()
    mek2.laporan_mekanik()
    print(f"\nTotal Mekanik: {Mekanik.total_mekanik}")
