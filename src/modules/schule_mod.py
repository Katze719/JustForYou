import sys
from functools import partial
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication,  QGridLayout, QPushButton, QLineEdit, QTextEdit
from PySide6.QtCore import Qt

tempNumber = 0
numbersCount = 0
lastNumberInput = 0

class SchoolWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # Eingabefeld
        self.input_display = QLineEdit("0")
        self.input_display.setStyleSheet("font-size: 20px; padding: 10px;")
        self.input_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.input_display)

        # Ausgabefeld
        self.output_display = QLabel('', self)
        self.output_display.setStyleSheet("font-size: 20px; padding: 10px; background: lightgray; border: 1px solid black;")
        self.output_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.output_display)

        # Ausgabefeld2
        self.output_display2 = QLabel('', self)
        self.output_display2.setStyleSheet("font-size: 20px; padding: 10px; background: lightgray; border: 1px solid black;")
        self.output_display2.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.output_display2)

        # Ausgabefeld3
        self.output_display3 = QLabel('', self)
        self.output_display3.setStyleSheet("font-size: 20px; padding: 10px; background: lightgray; border: 1px solid black;")
        self.output_display3.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.output_display3)

        buttonsLayout = QGridLayout()

        buttons = [
            '', 'CE', 'C',
            '4', '5', '6',
            '1', '2', '3',
            '', '+', '='
        ]

        row = 0
        col = 0

        for button in buttons:
            btn = QPushButton(button)
            if button == '=':
                btn.clicked.connect(self.calculate)
            elif button == 'C':
                btn.clicked.connect(self.clearAll)
            elif button == 'CE':
                btn.clicked.connect(self.clearDisplay)
            elif button == '+':
                btn.clicked.connect(partial(self.addMoreNumbers, button))
            else:
                btn.clicked.connect(partial(self.appendToDisplay, button))

            buttonsLayout.addWidget(btn, row, col)

            col += 1
            if col > 2:
                col = 0
                row += 1

        layout.addLayout(buttonsLayout)

        # Hilfe-Bereich
        help_layout = QVBoxLayout()
        help_label = QLabel("Hilfe", self)
        help_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        help_layout.addWidget(help_label)

        help_text = QTextEdit(self)
        help_text.setReadOnly(True)
        help_text.setText(
            "Bedienung\n"
            "1. Geben Sie eine Note ein\n"
            "2. Drucken Sie den Button \"+\" um weitere Noten einzugeben\n"
            "3. Drucken Sie den Button \"=\" um die Endnote zu berechen\n"
            "4. Die Endnote erscheint auf dem Display\n"
            "\n"
            "Hinweise\n"
            "Feld 1 =  Die eingebenen Noten\n"
            "Feld 2 =  Die Durchschnittsnote\n"
            "Feld 3 =  Die Notenempfehlung\n"
            "Feld 4 =  Die Anzahl der eingegebenen Noten\n"

        )
        help_layout.addWidget(help_text)

        layout.addLayout(help_layout)

    def appendToDisplay(self, char):

        if self.input_display.text() == "0":
            self.input_display.setText("")

        self.input_display.setText(self.input_display.text() + char)

        global tempNumber
        tempNumber = tempNumber + int(char)

        global numbersCount
        numbersCount = numbersCount + 1

        global lastNumberInput
        lastNumberInput = int(char)

    def calculate(self):
        try:
            global numbersCount

            self.output_display.setText(str(tempNumber / numbersCount))
            self.output_display2.setText(str(round(tempNumber / numbersCount)))
            self.output_display3.setText(str(numbersCount))
        except Exception as e:
            self.input_display.setText("Error")

    def clearAll(self):
        self.input_display.clear()
        self.output_display.clear()
        self.output_display2.clear()
        self.output_display3.clear()

        global tempNumber
        tempNumber = 0

        global numbersCount
        numbersCount = 0

    def clearDisplay(self):
        global tempNumber
        global lastNumberInput
        global numbersCount

        if lastNumberInput == "+":
            self.input_display.setText(self.input_display.text()[:-1])
            return

        tempNumber = tempNumber - lastNumberInput
        numbersCount = numbersCount - 1

    def addMoreNumbers(self, char):
        self.input_display.setText(self.input_display.text() + char)
        global lastNumberInput
        lastNumberInput = "+"

MODULE_NAME = 'Schule'
MODULE_DESCRIPTION = 'Berechnet die Noten der Schueler'

def create_main_window():
    return SchoolWidget()


MODULE_MAIN_WINDOW = create_main_window
