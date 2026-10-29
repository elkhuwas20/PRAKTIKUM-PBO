class JamDigital:
    def __init__(self):
        self.jam = 0
        self.menit = 0

    def atur(self, jam, menit):
        if not 0 <= jam <= 23:
            raise ValueError("jam harus 0 sampai 23")
        if not 0 <= menit <= 59:
            raise ValueError("menit harus 0 sampai 59")

        self.jam = jam
        self.menit = menit

    def tampilan(self):
        return f"{self.jam:02d}:{self.menit:02d}"


def main():
    jam_digital = JamDigital()
    print("=== JAM DIGITAL ===")
    print(f"Tampilan awal: {jam_digital.tampilan()}")

    percobaan = [(7, 30), (25, 0), (12, 75), (23, 59), (-1, 10)]
    for jam, menit in percobaan:
        print(f"Atur ke jam {jam} menit {menit} -> ", end="")
        try:
            jam_digital.atur(jam, menit)
        except ValueError as error:
            print(f"ditolak: {error}")
        else:
            print("berhasil")
        finally:
            print(f"  Tampilan jam: {jam_digital.tampilan()}")


if __name__ == "__main__":
    main()