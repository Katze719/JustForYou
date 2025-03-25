from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QTextEdit
from src.helpers import historyManager
import pathlib
import json


class InvoiceHistoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.historyManager = historyManager.HistoryManager()

        label = QLabel('Rechnungs-Historie:', self)
        layout.addWidget(label)

        # Textbox für die Rechnungsdaten
        self.history_label = QTextEdit(self)
        self.history_label.setReadOnly(True)
        layout.addWidget(self.history_label)

        self.history_label.setText(self.historyManager.get_history_fmt())


MODULE_NAME = 'start'
MODULE_DESCRIPTION = 'Deine Historie'


# Funktion, die ein neues Widget erstellt
def create_main_window():
    return InvoiceHistoryWidget()


MODULE_MAIN_WINDOW = create_main_window
