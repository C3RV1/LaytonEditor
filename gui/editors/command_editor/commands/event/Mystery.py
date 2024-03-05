from gui.ui.command_editor.commands.event.Mystery import MysteryUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class Mystery(CommandEditorEvent, MysteryUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(Mystery, self).set_command(command, event=event, **kwargs)
        if command.command == 0x71:
            self.mode.setCurrentIndex(0)
        else:
            self.mode.setCurrentIndex(1)

        self.mystery_id.setValue(command.params[0])

    def save(self):
        self.command.command = self.mode.currentData(QtCore.Qt.ItemDataRole.UserRole)
        self.command.params = [self.mystery_id.value()]
        super().save()
