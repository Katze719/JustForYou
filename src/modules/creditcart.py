from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QFormLayout, QTextEdit
)
from src.helpers import historyManager
from math import log, ceil


class KreditrechnerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kreditrechner")
        layout = QVBoxLayout(self)

        self.history_manager = historyManager.HistoryManager()

        # Formular für Eingaben
        form_layout = QFormLayout()

        self.credit_type_combo = QComboBox()
        self.credit_type_combo.addItems([
            "Einmalige Rückzahlung",
            "Ratenkredit (Laufzeit vorgegeben)",
            "Ratenkredit (Rate vorgegeben)"
        ])
        form_layout.addRow("Kreditart:", self.credit_type_combo)

        self.amount_edit = QLineEdit()
        form_layout.addRow("Kreditbetrag (€):", self.amount_edit)

        self.interest_edit = QLineEdit()
        form_layout.addRow("Zinssatz (% p.a.):", self.interest_edit)

        # Eingabefelder für Laufzeit bzw. Rate
        self.duration_label = QLabel("Laufzeit (Monate):")
        self.duration_edit = QLineEdit()
        form_layout.addRow(self.duration_label, self.duration_edit)

        self.rate_label = QLabel("Rate (€/Monat):")
        self.rate_edit = QLineEdit()
        form_layout.addRow(self.rate_label, self.rate_edit)

        layout.addLayout(form_layout)

        # Button zur Berechnung
        self.calc_button = QPushButton("Berechnen")
        layout.addWidget(self.calc_button)

        # Ausgabe-Label
        self.result_label = QTextEdit(self)
        self.result_label.setReadOnly(True)
        layout.addWidget(self.result_label)

        # Signale verbinden
        self.calc_button.clicked.connect(self.calculate)
        self.credit_type_combo.currentIndexChanged.connect(self.update_fields)
        self.update_fields(self.credit_type_combo.currentIndex())

    def update_fields(self, index):
        """
        Schaltet die Eingabefelder ein/aus:
         - Bei "Einmalige Rückzahlung" und "Ratenkredit (Laufzeit vorgegeben)" wird die Laufzeit benötigt.
         - Bei "Ratenkredit (Rate vorgegeben)" wird stattdessen die Rate benötigt.
        """
        if index in [0, 1]:
            self.duration_edit.setEnabled(True)
            self.duration_label.setEnabled(True)
            self.rate_edit.setEnabled(False)
            self.rate_label.setEnabled(False)
        else:
            self.duration_edit.setEnabled(False)
            self.duration_label.setEnabled(False)
            self.rate_edit.setEnabled(True)
            self.rate_label.setEnabled(True)

    def calculate(self):
        try:
            principal = float(self.amount_edit.text().replace(",", "."))
            interest_rate = float(self.interest_edit.text().replace(",", "."))
        except ValueError:
            self.result_label.setText("Bitte gültige Zahlen für Kreditbetrag und Zinssatz eingeben.")
            return

        credit_type = self.credit_type_combo.currentIndex()
        result_text = ""

        if credit_type == 0:
            # Einmalige Rückzahlung: Zinsen = Kreditbetrag * Zinssatz * (Laufzeit/12)
            try:
                months = int(self.duration_edit.text())
            except ValueError:
                self.result_label.setText("Bitte gültige Zahl für Laufzeit (Monate) eingeben.")
                return
            total_interest = principal * (interest_rate / 100) * (months / 12)
            result_text = (
                f"Einmalige Rückzahlung:\n"
                f"Kreditbetrag: {principal:.2f}€, Zinssatz: {interest_rate:.2f}% p.a., Laufzeit: {months} Monate\n"
                f"Zinsen gesamt: {total_interest:.2f}€"
            )

        elif credit_type == 1:
            # Ratenkredit, Laufzeit vorgegeben (Annuitätendarlehen)
            try:
                months = int(self.duration_edit.text())
            except ValueError:
                self.result_label.setText("Bitte gültige Zahl für Laufzeit (Monate) eingeben.")
                return
            r = interest_rate / 100 / 12  # monatlicher Zinssatz
            if r == 0:
                installment = principal / months
            else:
                installment = principal * (r * (1 + r) ** months) / ((1 + r) ** months - 1)
            total_interest = installment * months - principal
            result_text = (
                f"Ratenkredit (Laufzeit vorgegeben):\n"
                f"Kreditbetrag: {principal:.2f}€, Zinssatz: {interest_rate:.2f}% p.a., Laufzeit: {months} Monate\n"
                f"Monatsrate: {installment:.2f}€\n"
                f"Zinsen gesamt: {total_interest:.2f}€"
            )

        elif credit_type == 2:
            # Ratenkredit, Rate vorgegeben: Simuliere die Tilgung
            try:
                monthly_payment = float(self.rate_edit.text().replace(",", "."))
            except ValueError:
                self.result_label.setText("Bitte gültige Zahl für Rate (€/Monat) eingeben.")
                return
            r = interest_rate / 100 / 12  # monatlicher Zinssatz

            months, total_interest = self.simulate_credit_with_rate(principal, r, monthly_payment)
            result_text = (
                f"Ratenkredit (Rate vorgegeben):\n"
                f"Kreditbetrag: {principal:.2f}€, Zinssatz: {interest_rate:.2f}% p.a., Monatsrate: {monthly_payment:.2f}€\n"
                f"Laufzeit: {months} Monate\n"
                f"Zinsen gesamt: {total_interest:.2f}€"
            )

        self.result_label.setText(result_text)

    def simulate_credit_with_rate(self, principal, monthly_rate, monthly_payment):
        """
        Simuliert die Rückzahlung eines Kredits mit fester Rate.
        Pro Monat werden zuerst die Zinsen berechnet. Dann wird der
        fällige Betrag (Restschuld + Zinsen) ermittelt, und es wird der
        kleinere Betrag aus Monatsrate und fälligem Betrag bezahlt.
        Es werden die gezahlten Zinsen aufsummiert.
        """
        total_interest = 0.0
        months = 0
        while principal > 1e-6:
            interest = principal * monthly_rate
            due = principal + interest
            effective_payment = monthly_payment if monthly_payment < due else due
            principal_reduction = effective_payment - interest
            principal -= principal_reduction
            total_interest += interest
            months += 1
            if months > 50000:
                # Schutz vor endloser Schleife, falls Rate zu niedrig ist
                self.result_label.setText("Laufzeit zu lang, bitte überprüfen Sie die Eingabe der Rate.")
                raise ValueError("Laufzeit zu lang, bitte überprüfen Sie die Eingabe der Rate.")
        return months, total_interest


# Modul-Informationen
MODULE_NAME = 'Kreditrechner'
MODULE_DESCRIPTION = (
    'Modul zur Berechnung von Krediten. Unterstützt: '
    'Einmalige Rückzahlung, Ratenkredit mit vorgegebener Laufzeit und '
    'Ratenkredit mit vorgegebener Rate.'
)


def create_main_window():
    return KreditrechnerWidget()


MODULE_MAIN_WINDOW = create_main_window
