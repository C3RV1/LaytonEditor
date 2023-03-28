from gui.ui.command_editor.commands.event.Companion import CompanionUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class Companion(CommandEditorEvent, CompanionUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(Companion, self).set_command(command, event=event, **kwargs)
        if command.command == 0x96:
            self.mode.setCurrentIndex(0)
        else:
            self.mode.setCurrentIndex(1)

        self.companion_id.setValue(command.params[0])

    def save(self):
        self.command.command = self.mode.currentData(QtCore.Qt.ItemDataRole.UserRole)
        self.command.params = [self.companion_id.value()]
