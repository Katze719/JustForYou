import pathlib
import sys
import types

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import importlib.util


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Hauptlayout des Fensters
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

    def load_module_from_anywhere(self, path: pathlib.Path, module_name: str) -> types.ModuleType:
        """
        Import a module at runtime from a directory.
        :param path: the modules directory
        :param module_name: the name of the module to load
        :return: the loaded module
        """
        spec = importlib.util.spec_from_file_location(module_name, str(path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_name] = module
        return module


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Erstelle das Hauptfenster
    window = MainWindow()

    # Modul dynamisch laden und zum Layout hinzufügen
    modules_path = pathlib.Path(__file__).resolve().parent / pathlib.Path('modules') / pathlib.Path('__init__.py')
    example_mod = window.load_module_from_anywhere(path=modules_path, module_name='modules')
    widget = example_mod.hello_world.HelloWorldWidget()
    window.setCentralWidget(widget)

    window.show()
    sys.exit(app.exec_())