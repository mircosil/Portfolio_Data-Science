"""
main.py – Einstiegspunkt des Studien-Dashboard-Prototyps.

Diese Datei koordiniert den gesamten Programmablauf:
- Import der CSV-Daten (falls noch keine JSON existiert)
- Laden/Speichern über JsonStorage
- Erzeugen des StudienDashboard-Objekts
- Ausgabe der Ergebnisse im Terminal (ConsoleRenderer-Funktionen)

Trennung der Verantwortlichkeiten:
- Fachlogik → model.py
- Persistenz → storage.py
- CSV-Import → import_csv.py
- Darstellung → hier (Konsole)
"""

from pathlib import Path
from model import StudienDashboard
from storage import JsonStorage
from import_csv import CsvImporter

# --- ConsoleRenderer ---
def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def progress_bar(percent: float, width: int = 30) -> str:
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)

    if percent >= 75:
        return color(bar, "92")  # grün
    elif percent >= 40:
        return color(bar, "93")  # gelb
    else:
        return color(bar, "91")  # rot


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR.parent / "data"

    csv_path = DATA_DIR / "leistungen.csv"
    json_path = DATA_DIR / "daten.json"

    storage = JsonStorage(json_path)

    # Wenn noch keine JSON existiert -> einmalig importieren und speichern
    if not json_path.exists():
        importer = CsvImporter()
        mods = importer.import_modules(csv_path, debug=True)
        storage.save(mods)

    module = storage.load()

    dash = StudienDashboard(gesamt_ects=180, module=module)

    print()
    print(color("📊 Studien-Dashboard", "1"))
    print("=" * 50)

    ects_done = dash.erreichte_ects()
    ects_total = dash.gesamt_ects
    ects_missing = dash.fehlende_ects()
    progress = dash.fortschritt_prozent()
    avg = dash.durchschnittsnote()

    print(f"ECTS:      {ects_done:>3} / {ects_total}")
    print(f"Fehlend:   {ects_missing:>3}")
    print()

    print(f"Fortschritt: {progress_bar(progress)} {progress:5.1f} %")
    print()

    if avg > 0:
        avg_color = "92" if avg <= 2.0 else "93" if avg <= 3.0 else "91"
        print(f"Ø-Note:    {color(f'{avg:.2f}', avg_color)}")
    else:
        print("Ø-Note:    -")

    print("=" * 50)
