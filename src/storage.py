import json
from pathlib import Path
from model import Modul, ModulErgebnis


def save_module(path: Path, module: list[Modul]) -> None:
    data = []
    for m in module:
        data.append({
            "name": m.name,
            "ects": m.ects,
            "ergebnis": ( 
            {"note": m.ergebnis.note, "status": m.ergebnis.status} 
            if m.ergebnis else None
            )
        })
        
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')



def load_module(path: Path) -> list[Modul]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    module = []

    for item in raw:
        ergebnis = item["ergebnis"]
        module.append(
            Modul(
                name=item["name"],
                ects=item["ects"],
                ergebnis=ModulErgebnis(**ergebnis) if ergebnis else None
            )
        )

    return module