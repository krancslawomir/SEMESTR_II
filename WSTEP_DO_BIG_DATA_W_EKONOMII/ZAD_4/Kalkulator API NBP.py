# -*- coding: utf-8 -*-
"""

Kalkulator walutowy z wykorzystaniem API NBP. 
Uwzględnia średnie kursy walut pobrane ze strony NBP.
 
"""
 
import sys
import requests
from bs4 import BeautifulSoup
 
 
def pobierz_dane():
    """
    Pobiera dane ze strony NBP.
    Zwraca:
        - data_publikacji - data publikacji danych
        - dane_walut - słownik zawierający dane dla każdej waluty w postaci zagnieżdżonego słownika,
          dane_walut[kod waluty]:
            - nazwa - nazwa waluty
            - przelicznik - przelicznik waluty
            - kurs - średni kurs w PLN
    """
 
    # Pobranie danych z pliku xml:
    waluty_xml = requests.get(r'http://www.nbp.pl/kursy/xml/LastA.xml')
 
    # Ustawienie kodowania dla pliku xml ('requests' automatycznie ustawia nieprawidłowe 'ISO-8859-1'):
    waluty_xml.encoding = 'ISO-8859-2'
 
    # Stworzenie obiektu BeautifulSoup:
    waluty_soup = BeautifulSoup(waluty_xml.text, 'html.parser')
 
    # Pozyskanie i zapisanie daty publikacji:
    data_publikacji = waluty_soup.data_publikacji.string
 
    # Pozyskanie i zapisanie pozostałych danych indywidualnych dla każdej waluty (pozycji):
    dane_walut = {}
    for pozycja in waluty_soup.find_all('pozycja'):
        kod = pozycja.kod_waluty.string
        nazwa = pozycja.nazwa_waluty.string
        # Konwersja na int!
        przelicznik = int(pozycja.przelicznik.string)
        # Zamiana '.' na ',' i konwersja na float!
        kurs = float(pozycja.kurs_sredni.string.replace(',', '.'))
        dane_walut[kod] = {'nazwa': nazwa, 'przelicznik': przelicznik, 'kurs': kurs}
 
    return data_publikacji, dane_walut
 
 
def komendy(komenda):
    """Zarządza komendami wydawanymi przez użytkownika."""
 
    komenda = komenda.strip().lower()
 
    global waluty_klucze
    waluty_klucze = sorted(waluty.keys())
 
    # Jeśli komenda:
    if komenda.startswith('!'):
        if komenda == '!pomoc':
            funkcja_pomoc()
        elif komenda == '!kody':
            funkcja_kody()
        elif komenda == '!kursy':
            funkcja_kursy()
        elif komenda == '!data':
            funkcja_data()
        elif komenda == '!zamknij':
            sys.exit()
        else:
            print('Nieprawidłowa komenda!')
 
    # Jeśli komenda konwersji:
    else:
        # Wydziel waluty i kwotę:
        elementy = komenda.upper().split(' ')
 
        # Sprawdź czy drugi element to kwota:
        try:
            float(elementy[1])
        except ValueError:
            liczba = False
        else:
            liczba = True
 
        # Jeśli konwersja na PLN:
        if liczba or elementy[1] == 'PLN':
            # Skrócona forma:
            if liczba:
                for kwota in elementy[1:]:
                    przelicz_na_pln(elementy[0], float(kwota))
            # Pełna forma:
            else:
                for kwota in elementy[2:]:
                    przelicz_na_pln(elementy[0], float(kwota))
 
        # Jeśli konwersja z PLN:
        elif elementy[0] == 'PLN':
            for kwota in elementy[2:]:
                przelicz_z_pln(elementy[1], float(kwota))
 
        # Jeśli konwersja między obcymi walutami:
        else:
            for kwota in elementy[2:]:
                przelicz_obce(elementy[0], elementy[1], float(kwota))
 
 
def funkcja_pomoc():
    """Funkcja dla komendy !pomoc."""
    print(pomoc)
 
 
