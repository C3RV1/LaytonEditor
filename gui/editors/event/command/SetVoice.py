from gui.ui.event.command.SetVoice import SetVoiceUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class SetVoice(CommandEditor, SetVoiceUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(SetVoice, self).set_command(command, event)
        self.voice_clip.setValue(command.params[0])

    def save(self):
        self.command.params = [self.voice_clip.value()]
