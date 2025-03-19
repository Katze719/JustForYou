import json
import pathlib
from typing import List, Dict, Any
from src.helpers import AES


class HistoryManager:
    def __init__(self, history_file: str):
        self.historyFile = pathlib.Path(history_file)
        if not self.historyFile.exists():
            self._save([])  # Falls Datei nicht existiert, leere Liste speichern

    def _save(self, data: List[Dict[str, Any]]):
        """Speichert die History-Daten in die JSON-Datei."""
        AES.encrypt_json(data, "pw", str(self.historyFile))

    def _load(self) -> List[Dict[str, Any]]:
        """Lädt die History-Daten aus der JSON-Datei."""
        try:
            return AES.decrypt_json("pw", str(self.historyFile))
        except (json.JSONDecodeError, FileNotFoundError):
            return []  # Falls Datei leer oder defekt ist

    def add_entry(self, expression: str, result: Any):
        """Fügt eine neue Rechnung zur History hinzu."""
        history = self._load()
        history.append({"expression": expression, "result": result})
        self._save(history)

    def get_history(self) -> List[Dict[str, Any]]:
        """Gibt die gespeicherte Rechnungs-History zurück."""
        return self._load()

    def clear_history(self):
        """Löscht die gesamte Rechnungs-History."""
        self._save([])


if __name__ == "__main__":
    a = HistoryManager("./test.bin")
