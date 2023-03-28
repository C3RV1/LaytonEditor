from gui.ui.command_editor.commands.event.SetMode import SetModeUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class SetMode(CommandEditorEvent, SetModeUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(SetMode, self).set_command(command, event=event, **kwargs)
        next_index = {
            0x6: 0,
            0x7: 1
        }
        self.next_mode_type.setCurrentIndex(next_index[command.command])
        mode_keys = list(self.mode_list.keys())
        self.mode.setCurrentIndex(mode_keys.index(command.params[0]))

    def save(self):
        self.command.command = self.next_mode_type.currentData(QtCore.Qt.ItemDataRole.UserRole)
        self.command.params = [self.mode.currentData(QtCore.Qt.ItemDataRole.UserRole)]
