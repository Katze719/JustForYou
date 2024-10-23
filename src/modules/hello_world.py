from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class HelloWorldWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel('Hello World', self)
        layout.addWidget(label)