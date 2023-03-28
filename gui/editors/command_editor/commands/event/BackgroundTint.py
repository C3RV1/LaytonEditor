from gui.ui.command_editor.commands.event.BackgroundTint import BackgroundTintUI
from ..CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtGui


class BackgroundTint(CommandEditor, BackgroundTintUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(BackgroundTint, self).set_command(command, event)
        self.color.setCurrentColor(QtGui.QColor(
            command.params[0],
            command.params[1],
            command.params[2],
            command.params[3]
        ))

    def save(self):
        color: QtGui.QColor = self.color.currentColor()
        self.command.params = [
            color.red(),
            color.green(),
            color.blue(),
            color.alpha()
        ]
