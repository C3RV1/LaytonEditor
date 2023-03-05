from gui.ui.event.command.SaveProgress import SaveProgressUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class SaveProgress(CommandEditor, SaveProgressUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(SaveProgress, self).set_command(command, event)
        self.next_event.setValue(command.params[0])

    def save(self):
        self.command.params = [
            self.next_event.value()
        ]

