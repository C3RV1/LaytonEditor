from gui.ui.command_editor.commands.event.SetVoice import SetVoiceUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class SetVoice(CommandEditorEvent, SetVoiceUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(SetVoice, self).set_command(command, event=event, **kwargs)
        self.voice_clip.setValue(command.params[0])

    def save(self):
        self.command.params = [self.voice_clip.value()]
        super().save()
