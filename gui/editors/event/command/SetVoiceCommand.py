from gui.ui.event.command.SetVoiceCommand import SetVoiceCommandUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class SetVoiceCommand(CommandEditor, SetVoiceCommandUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(SetVoiceCommand, self).set_command(command, event)
        self.voice_clip.setValue(command.params[0])

    def save(self):
        self.command.params = [self.voice_clip.value()]
