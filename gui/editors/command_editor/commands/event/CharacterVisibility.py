import logging

from gui.ui.command_editor.commands.event.CharacterVisibility import CharacterVisibilityUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore
from gui.SettingsManager import SettingsManager


class CharacterVisibility(CommandEditorEvent, CharacterVisibilityUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(CharacterVisibility, self).set_command(command, event=event, **kwargs)
        settings = SettingsManager()

        for i, char_id in enumerate(self.event.characters):
            if char_id == 0:
                break
            char_name = SettingsManager().character_id_to_name.get(char_id, f"Unnamed {char_id}")
            self.character.addItem(f"{char_name}: {char_id}", i)
        self.character.setCurrentIndex(command.params[0])

        if command.command in [0x2a, 0x2b]:
            self.alpha.setChecked(False)
            self.shown.setCurrentIndex(0 if command.command == 0x2a else 1)
        else:
            self.alpha.setChecked(True)
            if abs(command.params[1]) != 2.0:
                logging.warning(f"Event {event.event_id}: Character visibility is not +-0.2 ({command.params[1]})")
            self.shown.setCurrentIndex(0 if command.params[1] > 0 else 1)

    def save(self):
        self.command.params = [self.character.currentData(QtCore.Qt.ItemDataRole.UserRole)]
        if not self.alpha.isChecked():
            if self.shown.currentData(QtCore.Qt.ItemDataRole.UserRole):
                self.command.command = 0x2a
            else:
                self.command.command = 0x2b
        else:
            self.command.command = 0x2c
            self.command.params.append(2.0 if self.shown.currentData(QtCore.Qt.ItemDataRole.UserRole) else -2.0)
