from gui.ui.event.command.LoadBG import LoadBGUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class LoadBG(CommandEditor, LoadBGUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(LoadBG, self).set_command(command, event)
        self.screens.setCurrentIndex(0 if command.command == 0x21 else 1)
        self.path.setText(command.params[0])

    def save(self):
        self.command.command = self.screens.currentData(QtCore.Qt.ItemDataRole.UserRole)
        self.command.params = [self.path.text()]
