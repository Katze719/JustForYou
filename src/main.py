import sys
import pathlib
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
)
from PySide6.QtGui import QIcon
from helpers.modulesLoaderWidget import ModulesLoaderWidget
from qt_material import apply_stylesheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Hauptlayout des Fensters
        self.central_widget = ModulesLoaderWidget(parent=self)
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("JustForYou - Calc")
    app.setOrganizationName("XYZ")
    app.setApplicationVersion("0.1.0")

    main_window = QMainWindow()
    main_window.setWindowIcon(QIcon(f"{pathlib.Path(__file__).parent}/pics/icon.png"))
    modules_widget = ModulesLoaderWidget()
    main_window.setCentralWidget(modules_widget)
    apply_stylesheet(main_window, 'dark_purple.xml', invert_secondary=True)
    main_window.show()
    sys.exit(app.exec())