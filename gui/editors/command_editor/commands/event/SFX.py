from gui.ui.command_editor.commands.event.SFX import SFXUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class SFX(CommandEditorEvent, SFXUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(SFX, self).set_command(command, event=event, **kwargs)
        self.sfx_id.setValue(command.params[0])
        self.sfx_type.setCurrentIndex(0 if command.command == 0x5d else 1)

    def save(self):
        self.command.command = self.sfx_type.currentData(QtCore.Qt.ItemDataRole.UserRole)
        self.command.params = [self.sfx_id.value()]
        super().save()
