class Klient:
    klient_items = ("imie", "miescowosc", "ulica", "email", "telefon")

    def __init__(self):
        self.imie_nazwisko = ""
        self.miejscowosc = ""
        self.adres = ""
        self.email = ""
        self.telefon = ""

    def __str__(self):
        return f'Klient:{self.imie_nazwisko}, Adres:{self.miejscowosc}, ul.{self.adres}, email:{self.email}, telefon:{self.telefon}'

    def kopiuj_z(self, zrodlo):
        self.imie_nazwisko = zrodlo.imie_nazwisko
        self.miejscowosc = zrodlo.miejscowosc
        self.adres = zrodlo.adres
        self.email = zrodlo.email
        self.telefon = zrodlo.telefon

    def dej_element(self, co_dac):
        v = ""
        if co_dac == "imie":
            v = self.imie_nazwisko
        elif co_dac == "miescowosc":
            v = self.miejscowosc
        elif co_dac == "ulica":
            v = self.adres
        elif co_dac == "email":
            v = self.email
        elif co_dac == "telefon":
            v = self.telefon
        return v

    def wstaw_element(self, co_wstaw, v):
        dane_ok = True
        if co_wstaw == "imie":
            self.imie_nazwisko = v
        elif co_wstaw == "miescowosc":
            self.miejscowosc = v
        elif co_wstaw == "ulica":
            self.adres = v
        elif co_wstaw == "email":
            self.email = v
            dane_ok = "@" in v
        elif co_wstaw == "telefon":
            self.telefon = v
        return dane_ok
