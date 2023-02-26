from gui.ui.event.command.SetModeCommand import SetModeCommandUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class SetModeCommand(CommandEditor, SetModeCommandUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(SetModeCommand, self).set_command(command, event)
        next_index = {
            0x6: 0,
            0x7: 1
        }
        self.next_mode_type.setCurrentIndex(next_index[command.command])
        self.value.setText(command.params[0])

    def save(self):
        self.command.command = self.next_mode_type.currentData(QtCore.Qt.ItemDataRole.UserRole)
        self.command.params = [self.value.text()]
