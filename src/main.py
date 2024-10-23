import pathlib
import pkgutil
import sys
import types

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
import importlib.util


class ModulesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.__modules_path = pathlib.Path(__file__).resolve().parent / pathlib.Path('modules') / pathlib.Path(
            '__init__.py')
        self.__available_modules = self.__get_available_modules()

        for module_name in self.__available_modules:
            button = QPushButton(text=module_name, parent=self)
            button.clicked.connect(lambda checked: self.__load_module(module_name=module_name))
            layout.addWidget(button)

    def __load_module(self, module_name: str) -> types.ModuleType:
        """
        Import a module at runtime from a directory.
        :param module_name: the name of the module to load
        :return: the loaded module
        """
        try:
            spec = importlib.util.spec_from_file_location(module_name, str(self.__modules_path))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.modules[module_name] = module
            print(f'loaded module: {module_name}')
            return module
        except ImportError as e:
            print(f'failed to load module {module_name}: {e}')

    def __get_available_modules(self) -> list[str]:
        modules = self.__load_module('modules')
        return [name for _, name, _ in pkgutil.iter_modules(modules.__path__)]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Hauptlayout des Fensters
        self.central_widget = ModulesWidget(parent=self)
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Erstelle das Hauptfenster
    window = MainWindow()

    window.show()
    sys.exit(app.exec())
