import re
import math
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QGridLayout, QPushButton, QTextEdit
from PySide6.QtCore import Qt
from src.helpers import parser, historyManager


class BaseWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.history_manager = historyManager.HistoryManager()

        self.parser = parser.CalculatorParser()

        # Hauptlayout
        main_layout = QVBoxLayout(self)

        # Eingabefeld
        self.input_display = QLineEdit("0")
        self.input_display.setStyleSheet("font-size: 20px; padding: 7px;")
        self.input_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self.input_display)

        # Ausgabefeld
        self.output_display = QLabel('', self)
        self.output_display.setStyleSheet(
            "font-size: 20px; padding: 10px; background: lightgray; border: 1px solid black;")
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
            ('√', 0, 4), ('!', 1, 4), ('^', 2, 4), ('UDb', 3, 4),
            ('=', 4, 5),
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
            "UDb... umwandlung zu Dezimalbruch"
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

        if text == 'PzG':
            if 'PzG' in current_text:
                text = ' | '
            else:
                text = text + ' '

        if current_text == '0':
            current_text = ''

        if text != '=':
            current_text = current_text + text
            self.input_display.setText(current_text)

        try:
            # Parse und evaluiere den Ausdruck
            if 'PzG' in current_text:
                result = self.parse_prime_numbers(current_text)
            elif 'UDb' in current_text:
                result = self.umwandlung_in_bruch(current_text)
            else:

                preparsed_expression = self.parse_square_root(current_text)
                preparsed_expression = self.parse_factorial(preparsed_expression)
                preparsed_expression = self.parse_prime_numbers(preparsed_expression)
                preparsed_expression = self.parse_exponetial(preparsed_expression)
                parsed_expression = self.parser.parse_and_calculate(preparsed_expression)
                result = eval(parsed_expression)
                print(f"parsed:{parsed_expression}")

            self.output_display.setText(f"{result}")
            print(2)
            if text == '=':
                self.history_manager.add_entry(self.input_display.text(), self.output_display.text())
                self.input_display.setText(self.output_display.text())
        except Exception as E:
            print(f"error_main... {E}")
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
        if '!' in text_to_parse:
            print(1)
            pattern_no_bracket = r"(?P<before_expression>.*)\s*(?P<match>[\d\.]+)!(?P<after_expression>.*)"
            pattern_bracket = r"(?P<before_expression>.*)\s*(?P<match>\(.*\))!(?P<after_expression>.*)"
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

    def parse_prime_numbers(self, text_to_parse):
        pattern = "PzG\s(\d*)\s\|\s(\d*)"

        if 'PzG' in text_to_parse:
            output = []
            text_to_parse.replace('=', '')
            match = re.findall(pattern, text_to_parse)[0]
            print(match)
            try:
                for x in range(int(match[0]), int(match[1])):
                    prime_flag = True
                    if x == 1:
                        continue  # No prime numbers

                    for y in range(int(match[0]), x):
                        if x == y or y == 1:
                            continue
                        if x % y == 0:
                            prime_flag = False

                    if prime_flag:
                        output.append(x)
                output = str(output).replace(',', ' ')
                output = output.replace('[', '')
                output = output.replace(']', '')
                return output
            except Exception as E:
                print(E)
        else:
            return text_to_parse

    def parse_exponetial(self, text_to_parse):
        pattern = r'(\d+)\s*\^\s*(\d+)'
        try:
            print(text_to_parse)
            if '^' in text_to_parse:
                match = re.findall(pattern, text_to_parse)[0]
                print(match)
                output = int(match[0])

                for x in range(1, int(match[1])):
                    output = output * int(match[0])
                    print(output)

                print(text_to_parse.replace(f'{match[0]}^{match[1]}', str(output)))

                return text_to_parse.replace(f'{match[0]}^{match[1]}', str(output))

            else:
                return text_to_parse

        except Exception as E:
            print(f'exponetial...{E}')

    def umwandlung_in_bruch(self, text_to_parse):
        pattern = r'UDb\s*([\d.]+)'

        match = re.findall(pattern, text_to_parse)
        print(match)

        result = float(match[0]).as_integer_ratio()

        result = f'{result[0]}/{result[1]}'

        return result


# Funktion, die ein neues Widget erstellt
def create_main_window():
    return BaseWidget()


MODULE_MAIN_WINDOW = create_main_window
MODULE_NAME = 'Math Modul'
MODULE_DESCRIPTION = 'Erweiterte mathematische Funktionen'
