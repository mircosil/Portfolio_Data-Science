import json
from pathlib import Path
from typing import List
from model import Modul, ModulErgebnis
from json import JSONDecodeError

class JsonStorage:
    def __init__(self, path: Path):
        self.path = path

    def save(self, module: List[Modul]) -> None:
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

        self.path.parent.mkdir(exist_ok=True)
        self.path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def load(self) -> List[Modul]:
        if not self.path.exists() or self.path.stat().st_size == 0:
            return []

        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except JSONDecodeError:
            return []

        module: List[Modul] = []
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
