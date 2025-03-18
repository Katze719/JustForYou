from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
#from src.helpers import historyManager

class InvoiceHistoryWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        #self.historyManager = historyManager.HistoryManager("test.bin")

        label = QLabel('Rechnungs-Historie:', self)
        layout.addWidget(label)

        # Textbox für die Rechnungsdaten
        self.history_label = QLabel(self)
        self.history_label.setWordWrap(True)  # Zeilenumbruch aktivieren
        layout.addWidget(self.history_label)

        # Beispiel-Daten setzen
        self.set_invoice_history([
            ("2024-001", "01.03.2024", "100.00€"),
            ("2024-002", "05.03.2024", "250.50€"),
            ("2024-003", "10.03.2024", "75.00€"),
        ])

    def set_invoice_history(self, invoices):
        """Setzt die Rechnungsdaten als einfachen Text in die Label-Textbox."""
        #self.historyManager.add_entry("2 * 2", "4")
        #self.history_label.setText(str(self.historyManager.get_history()))
        pass

MODULE_NAME = 'start'
MODULE_DESCRIPTION = 'Just a simple hello world module'


# Funktion, die ein neues Widget erstellt
def create_main_window():
    return InvoiceHistoryWidget()


MODULE_MAIN_WINDOW = create_main_window