def funkcja_kody():
    """Funkcja dla komendy !kody."""
    for k in waluty_klucze:
        print('    {}     {}'.format(k, waluty[k]['nazwa']))
    print()
 
 
def funkcja_kursy():
    """Funkcja dla komendy !kursy."""
    print('    Kursy walut obcych w złotówkach według NBP dostępne na dzień {}\n'.format(data))
    for k in waluty_klucze:
        print('    {}{:>10} {:35}{:>11}'.format(k, waluty[k]['przelicznik'], waluty[k]['nazwa'], waluty[k]['kurs']))
    print()
 
 
def funkcja_data():
    """Funkcja dla komendy !data."""
    print('    Data publikacji danych: {}\n'.format(data))
 
 
def przelicz_na_pln(kod, kwota, tekst=True):
    """Konwersja z waluty obcej na PLN."""
    kurs = waluty[kod]['kurs']
    przelicznik = waluty[kod]['przelicznik']
    wynik = (kwota * kurs)/przelicznik
    if tekst:
        print('    {:.2f} {} == {:.2f} PLN'.format(kwota, kod, wynik))
    return wynik
 
 
def przelicz_z_pln(kod, kwota, tekst=True):
    """Konwersja z PLN na walutę obcą."""
    kurs = waluty[kod]['kurs']
    przelicznik = waluty[kod]['przelicznik']
    wynik = (przelicznik * kwota)/kurs
    if tekst:
        print('    {:.2f} PLN == {:.2f} {}'.format(kwota, wynik, kod))
    return wynik
 
 
def przelicz_obce(kod1, kod2, kwota, tekst=True):
    """Konwersja pomiędzy walutami obcymi."""
    # kod1 --> PLN --> kod2:
    wynik = przelicz_z_pln(kod2, przelicz_na_pln(kod1, kwota, tekst=False), tekst=False)
    if tekst:
        print('    {:.2f} {} == {:.2f} {}'.format(kwota, kod1, wynik, kod2))
    return wynik
 
 
if __name__ == '__main__':
 
    print('{:^100}'.format('KALKULATOR WALUTOWY Z WYKORZYSTANIEM API NBP\n'))
 
    while True:
 
        pobrano = False
 
        # Pobranie aktualnych danych z NBP:
        try:
            data, waluty = pobierz_dane()
 
        # Przechwycenie wszystkich wyjątków związanych z 'requests':
        except requests.exceptions.RequestException:
            print('Nie udało się pobrać aktualnych danych!')
            odp = input('Zamknij program [OK] lub spróbuj ponownie [dowolny klawisz]: ').upper()
            if odp == 'OK':
                break
 
        # Jeśli brak wyjątków z 'requests':
        else:
            pobrano = True
            print('Dane aktualne na dzień: {}\n'.format(data))
            break
 
    if pobrano:
        pomoc = 'Program służy do konwersji walut.\n' \
                'Wykorzystywane są aktualne kursy walut określone przez NBP na dany dzień.\n\n' \
                'Konwersja danych : AAA BBB kwota1 [kwota2, kwota3...]\n\n' \
                '\tAAA - kod waluty przeliczanej\n' \
                '\tBBB - kod waluty docelowej\n' \
                '\tkwota - przeliczana kwota\n\n' \
                'Konwersja z waluty obcej do PLN - skrócona forma: AAA kwota1 [kwota2, kwota3...]\n' \
                'Komendy:\n\n' \
                '\t!pomoc - pomoc dotycząca programu\n' \
                '\t!kody - zestawienie kodów walutowych\n' \
                '\t!kursy - zestawienie aktualnych kursów walut\n' \
                '\t!data - data publikacji danych\n' \
                '\t!zamknij - zamknięcie programu\n'
 
        print(pomoc)
 
        while True:
 
            try:
                komendy(input('$ '))
 
            # Ogólna walidacja - łapie wszystkie wyjątki. Można bardziej sprecyzować.
            except Exception as X:
                print('Nieprawidłowa komenda! Spróbuj jeszcze raz.')