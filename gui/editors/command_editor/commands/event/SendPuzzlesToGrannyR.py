from gui.ui.command_editor.commands.event.SendPuzzlesToGrannyR import SendPuzzlesToGrannyRUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class SendPuzzlesToGrannyR(CommandEditorEvent, SendPuzzlesToGrannyRUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(SendPuzzlesToGrannyR, self).set_command(command, event=event, **kwargs)
        self.puzzle_group_id.setValue(command.params[0])

    def save(self):
        self.command.params = [
            self.puzzle_group_id.value()
        ]

