from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ModulErgebnis:
    note: Optional[float]
    status: str

@dataclass
class Modul:
    name: str
    ects: int
    ergebnis: Optional[ModulErgebnis] = None

    def ist_bewertet(self) -> bool:
        return self.ergebnis is not None and self.ergebnis.status == "BESTANDEN"


@dataclass
class StudienDashboard:
    gesamt_ects: int
    module: List[Modul]

    def erreichte_ects(self) -> int:
        return sum(m.ects for m in self.module if m.ist_bewertet())

    def fehlende_ects(self) -> int:
        return self.gesamt_ects - self.erreichte_ects()

    def fortschritt_prozent(self) -> float:
        return (self.erreichte_ects() / self.gesamt_ects) * 100.0

    def durchschnittsnote(self) -> float:
        noten = [
            m.ergebnis.note
            for m in self.module
            if m.ergebnis and m.ergebnis.status == "BESTANDEN" and m.ergebnis.note is not None
        ]
        return sum(noten) / len(noten) if noten else 0.0