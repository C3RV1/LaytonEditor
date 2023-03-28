from gui.ui.command_editor.commands.event.CharacterSlot import CharacterSlotUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore
from gui.SettingsManager import SettingsManager


class CharacterSlot(CommandEditorEvent, CharacterSlotUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(CharacterSlot, self).set_command(command, event=event, **kwargs)
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
