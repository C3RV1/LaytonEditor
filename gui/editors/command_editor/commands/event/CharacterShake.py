from gui.ui.command_editor.commands.event.CharacterShake import CharacterShakeUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore
from gui.SettingsManager import SettingsManager


class CharacterShake(CommandEditorEvent, CharacterShakeUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(CharacterShake, self).set_command(command, event=event, **kwargs)
        settings = SettingsManager()

        for i, char_id in enumerate(self.event.characters):
            if char_id == 0:
                break
            char_name = SettingsManager().character_id_to_name.get(char_id, f"Unnamed {char_id}")
            self.character.addItem(f"{char_name}: {char_id}", i)
        self.character.setCurrentIndex(command.params[0])

        self.duration.setValue(command.params[1])

    def save(self):
        self.command.params = [
            self.character.currentData(QtCore.Qt.ItemDataRole.UserRole),
            self.duration.value()
        ]
