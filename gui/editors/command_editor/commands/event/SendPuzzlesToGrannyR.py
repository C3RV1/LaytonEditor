from gui.ui.command_editor.commands.event.SendPuzzlesToGrannyR import SendPuzzlesToGrannyRUI
from ..CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class SendPuzzlesToGrannyR(CommandEditor, SendPuzzlesToGrannyRUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(SendPuzzlesToGrannyR, self).set_command(command, event)
        self.puzzle_group_id.setValue(command.params[0])

    def save(self):
        self.command.params = [
            self.puzzle_group_id.value()
        ]

