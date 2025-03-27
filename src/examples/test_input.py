from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from src.helpers import parser


class TestInput(QWidget):
    def __init__(self):
        super().__init__()
        self.parser = parser.CalculatorParser()

        layout = QVBoxLayout(self)

        self.label = QLabel('Parse :D', self)
        layout.addWidget(self.label)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Gib einen mathematischen Ausdruck ein...")
        layout.addWidget(self.input_field)

        self.button = QPushButton("Berechnen", self)
        self.button.clicked.connect(self.process_input)
        layout.addWidget(self.button)

    def process_input(self):
        input_text = self.input_field.text()
        result = self.parser.parse_and_calculate(input_text)
        self.label.setText(f"Ergebnis: {result}")


MODULE_NAME='Test Input'
MODULE_DESCRIPTION='For testing the parser'


# Funktion, die ein neues Widget erstellt
def create_main_window():
    return TestInput()


MODULE_MAIN_WINDOW = create_main_window
