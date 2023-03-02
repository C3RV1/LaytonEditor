from gui.ui.event.command.UnlockJournal import UnlockJournalUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class UnlockJournal(CommandEditor, UnlockJournalUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(UnlockJournal, self).set_command(command, event)
        self.entry_id.setValue(command.params[0])

    def save(self):
        self.command.params = [self.entry_id.value()]
