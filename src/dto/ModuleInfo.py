import types

from PySide6.QtWidgets import QWidget


class ModuleInfo:
    def __init__(self, name: str, description: str, main_window: QWidget):
        self.name = name
        self.description = description
        self.main_window = main_window

    @classmethod
    def from_module(cls, module: types.ModuleType):
        module_name = getattr(module, 'MODULE_NAME', 'Unknown')
        module_description = getattr(module, 'MODULE_DESCRIPTION', 'No description available')
        main_window = getattr(module, 'MODULE_MAIN_WINDOW', None)
        return cls(name=module_name, description=module_description, main_window=main_window)