# Modules-API

The modules in this folder will be dynamically loaded at runtime.
Each module must have a main widget, that encapsulate the module's functionality.

The runtime will search for some metadata:
- `MODULE_NAME`: The name of the module
- `MODULE_DESCRIPTION`: The description of the module
- `MODULE_MAIN_WINDOW`: Function with name create_main_window to create the main window

The module must export these variables in order to be loaded correctly.

You can have a look at the example [Hello World Module](hello_world.py) as an example.