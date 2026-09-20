class Pelanggan:
    nama_bengkel = "Bengkel Mas Ambasukiii"
    total_pelanggan = 0
    diskon_member = 0.05

    def __init__(self, nama, no_hp):
        self.nama = nama           
        self.__no_hp = None         
        self.no_hp = no_hp         
        Pelanggan.total_pelanggan += 1

    @property
    def no_hp(self):
        return self.__no_hp

    @no_hp.setter
    def no_hp(self, value):
        if Pelanggan.cek_format_hp(value):
            self.__no_hp = value
        else:
            print(f"Gagal! No HP '{value}' tidak valid (harus diawali '08' dan hanya angka).")

    def tampilkan_info(self):
        print(f"Pelanggan: {self.nama} | No HP: {self.__no_hp}")

    @classmethod
    def dari_dict(cls, data):
        return cls(data["nama"], data["no_hp"])

    @staticmethod
    def cek_format_hp(no_hp):
        return isinstance(no_hp, str) and no_hp.startswith("08") and no_hp.isdigit()


class Kendaraan:
    total_kendaraan = 0
    jenis_valid = ["Matic", "Manual", "Bebek"]

    def __init__(self, pemilik, plat_nomor, tipe):
        self.pemilik = pemilik       
        self.tipe = tipe            
        self.__plat_nomor = None     
        self.plat_nomor = plat_nomor

        Kendaraan.total_kendaraan += 1

    @property
    def plat_nomor(self):
        return self.__plat_nomor

    @plat_nomor.setter
    def plat_nomor(self, value):
        if Kendaraan.cek_format_plat(value):
            self.__plat_nomor = value.upper()
        else:
            print(f"Gagal! Plat nomor '{value}' tidak valid.")

    def tampilkan_info(self):
        print(f"Kendaraan: {self.tipe} | Plat: {self.__plat_nomor} | Pemilik: {self.pemilik.nama}")

    @classmethod
    def dari_dict(cls, pemilik, data):
        return cls(pemilik, data["plat_nomor"], data["tipe"])

    @staticmethod
    def cek_format_plat(plat):
        return isinstance(plat, str) and plat.strip() != ""


class Servis:
    total_servis = 0
    biaya_jasa_dasar = 20000

    def __init__(self, kendaraan, keluhan):
        self.kendaraan = kendaraan   
        self.__biaya = 0             

        self.keluhan = keluhan     
        Servis.total_servis += 1

    @property
    def biaya(self):
        return self.__biaya

    @biaya.setter
    def biaya(self, value):
        if value >= 0:
            self.__biaya = value
        else:
            print("Gagal! Biaya tidak boleh negatif.")

    def tampilkan_nota(self):
        print(f"--- Nota Servis ---")
        print(f"Kendaraan : {self.kendaraan.tipe} ({self.kendaraan.plat_nomor})")
        print(f"Keluhan   : {self.keluhan}")
        print(f"Biaya     : Rp{self.biaya:,.0f}")

    @classmethod
    def ubah_biaya_dasar(cls, biaya_baru):
        cls.biaya_jasa_dasar = biaya_baru
        print(f"Biaya jasa dasar diubah jadi Rp{biaya_baru:,.0f}")

    @staticmethod
    def cek_keluhan_kosong(teks):
        return teks.strip() == ""


if __name__ == "__main__":
    print("=== Data Pelanggan ===")
    p1 = Pelanggan("Mas Amba", "081234567890")
    p2 = Pelanggan.dari_dict({"nama": "Mas Suki", "no_hp": "089876543210"})
    p1.tampilkan_info()
    p2.tampilkan_info()
    print("Total pelanggan:", Pelanggan.total_pelanggan)

    print("\n=== Uji Setter no_hp ===")
    p1.no_hp = "0812abc"        
    p1.no_hp = "081211112222"   
    p1.tampilkan_info()

    print("\n=== Data Kendaraan ===")
    k1 = Kendaraan(p1, "KT 1234 AB", "Honda Beat")
    k2 = Kendaraan.dari_dict(p2, {"plat_nomor": "KT 5678 CD", "tipe": "Yamaha Vixion"})
    k1.tampilkan_info()
    k2.tampilkan_info()
    print("Total kendaraan:", Kendaraan.total_kendaraan)

    print("\n=== Uji Setter plat_nomor ===")
    k1.plat_nomor = ""            
    k1.plat_nomor = "kt 9999 zz"  
    k1.tampilkan_info()

    print("\n=== Data Servis ===")
    s1 = Servis(k1, "Ganti oli dan cek rem")
    s2 = Servis(k2, "Servis rutin bulanan")
    s1.biaya = 50000
    s2.biaya = 75000
    s1.tampilkan_nota()
    s2.tampilkan_nota()
    print("Total servis:", Servis.total_servis)

    print("\n=== Uji Setter biaya & static method ===")
    s1.biaya = -10000  
    print("Keluhan kosong?", Servis.cek_keluhan_kosong(""))

    Servis.ubah_biaya_dasar(25000)