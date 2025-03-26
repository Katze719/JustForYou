import re
import math

class CalculatorParser:
    def __init__(self):
        self.valid_pattern = re.compile(r"^[0-9+\-*/(). ]+|math\.sqrt\([0-9a-zA-Z\.\-\+\*\/\(\) ]*\)$")

    def parse_and_calculate(self, expression: str) -> str:
        if not self.valid_pattern.match(expression):
            return "Ungültiger Ausdruck"
        try:
            print(f'parsing: {expression}')
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Fehler: {e}"
