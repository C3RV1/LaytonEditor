from gui.ui.event.command.BackgroundShake import BackgroundShakeUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class BackgroundShake(CommandEditor, BackgroundShakeUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(BackgroundShake, self).set_command(command, event)
        if command.command == 0x6a:
            self.fade_screens.setCurrentIndex(0)
        else:
            self.fade_screens.setCurrentIndex(1)
        self.unk0.setValue(command.params[0])

    def save(self):
        self.command.command = self.fade_screens.currentData(QtCore.Qt.ItemDataRole.UserRole)
        self.command.params = [self.unk0.value()]

