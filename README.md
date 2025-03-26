# JustForYou

## Übersicht

"JustForYou" ist eine modulare Desktop-Anwendung, die verschiedene mathematische und technische Berechnungen unterstützt. Die Anwendung ist in Python entwickelt und nutzt das PySide6-Framework für die grafische Benutzeroberfläche (GUI). Sie bietet eine Vielzahl von Modulen, die dynamisch geladen werden können, um spezifische Funktionen bereitzustellen, wie z. B. Prozentrechnung, Kreditberechnung, Datenumrechnung und vieles mehr.

## Hauptfunktionen

- **Modulare Architektur**: Die Anwendung lädt Module dynamisch, die jeweils spezifische Funktionen bereitstellen.
- **Themenunterstützung**: Benutzer können zwischen verschiedenen GUI-Themen wechseln.
- **Schriftgrößenanpassung**: Die Schriftgröße der Anwendung kann angepasst werden.
- **Rechenhistorie**: Ergebnisse von Berechnungen werden gespeichert und können später eingesehen werden.
- **Verschiedene Module**:
  - Grundrechenarten
  - Prozentrechnung
  - Kreditberechnung
  - Datenumrechnung
  - Zahlensysteme
  - Schulnotenberechnung
  - Informationstechnik-Tools

## Installation

### Voraussetzungen

- Python 3.8 oder höher
- Abhängigkeiten aus der Datei `requirements.txt`

### Schritte

1. Klonen Sie das Repository:
   ```bash
   git clone <repository-url>
   cd JustForYou
   ```

2. Installieren Sie die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

3. Starten Sie die Anwendung:
   ```bash
   python src/main.py
   ```

## Module

### 1. **Grundrechenarten**
   - Addition, Subtraktion, Multiplikation und Division.
   - Unterstützt die Eingabe von mathematischen Ausdrücken.

### 2. **Prozentrechnung**
   - Berechnung von Prozentwerten, Prozentsätzen und Änderungen.
   - Unterstützt Funktionen wie "Prozent dazu" und "Prozent weg".

### 3. **Kreditberechnung**
   - Berechnung von monatlichen Raten, Gesamtkosten und Restschuld.
   - Unterstützt verschiedene Kreditarten wie Einmalzahlung und Ratenkredite.

### 4. **Datenumrechnung**
   - Umrechnung von Datenmengen zwischen verschiedenen Einheiten (z. B. Byte, KB, MB, GB).
   - Unterstützt Binär- und Dezimalpräfixe.

### 5. **Zahlensysteme**
   - Konvertierung zwischen Dezimal-, Binär-, Oktal- und Ternärsystemen.

### 6. **Schulnotenberechnung**
   - Berechnung von Durchschnittsnoten und Notenempfehlungen.
   - Unterstützt die Eingabe mehrerer Noten.

### 7. **Informationstechnik**
   - Tools zur Berechnung von Speichergrößen, Videodateigrößen und mehr.
   - Konvertierung von Zahlen und Text (z. B. ASCII zu Text).

### 8. **Rechenhistorie**
   - Speichert alle Berechnungen in einer verschlüsselten Datei.
   - Ermöglicht das Anzeigen und Aktualisieren der Historie.

## Bedienung

1. Starten Sie die Anwendung.
2. Wählen Sie ein Modul aus dem Menü "Load Module".
3. Führen Sie Berechnungen im ausgewählten Modul durch.
4. Wechseln Sie bei Bedarf das Thema oder passen Sie die Schriftgröße an.

## Themen und Anpassungen

- Die Anwendung unterstützt verschiedene GUI-Themen, die über das Menü "Settings > Select Theme" ausgewählt werden können.
- Die Schriftgröße kann über "Settings > Font Size" angepasst werden.

## Build-Anleitung

Um die Anwendung als ausführbare Datei zu erstellen, verwenden Sie PyInstaller:

1. Installieren Sie PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Erstellen Sie die ausführbare Datei:
   ```bash
   pyinstaller --onefile --windowed --add-data "src/modules;modules" src/main.py
   ```

3. Die ausführbare Datei befindet sich im Ordner `dist`.

## Tests

Die Anwendung enthält keine automatisierten Tests. Manuelle Tests können durch Ausführen der Module und Überprüfen der Ergebnisse durchgeführt werden.

## Projektstruktur

- **`src/`**: Enthält den Quellcode der Anwendung.
  - **`modules/`**: Enthält die Module der Anwendung.
  - **`helpers/`**: Hilfsfunktionen wie Parser, Historienmanager und Verschlüsselung.
- **`docs/`**: Dokumentation des Projekts, einschließlich Diagrammen.
- **`requirements.txt`**: Liste der Python-Abhängigkeiten.
- **`main.spec`**: PyInstaller-Spezifikationsdatei für den Build-Prozess.

## Lizenz

Dieses Projekt steht unter der GNU General Public License Version 3 (GPLv3). Weitere Informationen finden Sie in der Datei `LICENSE`.

## Mitwirkende

- **Projektleiter**: Gabriel
- **Entwickler**: Hugo
- **Product Owner**: Paul
