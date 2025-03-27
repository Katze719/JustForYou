from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class HelloWorldWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel('Hello World', self)
        layout.addWidget(label)


MODULE_NAME='Hello World'
MODULE_DESCRIPTION='Just a simple hello world module'


# Funktion, die ein neues Widget erstellt
def create_main_window():
    return HelloWorldWidget()


MODULE_MAIN_WINDOW = create_main_window
