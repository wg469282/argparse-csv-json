# Skryptowy Python – Lab 3: CSV/JSON CLI


## Opis
Narzędzie CLI tworzy i/lub odczytuje pliki CSV/JSON w strukturze katalogów Miesiąc/Dzień/Pora. W trybie odczytu sumuje wartości „Czas” wyłącznie dla rekordów, w których „Model” = „A”.

## Wymagania
- Python 3.x
- Standardowa biblioteka: argparse, pathlib, os, csv, json

## Instalacja
- Sklonuj repozytorium i przejdź do katalogu projektu.
- (Opcjonalnie) utwórz i aktywuj wirtualne środowisko.
- Uruchamiaj skrypt z Pythona 3.

## Użycie (pomoc)
``` Python 
python moj_skrypt.py -h
```

## Przykłady
Tworzenie plików CSV i JSON dla dwóch miesięcy, z rozwinięciem dni i porami dnia:
```
python moj_skrypt.py -m "styczeń,luty" -d "pn-wt,pt" -p "r,w" -t -c -j

```
Odczyt i podsumowanie czasu (Model=A) dla tych samych ścieżek:
``` 
python moj_skrypt.py -m "styczeń,luty" -d "pn-wt,pt" -p "r,w" -c -j

```

Dodatkowe opcje:
- Zmiana katalogu bazowego:
```
python moj_skrypt.py -m "styczeń,luty" -d "pn-wt,pt" -p "r,w" -t -c -j --root .

```
- Zakaz nadpisywania istniejących plików:

```
python moj_skrypt.py -m "styczeń,luty" -d "pn-wt,pt" -p "r,w" -t -c -j --no-overwrite

```

## Parametry
- `-m, --months`: lista miesięcy (np. `styczeń luty`).
- `-d, --days`: zakresy dni odpowiadające kolejno podanym miesiącom (np. `pn-wt pt`).
- `-p, --times`: pory dnia dla rozwiniętych dni (`r/rano` lub `w/wieczorem`); brakujące ustawiane są na „rano”.
- `--create` lub `--read`: tryb tworzenia albo odczytu.
- `--csv` i/lub `--json`: wybór formatu plików do utworzenia/odczytu.
- `--base`: katalog bazowy (domyślnie bieżący).
- `--no-overwrite`: nie nadpisuj istniejących plików przy tworzeniu.

## Struktura tworzonych katalogów
Dla:
- Miesiące: `[styczeń, luty]`
- Dni: `[pn-wt, pt]`
- Pory: `[r, w]`

Powstaną ścieżki:
```
Styczeń/poniedziałek/rano
Styczeń/wtorek/wieczorem
Luty/piątek/rano
```

## Format plików
- CSV: plik `Dane.csv` ma 2 linie:
  - Nagłówek: `Model; Wynik; Czas;`
  - Dane: losowe wartości (Model∈{A,B,C}, Wynik 0–1000, Czas 0–1000s z sufiksem `s`).
- JSON: plik `Dane.json` z polami `Model`, `Wynik`, `Czas` (czas z sufiksem `s`).

## Wynik odczytu
W trybie `--read` skrypt sumuje wartości „Czas” tylko dla plików, w których `Model = A`, i wypisuje sumę w sekundach (oddzielnie dla CSV/JSON oraz sumę łączną, jeśli pracuje na obu formatach).

## Uwagi
- Dopuszczalne skróty i formy bez polskich znaków dla dni tygodnia (np. `pn`, `wt`, `sr`, `cz`, `pt`, `so`, `nd`).
- Brakujące pozycje w `-p/--times` uzupełniane są domyślnie jako „rano”.
  
  ##
  Uwaga: projekt został wykonany samodzielnie ze względu na trudności ze znalezieniem grupy.

