class BarisDataError(Exception):
    def __init__(self, nomor_baris, alasan):
        self.nomor_baris = nomor_baris
        self.alasan = alasan
        super().__init__(f"Baris {nomor_baris}: {alasan}")


class Pendaftar:
    def __init__(self, nama, umur):
        self.nama = nama
        self.umur = umur


def baca_pendaftar(nomor_baris, teks):
    kolom = teks.split(";")
    if len(kolom) != 2:
        raise BarisDataError(nomor_baris, "format harus nama;umur")

    nama = kolom[0].strip()
    teks_umur = kolom[1].strip()
    if not nama:
        raise BarisDataError(nomor_baris, "nama tidak boleh kosong")

    try:
        umur = int(teks_umur)
    except ValueError as error:
        raise BarisDataError(
            nomor_baris, f"umur '{teks_umur}' bukan angka"
        ) from error

    if not 17 <= umur <= 25:
        raise BarisDataError(
            nomor_baris, f"umur {umur} di luar syarat 17-25 tahun"
        )

    return Pendaftar(nama, umur)


def main():
    data = [
        "Ayu Lestari;20",
        "Bima Saputra",
        "Citra Dewi;dua puluh",
        ";19",
        "Dimas Pratama;30",
        "Eka Putri;18",
        "Fajar Nugraha;21;Samarinda",
    ]
    peserta = []
    ditolak = 0

    print("=== IMPOR DATA PENDAFTAR LOMBA DEBAT ===")
    for nomor_baris, teks in enumerate(data, start=1):
        try:
            pendaftar = baca_pendaftar(nomor_baris, teks)
        except BarisDataError as error:
            print(f"[DITOLAK] {error}")
            if error.__cause__ is not None:
                print("          (penyebab asli: kesalahan konversi angka)")
            ditolak += 1
        else:
            peserta.append(pendaftar)
            print(
                f"[OK] Baris {nomor_baris}: "
                f"{pendaftar.nama} ({pendaftar.umur} tahun)"
            )

    print(f"\nDiterima: {len(peserta)}, ditolak: {ditolak}")
    print("Daftar peserta:")
    for pendaftar in peserta:
        print(f"- {pendaftar.nama} ({pendaftar.umur} tahun)")


if __name__ == "__main__":
    main()