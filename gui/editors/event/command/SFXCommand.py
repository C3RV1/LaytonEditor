from gui.ui.event.command.SFXCommand import SFXCommandUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class SFXCommand(CommandEditor, SFXCommandUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(SFXCommand, self).set_command(command, event)
        self.sfx_id.setValue(command.params[0])
        self.sfx_type.setCurrentIndex(0 if command.command == 0x5d else 1)

    def save(self):
        self.command.command = self.sfx_type.currentData(QtCore.Qt.ItemDataRole.UserRole)
        self.command.params = [self.sfx_id.value()]
