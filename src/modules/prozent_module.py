from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QApplication
from PySide6.QtCore import Qt
import re

class ProzentCalcWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Hauptlayout
        main_layout = QVBoxLayout(self)

        # Eingabefeld
        self.input_display = QLabel('0', self)
        self.input_display.setStyleSheet("font-size: 20px; padding: 10px; background: lightgray; border: 1px solid black;")
        self.input_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self.input_display)

        # Ausgabefeld
        self.output_display = QLabel('', self)
        self.output_display.setStyleSheet("font-size: 20px; padding: 10px; background: gray; border: 1px solid black;")
        self.output_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self.output_display)

        # Grid für die Buttons
        button_grid = QGridLayout()
        buttons = [
            ('CE', 0, 0), ('C', 0, 1), ('±', 0, 2), ('Brutto', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('von', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('%', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('%-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('%+', 4, 2), ('=', 4, 3),
            ('Netto', 0, 4), ('COPY', 1, 4), ('PASTE', 2, 4)
        ]

        for text, row, col in buttons:
            button = QPushButton(text, self)
            button.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            button_grid.addWidget(button, row, col)

        main_layout.addLayout(button_grid)

        # Hilfe-Bereich
        help_layout = QVBoxLayout()
        help_label = QLabel("Hilfe", self)
        help_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        help_layout.addWidget(help_label)

        help_text = QTextEdit(self)
        help_text.setReadOnly(True)
        help_text.setText(
            "% : Prozent von\n"
            "%+ : Prozent dazu\n"
            "%- : Prozent weg\n"
            "von : macht aus zwei Zahlen einen Prozentwert\n"
            "Brutto : Wandelt den Wert in Brutto um\n"
            "Netto : Wandelt den Wert in Netto um"
        )
        help_layout.addWidget(help_text)

        main_layout.addLayout(help_layout)

    def parse_expression(self, expression):
        # Bearbeite verschachtelte Klammern zuerst
        while '(' in expression:
            expression = re.sub(r'\(([^()]+)\)', lambda m: self.parse_expression(m.group(1)), expression)

        # Unterstützung für negative Zahlen in Operatoren
        expression = re.sub(r'(-?\d+(\.\d+)?)\s*%\+\s*(-?\d+(\.\d+)?)', r'(\1 + (\1 * \3 / 100))', expression)
        expression = re.sub(r'(-?\d+(\.\d+)?)\s*%-\s*(-?\d+(\.\d+)?)', r'(\1 - (\1 * \3 / 100))', expression)
        expression = re.sub(r'(-?\d+(\.\d+)?)\s*%\s*(-?\d+(\.\d+)?)', r'(\1 * \3 / 100)', expression)
        expression = re.sub(r'(-?\d+(\.\d+)?)\s*von\s*(-?\d+(\.\d+)?)', r'((\1 / \3) * 100)', expression)

        return expression

    def on_button_click(self, text):
        current_text = self.input_display.text()
        print(text)

        if text == "COPY":
            QApplication.clipboard().setText(self.output_display.text())
            return
        if text == "PASTE":
            if current_text == '0':
                current_text = QApplication.clipboard().text()
            else:
                current_text = self.input_display.text() + QApplication.clipboard().text()
            text = ""

        if text in {'C', 'CE'}:
            self.input_display.setText('0')
            self.output_display.setText('')
            return

        if text == '±':
            if current_text.startswith('-'):
                self.input_display.setText(current_text[1:])
            else:
                self.input_display.setText(f"-{current_text}")
            return

        if text == 'Brutto':
            self.input_display.setText(f"{float(current_text) * 1.19:.2f}")
            return
        if text == 'Netto':
            self.input_display.setText(f"{float(current_text) / 1.19:.2f}")
            return

        if current_text == '0':
            current_text = ''

        if text != '=':
            current_text = current_text + text
            self.input_display.setText(current_text)

        try:
            # Parse und evaluiere den Ausdruck
            parsed_expression = self.parse_expression(current_text)
            print(f"parsed:{parsed_expression}")
            result = eval(parsed_expression)
            self.output_display.setText(f"{result:.2f}")

            if text == '=':
                self.input_display.setText(self.output_display.text())
        except Exception:
            print("error")
            self.output_display.setText("...")



MODULE_NAME='Prozentrechnung'
MODULE_DESCRIPTION='Berechne Prozente'


# Funktion, die ein neues Widget erstellt
def create_main_window():
    return ProzentCalcWidget()


MODULE_MAIN_WINDOW = create_main_window
