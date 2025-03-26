from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QComboBox
)
from math import floor


# -----------------------------
# Tab 1: Grafikspeicher / Videodateigröße
# -----------------------------
class VideoCalculatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grafikspeicher & Videodateigröße")
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.bitdepth_edit = QLineEdit()
        self.bitdepth_edit.setStyleSheet("font-size: 20px; padding: 10px; background: lightgray; border: 1px solid black;")
        form_layout.addRow("Farbtiefe (Bit):", self.bitdepth_edit)

        self.width_edit = QLineEdit()
        self.width_edit.setStyleSheet("font-size: 20px; padding: 10px; background: lightgray; border: 1px solid black;")
        form_layout.addRow("Breite (Pixel):", self.width_edit)

        self.height_edit = QLineEdit()
        self.height_edit.setStyleSheet("font-size: 20px; padding: 10px; background: lightgray; border: 1px solid black;")
        form_layout.addRow("Höhe (Pixel):", self.height_edit)

        self.fps_edit = QLineEdit()
        self.fps_edit.setStyleSheet("font-size: 20px; padding: 10px; background: lightgray; border: 1px solid black;")
        form_layout.addRow("Bilder/s:", self.fps_edit)

        # Optionale Eingabe: Videolänge in Sekunden (Default = 1 s)
        self.duration_edit = QLineEdit()
        self.duration_edit.setStyleSheet("font-size: 20px; padding: 10px; background: lightgray; border: 1px solid black;")
        self.duration_edit.setPlaceholderText("Standard: 1 Sekunde")
        form_layout.addRow("Videolänge (Sekunden):", self.duration_edit)

        layout.addLayout(form_layout)

        self.calc_button = QPushButton("Berechnen")
        layout.addWidget(self.calc_button)
        self.calc_button.clicked.connect(self.calculate)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

    def calculate(self):
        try:
            bitdepth = float(self.bitdepth_edit.text().replace(",", "."))
            width = float(self.width_edit.text().replace(",", "."))
            height = float(self.height_edit.text().replace(",", "."))
            fps = float(self.fps_edit.text().replace(",", "."))
        except ValueError:
            self.result_label.setText("Bitte gültige Zahlen für Farbtiefe, Breite, Höhe und Bilder/s eingeben.")
            return

        # Falls keine Videolänge angegeben wurde, wird 1 Sekunde angenommen.
        try:
            duration = float(self.duration_edit.text().replace(",", "."))
            if duration <= 0:
                duration = 1.0
        except ValueError:
            duration = 1.0

        # Berechnung der Gesamtzahl Bytes: (Pixel * Bytes/Pixel) * Bilder/s * Dauer
        bytes_total = width * height * (bitdepth / 8) * fps * duration

        # Umrechnung in Binärpräfix (1024er-Basis)
        if bytes_total >= 1024 ** 3:
            bin_value = bytes_total / (1024 ** 3)
            bin_unit = "GiB"
        elif bytes_total >= 1024 ** 2:
            bin_value = bytes_total / (1024 ** 2)
            bin_unit = "MiB"
        elif bytes_total >= 1024:
            bin_value = bytes_total / 1024
            bin_unit = "KiB"
        else:
            bin_value = bytes_total
            bin_unit = "Byte"

        # Umrechnung in Dezimalpräfix (10er-Basis)
        if bytes_total >= 1e9:
            dec_value = bytes_total / 1e9
            dec_unit = "GB"
        elif bytes_total >= 1e6:
            dec_value = bytes_total / 1e6
            dec_unit = "MB"
        elif bytes_total >= 1e3:
            dec_value = bytes_total / 1e3
            dec_unit = "KB"
        else:
            dec_value = bytes_total
            dec_unit = "Byte"

        result = (
            f"Berechnete Dateigröße (bei {duration} s Video):\n"
            f"{bin_value:.1f} {bin_unit} (Binärpräfix)\n"
            f"{dec_value:.1f} {dec_unit} (Dezimalpräfix)"
        )
        self.result_label.setText(result)


