# class animal:
#     def __int__(self, nama):
#         self.nama = nama

#     def makan(self):
#         print(f"{self.nama} sedang makan")

# class mamalia(animal):

#     def __init__(self, nama, warna_bulu):
#         super().__init__(nama)
#         self.warna_bulu = warna_bulu

#     def makan(self):
#         print(f"{self.nama} sedang makan dan bulunya berwarna {self.warna_bulu}")

# kucing = [mamalia('kucing', 'merah')], [animal('serigala')]

# class akunbank:

#     def __init__(self, nama, saldo):
#         self.nama = nama
#         self.saldo = saldo

#     def hitungbunga(self):
#         return 0

# class tabungan(akunbank):

#     def hitungbunga(self):
#         return self.saldo * 0.02

# class deposito(akunbank):

#     def hitungbunga(self):
#         return self.saldo * 0.06

# daftar_akun = [Tabungan("Budi", 1000000), Deposito("Sari", 5000000)]
# for akun in daftar_akun:
#     print(f"Bunga {akun.nama}: Rp {akun.hitung_bunga():,.2f}")

# class akunbank:

#     def __init__(self, nama, saldo):
#         self.nama = nama
#         self.saldo = saldo

#     def hitungbunga(self):
#         return 0

# class tabungan(akunbank):

#     def __init__(self, nama, saldo):
#         self.nama = nama
#         self.saldo = saldo

#     def hitungbunga(self):
#         return self.saldo * 0.02

# class deposito(akunbank):

#     def __init__(self, nama, saldo):
#         self.nama = nama
#         self.saldo = saldo

#     def hitungbunga(self):
#         return self.saldo * 0.06

# daftar_akun = [Tabungan("Budi", 1000000), Deposito("Sari", 5000000)]
# for akun in daftar_akun:
#     print()

# from abc import ABC, abstractmethod

# class akunbank(ABC):

#     # def __init__(self, nama, saldo):
#     #     self.nama = nama
#     #     self.saldo = saldo

#     @abstractmethod
#     def hitungbunga(self):
#         pass

# class tabungan(akunbank):

#     def hitungbunga(self):
#         print("bunga dari tabungan")


# class deposito(akunbank):

#     def hitungbunga(self):
#         print("bunga dari deposito")

# daftarakun = [tabungan(), deposito()]
# # daftar_akun = [Tabungan("Budi", 1000000), Deposito("Sari", 5000000)]
# for akun in daftar_akun:

#     print()

# class Rekening:
#     def __init__(self, no_rek, saldo):
#         self.no_rek = no_rek
#         self.saldo = saldo
# # Mendefinisikan operator + (__add__)
#     def __add__(self, rekening_lain):
#         total_saldo = self.saldo + rekening_lain.saldo
#         return f"Total gabungan saldo: Rp {total_saldo:,}"
# # Mendefinisikan operator > (__gt__)
#     def __gt__(self, rekening_lain):
#         return self.saldo > rekening_lain.saldo
# # Tambahkan di dalam kelas Rekening:

# # Mendefinisikan operator - (__sub__)
#     def __sub__(self, rekening_lain):
#         return self.saldo - rekening_lain.saldo
# # Mendefinisikan operator == (__eq__)
#     def __eq__(self, rekening_lain):
#         return self.no_rek == rekening_lain.no_rek
# # Mendefinisikan tampilan saat di-print (__str__)
#     def __str__(self):
#         return f"Rekening {self.no_rek} | Saldo: Rp {self.saldo:,}"
    
# rek_utama = Rekening("123", 5000000)
# rek_cadangan = Rekening("456", 2000000)
# print(rek_utama + rek_cadangan) # Memanggil __add__
# print(rek_utama > rek_cadangan) # Memanggil __gt__, Output: True
# print(rek_utama - rek_cadangan) # 3000000 <- __sub__ (selisih saldo)
# print(rek_utama == rek_cadangan) # False <- __eq__ (no. rekening beda)
# print(rek_utama) # Rekening 123 | Saldo: Rp 5,000,000 <-__str__
# # Output:
# # Total gabungan saldo: Rp 7,000,000
# # True
class akunbank:

    def __init__(self, nama, saldo):
        self.nama = nama
        self.saldo = saldo

class deposito(akunbank):

    def __init__(self, nama, saldo):
        super().__init__(nama, saldo)

akun1 = akunbank("Budi", 1000000)
akun2 = deposito("Sari", 5000000)
print(isinstance(akun1, akunbank)) 
print(isinstance(akun1, deposito)) 