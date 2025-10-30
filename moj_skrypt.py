#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import random
import csv
import json
from typing import List, Tuple

# Miesiące i dni po polsku
MIESIACE = [
    "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
    "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"
]

DNI_ABBR_ORDER = ["pn", "wt", "sr", "cz", "pt", "so", "nd"]
DNI_FULL = {
    "pn": "poniedziałek",
    "wt": "wtorek",
    "sr": "środa",
    "cz": "czwartek",
    "pt": "piątek",
    "so": "sobota",
    "nd": "niedziela",
}

PORA_SHORT_TO_FULL = {
    "r": "rano",
    "w": "wieczór",
    "rano": "rano",
    "wieczór": "wieczór",
    "wieczorem": "wieczór",  # dopuszczamy oba warianty
}

CSV_NAME = "Dane.csv"
JSON_NAME = "Dane.json"


def parse_list_arg(arg: str) -> List[str]:
    if not arg:
        return []
    return [x.strip() for x in arg.split(",") if x.strip()]


def expand_day_range(rng: str) -> List[str]:
    # rng może być np. "pn-wt" albo "pt" (pojedynczy)
    rng = rng.strip().lower()
    if "-" in rng:
        a, b = [s.strip() for s in rng.split("-", 1)]
        if a not in DNI_ABBR_ORDER or b not in DNI_ABBR_ORDER:
            raise ValueError(f"Nieznany skrót dnia w zakresie: {rng}")
        i, j = DNI_ABBR_ORDER.index(a), DNI_ABBR_ORDER.index(b)
        if i <= j:
            abbrs = DNI_ABBR_ORDER[i:j+1]
        else:
            # pozwólmy na zakres owinięty (np. "pt-pn") – rzadko potrzebne, ale użyteczne
            abbrs = DNI_ABBR_ORDER[i:] + DNI_ABBR_ORDER[:j+1]
        return [DNI_FULL[a] for a in abbrs]
    else:
        if rng not in DNI_ABBR_ORDER:
            raise ValueError(f"Nieznany skrót dnia: {rng}")
        return [DNI_FULL[rng]]


def normalize_months(months: List[str]) -> List[str]:
    norm = []
    for m in months:
        m_low = m.strip().lower()
        # prosta normalizacja – szukamy dokładnego dopasowania
        found = None
        for ref in MIESIACE:
            if ref.lower() == m_low:
                found = ref
                break
        if not found:
            raise ValueError(f"Nieznany miesiąc: {m}")
        norm.append(found)
    return norm


def normalize_pory(pory: List[str]) -> List[str]:
    out = []
    for p in pory:
        p_low = p.strip().lower()
        if p_low not in PORA_SHORT_TO_FULL:
            raise ValueError(f"Nieznana pora dnia: {p}")
        out.append(PORA_SHORT_TO_FULL[p_low])
    return out


def build_plan(months: List[str], dni_ranges: List[str], pory: List[str]) -> List[Tuple[str, str, str]]:
    # months: lista nazw miesiecy (pełne)
    # dni_ranges: ta sama długość co months; każdy element to np. "pn-wt"
    # pory: lista pór dnia dla KAŻDEGO DNIA po rozwinięciu; brakujące -> "rano"
    if len(dni_ranges) != len(months):
        raise ValueError("Liczba zakresów dni musi odpowiadać liczbie miesięcy.")

    expanded = []
    for rng in dni_ranges:
        expanded.append(expand_day_range(rng))

    total_days = sum(len(x) for x in expanded)

    # uzupełnij pory do domyślnej "rano"
    if len(pory) < total_days:
        pory = pory + ["rano"] * (total_days - len(pory))
    elif len(pory) > total_days:
        raise ValueError("Podano więcej pór dnia niż łączna liczba dni po rozwinięciu.")

    # normalizacja pór do pełnych nazw
    pory = normalize_pory(pory)

    plan = []
    idx = 0
    for mi, month in enumerate(months):
        for day in expanded[mi]:
            pora = pory[idx]
            idx += 1
            plan.append((month, day, pora))
    return plan


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def write_csv(path: str, overwrite: bool):
    file_path = os.path.join(path, CSV_NAME)
    if os.path.exists(file_path) and not overwrite:
        return
    model = random.choice(["A", "B", "C"])
    wynik = random.randint(0, 1000)
    czas = random.randint(0, 1000)
    # Format dokładnie jak w opisie (średniki i spacje)
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        f.write("Model; Wynik; Czas; \n")
        f.write(f"{model} ; {wynik} ; {czas}s;\n")


