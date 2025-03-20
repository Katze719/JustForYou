from PySide6 import QtWidgets, QtCore


class CustomMenu(QtWidgets.QMenu):
    def mousePressEvent(self, event):
        # Prüfen, ob es ein Rechtsklick ist
        if event.button() == QtCore.Qt.RightButton:
            # Bestimme, welche Aktion angeklickt wurde
            action = self.actionAt(event.pos())
            if action:
                # Das zugehörige Modul-Objekt abrufen
                module = action.data()
                # Zusätzlichen Parameter (z. B. right_click=True) übergeben
                self.parent().set_module_widget(module, right_click=True)
            event.accept()  # Event als verarbeitet markieren
        else:
            # Bei anderen Mausklicks den Standardverhalten nutzen
            super().mousePressEvent(event)
