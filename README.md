Installationsanleitung - Studien-Dashboard

1. Voraussetzungen
    Windows 10 oder 11
    Python 3.10 oder neuer | Download: https://www.python.org/downloads/ (Beim Installieren die Option "Add Python to PATH" aktivieren)
    Optional: GIT (wird nur zum Klonen des Repositories benötigt) | Download: https://git-scm.com/downloads


2. Repository herunterladen
    Variante A: Klonen über GIT | im Terminal folgendes eingeben:
        gh repo clone mircosil/Portfolio_Data-Science
    
    Variante B: Download als ZIP-Datei
        1. Auf GitHub: Code -> Download ZIP
        2. ZIP entpacken
        3. Ordner "Portfolio_Data-Science-main" öffnen


3. Projektstruktur prüfen
    Portfolio_Data-Science/
    │
    ├── src/
    │   ├── main.py
    │   ├── model.py
    │   ├── storage.py
    │   └── import_csv.py
    │
    ├── data/
    │   ├── leistungen.csv
    │   └── daten.json
    │
    └── README.md


4. CSV-Daten in JSON importieren | im Terminal wird folgendes eingegeben:
    cd src
    python import_csv.py

    Beispiel der erwarteten Ausgabe:
        [DEBUG] Total rows read: 29
        [DEBUG] Rows matched (grade+ects+name): 29
        [DEBUG] Modules after dedupe: 29
        [DEBUG] Dialect delimiter detected: ;
        Import fertig. Kurse: 29


5. Dashboard starten mit dem Befehl im Terminal:
    python main.py

    Erwartete Beispielausgabe:

    📊 Studien-Dashboard
    ==================================================
    ECTS:        145 / 180
    Fehlend:      35

    Fortschritt: ████████████████████████░░░░░░  80.6 %

    Ø-Note:      2.69
    ==================================================


6. Fehler & Lösungen
    Fehler: Encoding-Probleme bei CSV
    Lösung: die CSV-Datei muss in UTF-8 gespeichert sein