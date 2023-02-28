from gui.ui.event.command.ShowChapterCommand import ShowChapterCommandUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class ShowChapterCommand(CommandEditor, ShowChapterCommandUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(ShowChapterCommand, self).set_command(command, event)
        self.chapter.setValue(command.params[0])

    def save(self):
        self.command.params = [self.chapter.value()]
