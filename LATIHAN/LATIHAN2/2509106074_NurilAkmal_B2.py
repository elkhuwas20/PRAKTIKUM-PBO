class animal:

    def __init__(self, nama, umur, warna_bulu, berbisa):

        self.nama = nama
        self.umur = umur

    def makan(self):
        print(f"{self.nama} Sedang Makan")

kucing = animal("oren", 1, "oren", None)
ular = animal("cobra", 2, None, True)

class mamalia(animal):

    def __init__(self, nama, umur, warna_bulu):
        super().__init__(nama, umur)
        self.warna_bulu = warna_bulu

    def makan_mamalia(self):
        print(super().makan())


class reptil(animal):
    def __init__(self, nama, umur, berbisa):
        self.berbisa = berbisa


class Teller(Karyawan):
    def __init__(self, nama, nip):
        super().__init__(nama, nip, "Teller")
    def layani_setoran(self, rekening, nominal):
        print(f" Teller {self.nama} melayani setoran...")
rekening.setor(nominal, f"Setoran via teller {self.nip}")


