from gui.ui.command_editor.commands.event.StartTea import StartTeaUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class StartTea(CommandEditorEvent, StartTeaUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(StartTea, self).set_command(command, event=event, **kwargs)
        self.hint_id.setValue(command.params[0])
        self.solution_id.setValue(command.params[1])

    def save(self):
        self.command.params = [
            self.hint_id.value(),
            self.solution_id.value()
        ]

