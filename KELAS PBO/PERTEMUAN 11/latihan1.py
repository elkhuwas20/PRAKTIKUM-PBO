def rata_rata_nilai(daftar_teks):
    total = 0
    jumlah_valid = 0

    for teks in daftar_teks:
        try:
            nilai = int(teks)
        except ValueError:
            print(f"  '{teks}' bukan angka, dilewati")
        else:
            total += nilai
            jumlah_valid += 1

    return total // jumlah_valid


def proses_kelas(nama_kelas, daftar_teks):
    print(f"=== {nama_kelas} ===")
    try:
        rata_rata = rata_rata_nilai(daftar_teks)
    except ZeroDivisionError:
        print("Tidak ada nilai yang valid, rata-rata tidak bisa dihitung")
    else:
        print(f"Rata-rata: {rata_rata}")
    print()


def main():
    proses_kelas("KELAS A", ["80", "75", "sembilan puluh", "92", ""])
    proses_kelas("KELAS B", ["-", "tidak hadir"])


if __name__ == "__main__":
    main()