def write_json(path: str, overwrite: bool):
    file_path = os.path.join(path, JSON_NAME)
    if os.path.exists(file_path) and not overwrite:
        return
    model = random.choice(["A", "B", "C"])
    wynik = random.randint(0, 1000)
    czas = random.randint(0, 1000)
    payload = {"Model": model, "Wynik": wynik, "Czas": f"{czas}s"}
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def read_csv_file(file_path: str) -> int:
    if not os.path.exists(file_path):
        return 0
    # Parsujemy prosty dwuliniowy CSV na średnikach z odstępami
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]
    if len(lines) < 2:
        return 0
    # Druga linia: "A ; 17 ; 465s;"
    parts = [p.strip() for p in lines[1].split(";") if p.strip() != ""]
    # spodziewane: ["A", "17", "465s"]
    if len(parts) < 3:
        return 0
    model = parts[0]
    czas_field = parts[2]
    try:
        if model == "A":
            if czas_field.endswith("s"):
                czas_val = int(czas_field[:-1])
            else:
                czas_val = int(czas_field)
            return czas_val
        return 0
    except Exception:
        return 0


def read_json_file(file_path: str) -> int:
    if not os.path.exists(file_path):
        return 0
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        model = data.get("Model")
        czas_field = str(data.get("Czas", "")).strip()
        if model == "A":
            if czas_field.endswith("s"):
                czas_val = int(czas_field[:-1])
            else:
                czas_val = int(czas_field)
            return czas_val
        return 0
    except Exception:
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="Tworzenie/odczyt plików CSV/JSON w strukturze Miesiąc/Dzień/Pora."
    )
    parser.add_argument("-m", "--miesiace", required=True,
                        help="Lista miesięcy, np.: styczeń,luty")
    parser.add_argument("-d", "--dni", required=True,
                        help="Lista zakresów dni (po jednym na miesiąc), np.: pn-wt,pt")
    parser.add_argument("-p", "--pory", default="",
                        help="Pory dnia dla każdego rozwiniętego dnia, np.: r,w,r; domyślnie 'rano'")
    parser.add_argument("-t", "--tworzenie", action="store_true",
                        help="Tryb tworzenia (gdy brak - tryb odczytu)")
    parser.add_argument("-c", "--csv", action="store_true",
                        help="Pracuj z plikami CSV")
    parser.add_argument("-j", "--json", action="store_true",
                        help="Pracuj z plikami JSON")
    parser.add_argument("--root", "-r", default=".",
                        help="Katalog bazowy (domyślnie bieżący)")
    parser.add_argument("--no-overwrite", action="store_true",
                        help="Nie nadpisuj istniejących plików przy tworzeniu")
    parser.add_argument("--seed", type=int, help="Ziarno generatora liczb losowych")

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    months = normalize_months(parse_list_arg(args.miesiace))
    dni_ranges = parse_list_arg(args.dni)
    pory_list = parse_list_arg(args.pory)

    plan = build_plan(months, dni_ranges, pory_list)

    use_csv = args.csv
    use_json = args.json
    if not use_csv and not use_json:
        # Domyślnie CSV, jeśli nic nie wskazano
        use_csv = True

    if args.tworzenie:
        # Tworzenie plików
        for month, day, pora in plan:
            path = os.path.join(args.root, month, day, pora)
            ensure_dir(path)
            if use_csv:
                write_csv(path, overwrite=not args.no_overwrite)
            if use_json:
                write_json(path, overwrite=not args.no_overwrite)
        print("Zakończono tworzenie plików.")
    else:
        # Odczyt i sumowanie czasów dla Model == 'A'
        total = 0
        for month, day, pora in plan:
            path = os.path.join(args.root, month, day, pora)
            if use_csv:
                total += read_csv_file(os.path.join(path, CSV_NAME))
            if use_json:
                total += read_json_file(os.path.join(path, JSON_NAME))
        print(total)


if __name__ == "__main__":
    main()
