classDiagram
    class Rechner {
        +List~Modul~ modulListe
        +List~Rechnungsprotokoll~ protokoll
        +Date aktuellesDatum
        +starteModul(name: String)
        +beendeModul()
        +speichereErgebnis(protokoll: Rechnungsprotokoll)
    }

    class Modul {
        <<abstract>>
        +String name
        +String version
        +starte()
        +beende()
    }
    Rechner --> Modul
    Modul <|-- GrundrechenartenModul
    Modul <|-- ProzentRechenModul
    Modul <|-- KreditBerechnungModul
    Modul <|-- GeometrieModul
    Modul <|-- MathematischeFunktionenModul
    Modul <|-- SchuleModul
    Modul <|-- InformationstechnikModul

    class Rechnungsprotokoll {
        +String operation
        +List~String~ parameter
        +String ergebnis
        +Date zeitstempel
        +zeigeProtokoll()
    }
    Rechner --> Rechnungsprotokoll

    class Eingabemodul {
        +String parameterBezeichnung
        +String eingabewert
        +prüfeEingabe()
        +liefereWert()
    }
    Modul --> Eingabemodul

    class GUI {
        +String layout
        +String schriftart
        +Integer schriftgröße
        +String hintergrundfarbe
        +zeigeStartFenster()
        +zeigeModulFenster(modul: Modul)
        +anpassungSpeichern()
    }
    Rechner --> GUI

    class ModulInterface {
        <<interface>>
        +starteFunktion(funktionName: String)
        +liefereErgebnis()
    }
    Modul --> ModulInterface

    class DateiSpeicher {
        +speichere(protokoll: List~Rechnungsprotokoll~)
        +lade()
    }
    Rechner --> DateiSpeicher
