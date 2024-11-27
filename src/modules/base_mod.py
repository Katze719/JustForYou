from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class BaseWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel('Based', self)
        layout.addWidget(label)


MODULE_NAME='Base Module'
MODULE_DESCRIPTION='Das base rechen modul'


# Funktion, die ein neues Widget erstellt
def create_main_window():
    return BaseWidget()


MODULE_MAIN_WINDOW = create_main_window
