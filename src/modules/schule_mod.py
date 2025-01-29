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
            '>', ',', '='
        ]

        row = 0
        col = 0

        for button in buttons:
            btn = QPushButton(button)
            if button == '=':
                btn.clicked.connect(self.calculate)
            elif button == 'C':
                btn.clicked.connect(self.clearDisplay)
            else:
                btn.clicked.connect(partial(self.appendToDisplay, button))

            buttonsLayout.addWidget(btn, row, col)

            col += 1
            if col > 2:
                col = 0
                row += 1

        layout.addLayout(buttonsLayout)

        self.display2Label = QLabel()
        self.display2Label.setText('Anleitung')
        layout.addWidget(self.display2Label)

        self.display2 = QLineEdit()
        self.display2.setText('1. Geben Sie eine Note ein\n 2. Drucken Sie den Button ">" um weitere Noten einzugeben\n 3. Drucken Sie den Button "=" um die Endnote zu berechen\n 4. Die Endnote erscheint auf dem Display')
        self.display2.setMinimumSize(0, 150)
        self.display2.setReadOnly(True)
        layout.addWidget(self.display2)

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
