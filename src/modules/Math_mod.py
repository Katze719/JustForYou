import re
import math
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QTextEdit
from PySide6.QtCore import Qt
from src.helpers import parser


class BaseWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.parser = parser.CalculatorParser()

        # Hauptlayout
        main_layout = QVBoxLayout(self)

        # Eingabefeld
        self.input_display = QLabel('0', self)
        self.input_display.setStyleSheet(
            "font-size: 20px; padding: 10px; background: lightgray; border: 1px solid black;")
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
            ('CE', 0, 0), ('C', 0, 1), ('(', 0, 2), (')', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('±', 4, 2), ('/', 4, 3),
            ('√', 0, 4), ('!', 1, 4), ('=', 4, 5),
            ('PzG', 0, 5), ('Bruch', 1, 5), ('COPY', 2, 5), ('PASTE', 3, 5),
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
            "PzG... Primzahlen zwischen Grenzwerten"
        )
        help_layout.addWidget(help_text)

        main_layout.addLayout(help_layout)

    def on_button_click(self, text):
        current_text = self.input_display.text()

        if text == ' ':
            return

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

        if current_text == '0':
            current_text = ''

        if text != '=':
            current_text = current_text + text
            self.input_display.setText(current_text)

        try:
            # Parse und evaluiere den Ausdruck
            preparsed_expression = self.parse_square_root(current_text)
            print(preparsed_expression)
            preparsed_expression = self.parse_factorial(preparsed_expression)
            print(preparsed_expression)
            parsed_expression = self.parser.parse_and_calculate(preparsed_expression)

            print(f"parsed:{parsed_expression}")

            result = eval(parsed_expression)
            self.output_display.setText(f"{result:.2f}")

            if text == '=':
                self.input_display.setText(self.output_display.text())
        except Exception:
            print(f"error")
            self.output_display.setText("...")

    def parse_square_root(self, text_to_parse):

        if '√' in text_to_parse:
            pattern_no_bracket = r"(?P<before_expression>.*)√\s*(?P<match>[\d\.]+)(?P<after_expression>.*)"
            pattern_bracket = r"(?P<before_expression>.*)√\s*(?P<match>\(.*\))(?P<after_expression>.*)"
            text_to_parse.replace('=', '')
            print(text_to_parse)

            try:
                if '(' in text_to_parse:
                    match = re.findall(pattern_bracket, text_to_parse)[0]
                else:
                    match = re.findall(pattern_no_bracket, text_to_parse)[0]

                print(match)
                sqrt = f'math.sqrt({match[1]})'

            except Exception as E:
                print(E)

            return f'{match[0]} {sqrt} {match[2]}'
        else:
            return text_to_parse

    def parse_factorial(self, text_to_parse):

        print(text_to_parse, 'test')
        if '!' in text_to_parse:
            print(1)
            pattern_no_bracket = r"(?P<before_expression>.*)!\s*(?P<match>[\d\.]+)(?P<after_expression>.*)"
            pattern_bracket = r"(?P<before_expression>.*)!\s*(?P<match>\(.*\))(?P<after_expression>.*)"
            text_to_parse.replace('=', '')
            try:
                if '(' in text_to_parse:
                    match = re.findall(pattern_bracket, text_to_parse)[0]
                else:
                    match = re.findall(pattern_no_bracket, text_to_parse)[0]

            except Exception as E:
                print(f"error factorial: {E}")
            print(match)

            result = 1

            for x in range(1, int(match[1]) + 1):
                result = result * x

            text_to_parse = f'{match[0]} {result} {match[2]}'

            return text_to_parse
        else:
            return text_to_parse


# Funktion, die ein neues Widget erstellt
def create_main_window():
    return BaseWidget()


MODULE_MAIN_WINDOW = create_main_window
MODULE_NAME = 'Math Modul'
MODULE_DESCRIPTION = 'Copy from Base'