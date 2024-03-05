from gui.ui.command_editor.commands.event.SaveProgress import SaveProgressUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class SaveProgress(CommandEditorEvent, SaveProgressUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(SaveProgress, self).set_command(command, event=event, **kwargs)
        self.next_event.setValue(command.params[0])

    def save(self):
        self.command.params = [
            self.next_event.value()
        ]
        super().save()

