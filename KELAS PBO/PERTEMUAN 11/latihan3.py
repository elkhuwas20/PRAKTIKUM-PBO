class PerpustakaanError(Exception):
    pass


class BukuSedangDipinjamError(PerpustakaanError):
    def __init__(self, judul, peminjam):
        self.judul = judul
        self.peminjam = peminjam
        super().__init__(f"Buku '{judul}' sedang dipinjam oleh {peminjam}")


class BatasPinjamError(PerpustakaanError):
    def __init__(self, nama, batas):
        self.nama = nama
        self.batas = batas
        super().__init__(f"{nama} sudah meminjam {batas} buku (batas maksimal)")


class Buku:
    def __init__(self, judul):
        self.judul = judul
        self.peminjam = None


class Anggota:
    BATAS_PINJAM = 2

    def __init__(self, nama):
        self.nama = nama
        self.buku_dipinjam = []

    def pinjam(self, buku):
        if buku.peminjam is not None:
            raise BukuSedangDipinjamError(buku.judul, buku.peminjam)
        if len(self.buku_dipinjam) >= self.BATAS_PINJAM:
            raise BatasPinjamError(self.nama, self.BATAS_PINJAM)

        buku.peminjam = self.nama
        self.buku_dipinjam.append(buku)

    def kembalikan(self, buku):
        if buku not in self.buku_dipinjam:
            raise PerpustakaanError(
                f"{self.nama} tidak sedang meminjam '{buku.judul}'"
            )

        self.buku_dipinjam.remove(buku)
        buku.peminjam = None


def main():
    ayu = Anggota("Ayu")
    bima = Anggota("Bima")
    laskar_pelangi = Buku("Laskar Pelangi")
    bumi_manusia = Buku("Bumi Manusia")
    negeri_5_menara = Buku("Negeri 5 Menara")

    print("=== PEMINJAMAN BUKU ===")
    for anggota, buku in [
        (ayu, laskar_pelangi),
        (ayu, bumi_manusia),
        (ayu, negeri_5_menara),
        (bima, laskar_pelangi),
    ]:
        try:
            anggota.pinjam(buku)
        except BatasPinjamError as error:
            print(f"Gagal: {error}")
            print(
                f"  Saran: kembalikan dulu salah satu dari {error.batas} buku"
            )
        except BukuSedangDipinjamError as error:
            print(f"Gagal: {error}")
            print(f"  Saran: tunggu sampai {error.peminjam} mengembalikannya")
        else:
            print(f"{anggota.nama} meminjam '{buku.judul}'")

    print("\n=== PENGEMBALIAN ===")
    try:
        bima.kembalikan(bumi_manusia)
    except PerpustakaanError as error:
        print(f"Gagal: {error}")

    ayu.kembalikan(laskar_pelangi)
    print(f"Ayu mengembalikan '{laskar_pelangi.judul}'")

    bima.pinjam(laskar_pelangi)
    print(f"Bima meminjam '{laskar_pelangi.judul}'")


if __name__ == "__main__":
    main()