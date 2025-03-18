import types
from PySide6.QtWidgets import QWidget

class Details:
    def __init__(self, name: str, description: str, create_main_window: callable):
        self.name = name
        self.description = description
        self.create_main_window = create_main_window

    @classmethod
    def from_module(cls, module: types.ModuleType):
        module_name: str = getattr(module, "MODULE_NAME", "Unknown")
        module_description: str = getattr(
            module, "MODULE_DESCRIPTION", "No description available"
        )
        create_main_window_: callable = getattr(module, "MODULE_MAIN_WINDOW", lambda: None)

        if not callable(create_main_window_):
            raise ValueError(f"MODULE_MAIN_WINDOW in {module.__name__} is not callable")
        return cls(
            name=module_name,
            description=module_description,
            create_main_window=create_main_window_
        )
