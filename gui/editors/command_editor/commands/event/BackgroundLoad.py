from gui.ui.command_editor.commands.event.BackgroundLoad import BackgroundLoadUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class BackgroundLoad(CommandEditorEvent, BackgroundLoadUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(BackgroundLoad, self).set_command(command, event=event, **kwargs)
        self.screens.setCurrentIndex(0 if command.command == 0x21 else 1)
        self.path.setText(command.params[0])

    def save(self):
        self.command.command = self.screens.currentData(QtCore.Qt.ItemDataRole.UserRole)
        self.command.params = [self.path.text(), 3]
