class KedaiError(Exception):
    pass


class MenuSudahAdaError(KedaiError):
    def __init__(self, kode, nama_lama):
        self.kode = kode
        self.nama_lama = nama_lama
        super().__init__(f"Kode {kode} sudah dipakai oleh {nama_lama}")


class Menu:
    def __init__(self, kode, nama, harga):
        self.kode = kode
        self.nama = nama
        self.harga = harga


class KedaiKopi:
    def __init__(self):
        self.daftar_menu = []

    def tambah_menu(self, menu):
        for menu_lama in self.daftar_menu:
            if menu_lama.kode == menu.kode:
                raise MenuSudahAdaError(menu.kode, menu_lama.nama)

        self.daftar_menu.append(menu)


def format_rupiah(jumlah):
    return f"Rp{jumlah:,}".replace(",", ".")


def main():
    kedai = KedaiKopi()
    menu_awal = [
        Menu("M01", "Kopi Susu Gula Aren", 18000),
        Menu("M02", "Es Teh Manis", 8000),
        Menu("M03", "Nasi Goreng Kampung", 25000),
        Menu("M04", "Mie Goreng Jawa", 23000),
        Menu("M05", "Pisang Goreng Keju", 15000),
    ]

    print("=== MENAMBAH MENU ===")
    for menu in menu_awal + [
        Menu("M02", "Es Jeruk", 10000),
        Menu("M06", "Teh Tarik", 12000),
        Menu("M06", "Kopi Tubruk", 12000),
    ]:
        try:
            kedai.tambah_menu(menu)
        except MenuSudahAdaError as error:
            print(f"[GAGAL] {error}")
            print(
                f"        {menu.nama} tidak ditambahkan, pilih kode selain {error.kode}"
            )
        else:
            print(
                f"[OK] [{menu.kode}] {menu.nama} - {format_rupiah(menu.harga)}"
            )

    print(f"Jumlah menu terdaftar: {len(kedai.daftar_menu)}")


if __name__ == "__main__":
    main()