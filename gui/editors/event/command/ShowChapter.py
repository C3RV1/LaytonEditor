from gui.ui.event.command.ShowChapter import ShowChapterUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class ShowChapter(CommandEditor, ShowChapterUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(ShowChapter, self).set_command(command, event)
        self.chapter.setValue(command.params[0])

    def save(self):
        self.command.params = [self.chapter.value()]
