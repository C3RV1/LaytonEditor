from gui.ui.event.command.CharacterVisibilityCommand import CharacterVisibilityCommandUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore
from gui.SettingsManager import SettingsManager


class CharacterVisibilityCommand(CommandEditor, CharacterVisibilityCommandUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(CharacterVisibilityCommand, self).set_command(command, event)
        settings = SettingsManager()

        for i, char_id in enumerate(self.event.characters):
            if char_id == 0:
                break
            char_name = settings.character_id_to_name[char_id]
            self.character.addItem(f"{char_name}: {char_id}", i)
        self.character.setCurrentIndex(command.params[0])

        if command.command in [0x2a, 0x2b]:
            self.alpha.setChecked(False)
            self.shown.setChecked(command.command == 0x2a)
        else:
            self.alpha.setChecked(True)
            self.shown.setChecked(command.params[1] > 0)

    def save(self):
        self.command.params = [self.character.currentData(QtCore.Qt.ItemDataRole.UserRole)]
        if not self.alpha.isChecked():
            if self.shown.isChecked():
                self.command.command = 0x2a
            else:
                self.command.command = 0x2b
        else:
            self.command.command = 0x2c
            self.command.params.append(2.0 if self.shown.isChecked() else -2.0)
