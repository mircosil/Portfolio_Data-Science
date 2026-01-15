from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Optional, List, Tuple

from model import Modul, ModulErgebnis
from storage import save_module


GRADE_RE = re.compile(r"^(NB|A|B|\d,\d|\d\.\d)$", re.IGNORECASE)

def looks_like_grade(s: str) -> bool:
    s = (s or "").strip().strip('"')
    return bool(GRADE_RE.fullmatch(s))

def ects_strict(s: str) -> Optional[int]:
    s = (s or "").strip().strip('"')
    if re.fullmatch(r"\d{1,2}", s):
        v = int(s)
        return v if 1 <= v <= 30 else None
    return None

def parse_grade(s: str) -> ModulErgebnis:
    g = (s or "").strip().strip('"').upper()
    if g == "NB":
        return ModulErgebnis(note=None, status="NICHT_BESTANDEN")
    if g in {"A", "B"}:
        return ModulErgebnis(note=None, status="BESTANDEN")
    try:
        return ModulErgebnis(note=float(g.replace(",", ".")), status="BESTANDEN")
    except ValueError:
        return ModulErgebnis(note=None, status="BESTANDEN")

def clean(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().strip('"'))

def detect_dialect(csv_path: Path) -> csv.Dialect:
    sample = csv_path.read_text(encoding="utf-8-sig", errors="replace")[:4000]
    sniffer = csv.Sniffer()
    try:
        return sniffer.sniff(sample, delimiters=[",", ";", "\t"])
    except csv.Error:
        # Fallback: Semikolon ist in DE oft Standard
        class D(csv.Dialect):
            delimiter = ";"
            quotechar = '"'
            doublequote = True
            skipinitialspace = True
            lineterminator = "\n"
            quoting = csv.QUOTE_MINIMAL
        return D()

def import_csv_to_json(csv_path: Path, json_path: Path, debug: bool = True) -> List[Modul]:
    dialect = detect_dialect(csv_path)

    modules_by_key: dict[Tuple[str, int], Modul] = {}
    total_rows = 0
    kept_rows = 0

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f, dialect)

        for i, row in enumerate(reader, start=1):
            total_rows += 1
            # leere Zeilen skip
            if not row or all(not clean(c) for c in row):
                continue

            # Debug: zeig die ersten 5 Zeilen so wie Python sie sieht
            if debug and i <= 5:
                print(f"[DEBUG] Row {i}: {row}")

            # Manche Exporte liefern alles in 1 Zelle -> dann splitte nochmal hart
            # Sonderfall: ganze Zeile ist ein einziges quoted CSV-Feld
            if len(row) == 1:
                raw = row[0]

            # Versuche, die innere CSV korrekt zu parsen
            try:
                inner_reader = csv.reader(
                [raw],
                delimiter=",",
                quotechar='"',
                doublequote=True,
                skipinitialspace=True,
            )
                row = next(inner_reader)
            except Exception:
                continue


            # Name ist fast immer Spalte 0
            name = clean(row[0])
            if not name:
                continue

            # Note finden
            grade = None
            for c in row:
                if looks_like_grade(c):
                    grade = clean(c)
                    break
            if grade is None:
                continue

            # ECTS (1..30) finden, meist am Ende
            ects = None
            for c in reversed(row):
                ects = ects_strict(c)
                if ects is not None:
                    break
            if ects is None:
                continue

            kept_rows += 1
            ergebnis = parse_grade(grade)

            key = (name.lower(), ects)
            if key in modules_by_key:
                ex = modules_by_key[key]
                # Zahl-Note schlägt None
                if ex.ergebnis and ex.ergebnis.note is None and ergebnis.note is not None:
                    ex.ergebnis = ergebnis
                # BESTANDEN schlägt NICHT_BESTANDEN
                if ex.ergebnis and ex.ergebnis.status != "BESTANDEN" and ergebnis.status == "BESTANDEN":
                    ex.ergebnis.status = "BESTANDEN"
            else:
                modules_by_key[key] = Modul(name=name, ects=ects, ergebnis=ergebnis)

    modules = sorted(modules_by_key.values(), key=lambda m: m.name.lower())
    save_module(json_path, modules)

    if debug:
        print(f"[DEBUG] Total rows read: {total_rows}")
        print(f"[DEBUG] Rows matched (grade+ects+name): {kept_rows}")
        print(f"[DEBUG] Modules after dedupe: {len(modules)}")
        print(f"[DEBUG] Dialect delimiter detected: '{dialect.delimiter}'")

    return modules


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    csv_path = BASE_DIR.parent / "data" / "leistungen.csv"
    json_path = BASE_DIR.parent / "data" / "daten.json"

    mods = import_csv_to_json(csv_path, json_path, debug=True)
    print(f"Import fertig. Kurse: {len(mods)}")

