from gui.ui.command_editor.commands.event.CharacterAnimation import CharacterAnimationUI
from ..CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore
from gui.SettingsManager import SettingsManager


class CharacterAnimation(CommandEditor, CharacterAnimationUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(CharacterAnimation, self).set_command(command, event)
        settings = SettingsManager()

        index = -1
        for i, char_id in enumerate(self.event.characters):
            if char_id == 0:
                break
            if char_id == command.params[0]:
                index = i
            char_name = settings.character_id_to_name[char_id]
            self.character.addItem(f"{char_name}: {char_id}", char_id)
        if index != -1:
            self.character.setCurrentIndex(index)

        self.animation.setText(command.params[1])

    def save(self):
        self.command.params = [
            self.character.currentData(QtCore.Qt.ItemDataRole.UserRole),
            self.animation.text()
        ]
