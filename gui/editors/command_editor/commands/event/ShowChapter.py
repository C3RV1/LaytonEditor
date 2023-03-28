from gui.ui.command_editor.commands.event.ShowChapter import ShowChapterUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class ShowChapter(CommandEditorEvent, ShowChapterUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(ShowChapter, self).set_command(command, event=event, **kwargs)
        self.chapter.setValue(command.params[0])

    def save(self):
        self.command.params = [self.chapter.value()]
