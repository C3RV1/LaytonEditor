from gui.ui.command_editor.commands.event.SetID import SetIDUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class SetID(CommandEditorEvent, SetIDUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(SetID, self).set_command(command, event=event, **kwargs)
        mode_index = {
            0x5: 0,
            0x8: 1,
            0x9: 2,
            0xb: 3
        }
        self.mode.setCurrentIndex(mode_index[command.command])
        self.value.setValue(command.params[0])

    def save(self):
        self.command.command = self.mode.currentData(QtCore.Qt.ItemDataRole.UserRole)
        self.command.params = [self.value.value()]
        super().save()