# -----------------------------
# Tab 2: Zahlensystem Umrechnungen
# -----------------------------
class ZahlensystemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zahlensysteme")
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.number_edit = QLineEdit()
        form_layout.addRow("Zahl:", self.number_edit)

        # Auswahl, in welchem System die Eingabe erfolgt
        self.input_system_combo = QComboBox()
        self.input_system_combo.addItems(["Dezimal", "Binär", "Ternär", "Oktal"])
        form_layout.addRow("Eingabesystem:", self.input_system_combo)

        layout.addLayout(form_layout)

        self.convert_button = QPushButton("Umrechnen")
        layout.addWidget(self.convert_button)
        self.convert_button.clicked.connect(self.convert)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

    def convert(self):
        system = self.input_system_combo.currentText()
        input_text = self.number_edit.text().strip()
        try:
            if system == "Dezimal":
                n = int(input_text, 10)
            elif system == "Binär":
                n = int(input_text, 2)
            elif system == "Ternär":
                n = int(input_text, 3)
            elif system == "Oktal":
                n = int(input_text, 8)
        except ValueError:
            self.result_label.setText("Bitte eine gültige Zahl im gewählten System eingeben.")
            return

        dec_str = str(n)
        bin_str = bin(n)[2:]
        oct_str = oct(n)[2:]
        tern_str = self.convert_to_ternary(n)

        result = (
            f"Dezimal: {dec_str}\n"
            f"Binär: {bin_str}\n"
            f"Ternär: {tern_str}\n"
            f"Oktal: {oct_str}"
        )
        self.result_label.setText(result)

    def convert_to_ternary(self, n):
        if n == 0:
            return "0"
        digits = []
        num = n
        while num:
            digits.append(str(num % 3))
            num //= 3
        return "".join(reversed(digits))


# -----------------------------
# Tab 3: Umrechnung von Datenmengen
# -----------------------------
class DatenmengenWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Datenmengen Umrechnungen")
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.value_edit = QLineEdit()
        form_layout.addRow("Menge:", self.value_edit)

        # Auswahl der Eingabeeinheit
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["Byte", "KB", "KiB", "MB", "MiB", "GB", "GiB"])
        form_layout.addRow("Einheit:", self.unit_combo)

        layout.addLayout(form_layout)

        self.convert_button = QPushButton("Umrechnen")
        layout.addWidget(self.convert_button)
        self.convert_button.clicked.connect(self.convert)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

    def convert(self):
        try:
            value = float(self.value_edit.text().replace(",", "."))
        except ValueError:
            self.result_label.setText("Bitte eine gültige Zahl eingeben.")
            return

        unit = self.unit_combo.currentText()
        # Umrechnung der Eingabe in Bytes
        if unit == "Byte":
            b = value
        elif unit == "KB":
            b = value * 1000
        elif unit == "KiB":
            b = value * 1024
        elif unit == "MB":
            b = value * 1000000
        elif unit == "MiB":
            b = value * (1024 ** 2)
        elif unit == "GB":
            b = value * 1000000000
        elif unit == "GiB":
            b = value * (1024 ** 3)
        else:
            b = value

        # Umrechnung in Binärpräfix (1024er-Basis)
        if b >= 1024 ** 3:
            bin_value = b / (1024 ** 3)
            bin_unit = "GiB"
        elif b >= 1024 ** 2:
            bin_value = b / (1024 ** 2)
            bin_unit = "MiB"
        elif b >= 1024:
            bin_value = b / 1024
            bin_unit = "KiB"
        else:
            bin_value = b
            bin_unit = "Byte"

        # Umrechnung in Dezimalpräfix (1000er-Basis)
        if b >= 1e9:
            dec_value = b / 1e9
            dec_unit = "GB"
        elif b >= 1e6:
            dec_value = b / 1e6
            dec_unit = "MB"
        elif b >= 1e3:
            dec_value = b / 1e3
            dec_unit = "KB"
        else:
            dec_value = b
            dec_unit = "Byte"

        result = (
            f"Eingegebene Datenmenge: {value:.3f} {unit}\n"
            f"Entspricht {b:.0f} Byte.\n\n"
            f"Umrechnung in Binärpräfix:\n{bin_value:.3f} {bin_unit}\n\n"
            f"Umrechnung in Dezimalpräfix:\n{dec_value:.3f} {dec_unit}"
        )
        self.result_label.setText(result)


# -----------------------------
# Hauptwidget mit Tabs
# -----------------------------
class InformationstechnikWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Informationstechnik Modul")
        # Tab 1: Video / Grafikspeicher
        self.addTab(VideoCalculatorWidget(), "Video & Grafikspeicher")
        # Tab 2: Zahlensysteme
        self.addTab(ZahlensystemWidget(), "Zahlensysteme")
        # Tab 3: Datenmengen
        self.addTab(DatenmengenWidget(), "Datenmengen")


# -----------------------------
# Modul-Informationen
# -----------------------------
MODULE_NAME = "Informationstechnik"
MODULE_DESCRIPTION = (
    "Modul für Berechnungen im Bereich Informationstechnik:\n"
    "- Grafikspeicher / Videodateigröße (Umrechnung in Binär- und Dezimalpräfixen),\n"
    "- Umrechnung zwischen Zahlensystemen (Eingabe in Dezimal, Binär, Ternär oder Oktal) und Ausgabe in allen Systemen sowie\n"
    "- Umrechnung von Datenmengen (Eingabe in verschiedenen Einheiten wie Byte, KB, KiB, MB, MiB, GB, GiB)."
)


def create_main_window():
    return InformationstechnikWidget()


MODULE_MAIN_WINDOW = create_main_window
