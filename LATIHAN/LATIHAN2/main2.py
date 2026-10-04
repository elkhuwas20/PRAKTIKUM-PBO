# class nasabah:
#     def __init__(self, nama, nomor_rekening, saldo):
#         self.nama = nama
#         self.nomor_rekening = nomor_rekening
#         self.saldo = saldo

#     def tarik_tunai(self, atm: {saldo_kas}, jumlah):
#         self.saldo -= jumlah
#         atm.saldo_kas

# class mesinatm:

#     def __init__(self, id_atm, lokasi, saldo_kas):
#         self.id_atm = id_atm
#         self.lokasi = lokasi
#         self.saldo_kas = saldo_kas

#     def proses_penarikan(nama, jumlah):
#         pass

# dapa = nasabah("Dapa", "12345", 1000)
# atm_pusat = mesinatm("54321", "Samarinda", "10000")

# print(dapa.nama)

# class bank:
#     def __init__(self, nama_bank, kode, total_karyawan):
#         self.nama_bank = nama_bank
#         self.kode = kode
#         self.total_karyawan = total_karyawan
#         self.karyawan = []

#     def tambah_karyawan(self, nama, nip, posisi):
#         karyawan_baru = karyawan(nama, nip, posisi)
#         self.karyawan.append(karyawan)

# class karyawan:
#     def __init__(self, nama, nip, posisi):
#         self.nama = nama
#         self.nip = nip
#         self.posisi = posisi

# bank = bank("BCA", "12345")
# dapa = karyawan("dapa", "012", "Manager")
# bank.tambah_karyawan(dapa)

# del bank
# print(nama.dapa)


class Bank:
    def __init__(self, nama_bank, kode):
        self.nama_bank = nama_bank
        self.kode = kode
        self.karyawan = []

    def tambah_karyawan(self, nama, nip, posisi):
        karyawan_baru = Karyawan(nama, nip, posisi)
        self.karyawan.append(karyawan_baru) 


class Karyawan:
    def __init__(self, nama, nip, posisi):
        self.nama = nama
        self.nip = nip
        self.posisi = posisi


bank_bca = Bank("BCA", "12345")
bank_bca.tambah_karyawan("Dapa", "012", "Manager")

print(bank_bca.kode)