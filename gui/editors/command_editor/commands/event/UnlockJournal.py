from gui.ui.command_editor.commands.event.UnlockJournal import UnlockJournalUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class UnlockJournal(CommandEditorEvent, UnlockJournalUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(UnlockJournal, self).set_command(command, event=event, **kwargs)
        self.entry_id.setValue(command.params[0])

    def save(self):
        self.command.params = [self.entry_id.value()]
