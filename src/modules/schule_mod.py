import sys
from functools import partial
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication,  QGridLayout, QPushButton, QLineEdit

class SchoolWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        layout.addWidget(self.display)

        buttonsLayout = QGridLayout()

        buttons = [
            '', 'CE', 'C',
            '4', '5', '6',
            '1', '2', '3',
            '0', ',', '', '='
        ]

        row = 0
        col = 0
        ord = 0

        for button in buttons:
            btn = QPushButton(button)
            if button == '=':
                btn.clicked.connect(self.calculate)
            elif button == 'C':
                btn.clicked.connect(self.clearDisplay)
            else:
                btn.clicked.connect(partial(self.appendToDisplay, button))

            buttonsLayout.addWidget(btn, row, col)
            ## mudar aqui depois para adcionar o = grande
            col += 1
            if col > 2:
                col = 0
                row += 1

        layout.addLayout(buttonsLayout)
        self.setLayout(layout)

    def appendToDisplay(self, char):
        self.display.setText(self.display.text() + char)

    def calculate(self):
        try:
            result = eval(self.display.text())
            self.display.setText(str(result))
        except Exception as e:
            self.display.setText("Error")

    def clearDisplay(self):
        self.display.clear()

MODULE_NAME = 'Schule'
MODULE_DESCRIPTION = 'Berechnet die Noten der Schueler'

def create_main_window():
    return SchoolWidget()


MODULE_MAIN_WINDOW = create_main_window
