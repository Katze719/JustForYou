from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout
)
from src.helpers import historyManager
import pathlib
import json


class HistoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)

        self.historyManager = historyManager.HistoryManager()

        header_layout = QHBoxLayout()
        label = QLabel('Rechnungs-Historie:', self)
        header_layout.addWidget(label)

        # Refresh-Button
        refresh_button = QPushButton("Aktualisieren", self)
        refresh_button.clicked.connect(self.load_history)
        header_layout.addWidget(refresh_button)

        main_layout.addLayout(header_layout)

        # Tabelle für Rechnungsdaten
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Datum", "Ausdruck", "Ergebnis"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.table)

        self.load_history()  # Initiales Laden

    def load_history(self):
        history = self.historyManager.get_history()
        history.reverse()  # Neueste zuerst
        self.table.setRowCount(len(history))

        for row_index, entry in enumerate(history):
            self.table.setItem(row_index, 0, QTableWidgetItem(entry["date"]))
            self.table.setItem(row_index, 1, QTableWidgetItem(entry["expression"]))
            self.table.setItem(row_index, 2, QTableWidgetItem(str(entry["result"])))

        self.table.resizeColumnsToContents()

    def mousePressEvent(self, event):
        self.load_history()
        super().mousePressEvent(event)


MODULE_NAME = 'Historie'
MODULE_DESCRIPTION = 'Deine Historie'


# Funktion, die ein neues Widget erstellt
def create_main_window():
    return HistoryWidget()


MODULE_MAIN_WINDOW = create_main_window
