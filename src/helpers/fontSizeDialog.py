from PySide6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QSlider,
    QLabel,
    QDialog,
)

from PySide6.QtCore import Qt

class FontSizeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adjust Font Size")
        self.layout = QVBoxLayout(self)

        self.font_size_label = QLabel(f"Font Size: {parent.font_size}", self)
        self.layout.addWidget(self.font_size_label)

        self.font_slider = QSlider(Qt.Horizontal, self)
        self.font_slider.setMinimum(8)
        self.font_slider.setMaximum(1000)
        self.font_slider.setValue(parent.font_size)
        self.font_slider.valueChanged.connect(lambda value: parent.change_font_size(value, self.font_size_label))
        self.layout.addWidget(self.font_slider)

        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)