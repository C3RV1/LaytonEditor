from gui.ui.event.command.MusicFade import MusicFadeUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class MusicFade(CommandEditor, MusicFadeUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(MusicFade, self).set_command(command, event)
        if command.command == 0x8b:
            self.fade_type.setCurrentIndex(0)
        else:
            self.fade_type.setCurrentIndex(1)

        self.time_def_id.setValue(command.params[1])

    def save(self):
        self.command.command = self.fade_type.currentData(QtCore.Qt.ItemDataRole.UserRole)
        self.command.params = [
            (0.0 if self.command.command == 0x8a else 1.0),
            self.time_def_id.value()
        ]
