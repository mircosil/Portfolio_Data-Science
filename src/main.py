from pathlib import Path
from model import StudienDashboard
from storage import load_module

if __name__ == "__main__":
    module = load_module(Path("../data/daten.json"))
    dash = StudienDashboard(gesamt_ects=180, module=module)

    def color(text: str, code: str) -> str:
        return f"\033[{code}m{text}\033[0m"


    def progress_bar(percent: float, width: int = 30) -> str:
        filled = int(width * percent / 100)
        bar = "█" * filled + "░" * (width - filled)

        if percent >= 75:
            bar = color(bar, "92")   # grün
        elif percent >= 40:
            bar = color(bar, "93")   # gelb
        else:
            bar = color(bar, "91")   # rot

        return bar


    print()
    print(color("📊 Studien-Dashboard", "1"))
    print("=" * 50)

    ects_done = dash.erreichte_ects()
    ects_total = dash.gesamt_ects
    ects_missing = dash.fehlende_ects()
    progress = dash.fortschritt_prozent()
    avg = dash.durchschnittsnote()

    print(f"ECTS:        {ects_done:>3} / {ects_total}")
    print(f"Fehlend:     {ects_missing:>3}")
    print()

    print(f"Fortschritt: {progress_bar(progress)} {progress:5.1f} %")
    print()

    if avg > 0:
        avg_color = "92" if avg <= 2.0 else "93" if avg <= 3.0 else "91"
        print(f"Ø-Note:      {color(f'{avg:.2f}', avg_color)}")
    else:
        print("Ø-Note:      –")

    print("=" * 50)
