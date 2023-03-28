from gui.ui.command_editor.commands.event.UnlockMinigame import UnlockMinigameUI
from ..CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class UnlockMinigame(CommandEditor, UnlockMinigameUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(UnlockMinigame, self).set_command(command, event)
        self.minigame_id.setValue(command.params[0])

    def save(self):
        self.command.params = [self.minigame_id.value()]
