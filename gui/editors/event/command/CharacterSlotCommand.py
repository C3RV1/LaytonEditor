from gui.ui.event.command.CharacterSlotCommand import CharacterSlotCommandUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore
from gui.SettingsManager import SettingsManager


class CharacterSlotCommand(CommandEditor, CharacterSlotCommandUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(CharacterSlotCommand, self).set_command(command, event)
        settings = SettingsManager()

        for i, char_id in enumerate(self.event.characters):
            if char_id == 0:
                break
            char_name = settings.character_id_to_name[char_id]
            self.character.addItem(f"{char_name}: {char_id}", i)
        self.character.setCurrentIndex(command.params[0])

        self.slot.setCurrentIndex(command.params[1])

    def save(self):
        self.command.params = [
            self.character.currentData(QtCore.Qt.ItemDataRole.UserRole),
            self.slot.currentData(QtCore.Qt.ItemDataRole.UserRole)
        ]
