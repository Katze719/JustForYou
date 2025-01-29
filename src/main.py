import importlib.util
import pathlib
import pkgutil
import sys
import types
import typing

from helpers.fontSizeDialog import FontSizeDialog

from dto import ModuleInfo

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QMenu,
    QMenuBar,
)

from PySide6.QtGui import QAction
from qt_material import apply_stylesheet, list_themes
class ModulesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.__modules_base_path = pathlib.Path(
            __file__
        ).resolve().parent / pathlib.Path("modules")
        self.__available_modules = self.__get_available_modules()

        # Standardwerte für Einstellungen
        self.current_theme = "dark_teal.xml"
        self.font_size = 12  # Standard-Schriftgröße

        # Menüleiste erstellen
        self.menu_bar = QMenuBar(self)
        self.layout.setMenuBar(self.menu_bar)

        # Menü hinzufügen
        self.modules_menu = QMenu("Load Module", self)
        self.menu_bar.addMenu(self.modules_menu)

        # Aktuelles Modul speichern
        self.current_module_widget = None

        # Module in das Menü hinzufügen
        for module in self.__available_modules:
            action = self.modules_menu.addAction(f"{module.name}  ({module.description})")
            action.triggered.connect(
                lambda checked, mod=module: self.set_module_widget(mod)
            )

        # Einstellungen hinzufügen
        self.settings_menu = QMenu("Settings", self)
        self.menu_bar.addMenu(self.settings_menu)

        # Theme Auswahl Menü
        self.theme_menu = QMenu("Select Theme", self)
        self.settings_menu.addMenu(self.theme_menu)

        # Schriftgrößensteuerung hinzufügen
        font_size_action = QAction("Font Size", self)
        font_size_action.triggered.connect(self.open_font_size_dialog)
        self.settings_menu.addAction(font_size_action)

        # Hilfe text hinzufügen
        self.help_menu = QMenu("Help", self)
        self.menu_bar.addMenu(self.help_menu)

        # Verfügbare Themes laden
        self.available_themes = list_themes()

        # Themes als Menüeinträge hinzufügen
        for theme in self.available_themes:
            theme_action = QAction(theme, self)
            theme_action.triggered.connect(lambda checked, t=theme: self.apply_theme(t))
            self.theme_menu.addAction(theme_action)

    def set_module_widget(self, module):
        """Ersetzt das aktuell angezeigte Modul."""
        # Aktuelles Widget entfernen
        if self.current_module_widget is not None:
            self.layout.removeWidget(self.current_module_widget)
            self.current_module_widget.deleteLater()
            self.current_module_widget = None

        # Neues Widget erstellen und hinzufügen
        self.current_module_widget = module.create_main_window()
        self.layout.addWidget(self.current_module_widget)

    def apply_theme(self, theme_name):
        """Wendet das ausgewählte Theme an und erkennt helle Themes."""
        self.current_theme = theme_name

        # Prüfen, ob es sich um ein "light"-Theme handelt
        if "light" in theme_name:
            apply_stylesheet(self.window(), theme_name, invert_secondary=True)
        else:
            apply_stylesheet(self.window(), theme_name)

    def open_font_size_dialog(self):
        """Öffnet das Fenster zur Schriftgrößenanpassung."""
        self.font_size_dialog = FontSizeDialog(self)
        self.font_size_dialog.exec()

    def change_font_size(self, value, label):
        """Ändert die Schriftgröße basierend auf dem Slider-Wert."""
        self.font_size = value
        label.setText(f"Font Size: {self.font_size}")
        self.setStyleSheet(f"font-size: {self.font_size}px;")

    def __load_module(self, module_name: str) -> types.ModuleType:
        """
        Import a module at runtime from a directory.
        :param module_name: the name of the module to load
        :return: the loaded module
        """
        print(f"trying to load module: {module_name}")

        if module_name == "modules":
            modules_path = self.__modules_base_path / "__init__.py"
        else:
            modules_path = self.__modules_base_path / f"{module_name}.py"
        try:
            spec = importlib.util.spec_from_file_location(
                module_name, str(modules_path)
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.modules[module_name] = module
            print(f"loaded module: {module_name}")
            return module
        except ImportError as e:
            print(f"failed to load module {module_name}: {e}")

    def __get_available_modules(self) -> typing.List[ModuleInfo.Details]:
        modules = self.__load_module("modules")
        modules_list: typing.List[ModuleInfo.Details] = []
        for module_info in pkgutil.iter_modules(modules.__path__):
            module = self.__load_module(module_info.name)
            modules_list.append(ModuleInfo.Details.from_module(module))

        return modules_list


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Hauptlayout des Fensters
        self.central_widget = ModulesWidget(parent=self)
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("JustForYou - Calc")
    app.setOrganizationName("XYZ")
    app.setApplicationVersion("0.1.0")

    main_window = QMainWindow()
    modules_widget = ModulesWidget()
    main_window.setCentralWidget(modules_widget)
    apply_stylesheet(main_window, 'dark_teal.xml')
    main_window.show()
    sys.exit(app.exec())