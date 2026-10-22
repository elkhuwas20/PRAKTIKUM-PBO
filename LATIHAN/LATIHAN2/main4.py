""" Penerapan SOLID di Python"""

class Hero:
    def __init__(self, name, health):
        self.name = name
        self.health = health


    def serang(self, hero_target):
        hero_target.health -= 10
        print(f"{self.name} menyerang {hero_target.name} dan mengurangi 10 health.")

class Tampilanhero:
    def tampilkan(self, hero):
        print(f"Nama Hero: {hero.name}, Health: {hero.health}")

class penyimpanhero:
    def simpan(self, hero, namafile):
        with open(namafile, 'w') as file:
            file.write(f"{hero.name},{hero.health}")
        print(f"Data hero {hero.name} disimpan ke {namafile}.")

Gusion = Hero("Gusion", 100)
Tampilan = Tampilanhero()
Penyimpan = penyimpanhero()

Tampilan.tampilkan(Gusion)
Penyimpan.simpan(Gusion, "data_hero.txt")

"""OCP"""

class Hero:

    def __init__(self, attack):
        self.attack = attack

    def hitung_damage(self):
        return self.attack
    
class Fighter(Hero):

    def hitung_damage(self):
        return self.attack * 2

class Mage(Hero):
    def hitung_damage(self):
        return self.attack * 3

class Assassin(Hero):
    def hitung_damage(self):
        return self.attack * 4


print(Fighter(10).hitung_damage())  # Output: 20
print(Mage(10).hitung_damage())     # Output: 30
print(Assassin(10).hitung_damage()) # Output: 40

"""LSP"""

from abc import ABC, abstractmethod

class Unit(ABC):
    @abstractmethod
    def bergerak(self):
        pass

class Minion(Unit):
    def bergerak(self):
        print("Minion bergerak dengan berjalan.")

class Turet(Unit):
    def bergerak(self):
        raise Exception("Turet tidak bisa bergerak.")

def maju(unit: Unit):
    unit.bergerak()


"""ISP"""
class BisaMenyerang(ABC):
    @abstractmethod
    def menyerang(self):
        pass

class BisaHeal(ABC):
    @abstractmethod
    def heal(self):
        pass

class Fighter(BisaMenyerang):
    def menyerang(self):
        print("Fighter menyerang musuh.")

class Support(BisaMenyerang, BisaHeal):
    def menyerang(self):
        print("Support menyerang musuh.")

    def heal(self):
        print("Support menyembuhkan teman.")

Fighter().menyerang()
Support().menyerang()
Support().heal()

"""DIP"""

class Senjata(ABC):
    @abstractmethod
    def pukul(self):
        pass

class pedang(Senjata):
    def pukul(self):
        return 10

class kapak(Senjata):
    def pukul(self):
        return 15
    

class Hero:
    def __init__(self, nama, senjata):
        self.nama = nama
        self.senjata = senjata

    def serang(self):
        damage = self.senjata.pukul()
        print(f"Hero {self.nama} menyerang dengan damage {damage}.")

    