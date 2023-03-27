from typing import List

from PySide6 import QtWidgets, QtGui, QtCore
from formats.event import Event
from formats.gds import GDS, GDSCommand
from formats.dlz import TimeDefinitionsDlz
from gui.SettingsManager import SettingsManager
from utility.replace_substitutions import replace_substitutions


class CommandListModel(QtCore.QAbstractListModel):
    def __init__(self):
        super(CommandListModel, self).__init__()
        self._event: Event = None
        self.settings_manager = SettingsManager()

    def set_event(self, event):
        self.layoutAboutToBeChanged.emit()
        self._event = event
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if parent.isValid():
            return 0
        return len(self._event.gds.commands)

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid():
            return None
        command: GDSCommand = self._event.gds.commands[index.row()]
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.parse_command(command) + "\n"
        elif role == QtCore.Qt.ItemDataRole.UserRole:
            return command
        return None

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super().flags(index)
        if not index.isValid():
            return default_flags | QtCore.Qt.ItemFlag.ItemIsDropEnabled
        return default_flags | QtCore.Qt.ItemFlag.ItemIsDragEnabled

    def supportedDropActions(self) -> QtCore.Qt.DropAction:
        return QtCore.Qt.DropAction.MoveAction

    def mimeData(self, indexes: List[QtCore.QModelIndex]) -> QtCore.QMimeData:
        mime_data = super().mimeData(indexes)
        if not indexes:
            return mime_data
        index = indexes[0].row()
        mime_data.setText(str(index))
        return mime_data

    def dropMimeData(self, data: QtCore.QMimeData, action: QtCore.Qt.DropAction, row: int, column: int,
                     parent: QtCore.QModelIndex) -> bool:
        if row == -1:
            return False
        src_row = int(data.text())
        if src_row < row:
            row -= 1
        if src_row == row:
            return False
        self.layoutAboutToBeChanged.emit()
        command = self._event.gds.commands[src_row]
        self._event.gds.commands.pop(src_row)
        self._event.gds.commands.insert(row, command)
        self.layoutChanged.emit()
        return True

    def parse_command(self, command: GDSCommand):
        if command.command in [0x2, 0x3, 0x32, 0x33, 0x72, 0x7f, 0x80, 0x81, 0x87, 0x88]:  # fade
            fade_in = command.command in [0x2, 0x32, 0x80, 0x81, 0x88]
            fade_time = None
            fade_screens = 0
            if command.command in [0x2, 0x3, 0x72, 0x80]:
                fade_screens = 2  # both screens
            elif command.command in [0x32, 0x33, 0x7f, 0x81]:
                fade_screens = 0  # btm screen
            elif command.command in [0x87, 0x88]:
                fade_screens = 1  # top screen
            if command.command in [0x72, 0x7f, 0x80, 0x81, 0x87, 0x88]:
                fade_time = command.params[0]  # timed

            screens = {
                0: "Bottom screen",
                1: "Top screen",
                2: "Both screens"
            }[fade_screens]

            duration = "Default frames" if fade_time is None else f"{fade_time} frames"

            return f"Screen: Fade {'In' if fade_in else 'Out'}\n" \
                   f"{screens} ({duration})"
        elif command.command == 0x4:
            text_id = command.params[0]
            text = self._event.get_text(text_id)

            char_id = text.params[0]
            if char_id != 0:
                char_name = self.settings_manager.character_id_to_name[char_id]
            else:
                char_name = "Narrator"

            text_parsed = replace_substitutions(text.params[4])

            text_one_line = text_parsed.split('\n')
            if len(text_one_line) > 1:
                text_one_line = text_one_line[0] + "..."
            else:
                text_one_line = text_one_line[0]

            return f"Dialogue {char_name}: {char_id} [{text.params[1]}, {text.params[2]}] ({text.params[3]} voice pitch)\n" \
                   f"{text_one_line}"
        elif command.command in [0x5, 0x8, 0x9, 0xb]:
            mode = {
                0x5: "Place",
                0x8: "Movie",
                0x9: "Event",
                0xb: "Puzzle"
            }[command.command]
            return f"Sequencing: Set Mode ID\n" \
                   f"{mode} to {command.params[0]}"
        elif command.command in [0x6, 0x7]:
            mode = {
                "narration": "Narration",
                "movie": "Movie",
                "puzzle": "Puzzle",
                "drama event": "Event",
                "room": "Place",
                "name": "Name",
                "staff": "Staff",
                "nazoba": "Nazoba",
                "menu": "Menu",
                "challenge": "Challenge",
                "sub herb": "Herbal tea",
                "sub camera": "Camera",
                "sub ham": "Hamster",
                "passcode": "Passcode"
            }[command.params[0]]
            return f"Sequencing: {'Next Mode' if command.command == 0x6 else 'Queue Following Mode'}\n" \
                   f"Mode: {mode}"
        elif command.command in [0x31, 0x69, 0x6c, 0x8e]:
            if command.command == 0x31:
                line = f"{command.params[0]} Frames"
            elif command.command == 0x69:
                line = f"Tap"
            elif command.command == 0x6c:
                line = f"Tap or {command.params[0]} Frames"
            elif command.command == 0x8e:
                tm_def = TimeDefinitionsDlz(rom=self._event.rom, filename="data_lt2/rc/tm_def.dlz")
                frames = tm_def[command.params[0]]
                line = f"Time Definition {command.params[0]} ({frames} frames)"
            return f"Wait: {line}"
        elif command.command in [0x21, 0x22]:
            return f"Screen: Load {'Bottom' if command.command == 0x21 else 'Top'} Background\n" \
                   f"{command.params[0]}"
        elif command.command in [0x2a, 0x2b, 0x2c]:
            if command.command in [0x2a, 0x2b]:
                show = command.command == 0x2a
            else:
                show = command.params[1] > 0
            alpha = "" if command.command != 0x2c else ' (alpha)'

            char_id = self._event.characters[command.params[0]]
            char_name = self.settings_manager.character_id_to_name[char_id]

            return f"Character {char_name}: {char_id} Visibility\n" \
                   f"{'Show' if show else 'Hide'}{alpha}"
        elif command.command == 0x2d:
            return f"Screen: Show Chapter {command.params[0]}"
        elif command.command == 0x30:
            char_id = self._event.characters[command.params[0]]
            char_name = self.settings_manager.character_id_to_name[char_id]

            slot_name = {
                0: "Left 1",
                1: "Center (looking right)",
                2: "Right 1",
                3: "Left 2",
                4: "Left Center",
                5: "Right Center",
                6: "Right 2"
            }[command.params[1]]

            return f"Character {char_name}: {char_id} Slot\n" \
                   f"Moving to slot {slot_name}"
        elif command.command == 0x37:
            return f"Screen: Bottom Tint (RGBA: {command.params})"
        elif command.command == 0x3f:
            char_id = command.params[0]
            char_name = self.settings_manager.character_id_to_name[char_id]

            return f"Character {char_name}: {char_id} Animation\n" \
                   f"Setting animation to {command.params[1]}"
        elif command.command == 0x5c:
            return f"Dialogue: Set Voice Clip {command.params[0]}"
        elif command.command in [0x5d, 0x5e]:
            return f"Audio: Sound Effect {command.params[0]} ({'SAD' if command.command == 0x5d else 'SED'})"
        elif command.command in [0x62, 0x8c]:
            if command.command == 0x62:
                return f"Audio: Play Music {command.params[0]} at {command.params[1]} Volume\n" \
                       f"Fade In {command.params[2]} Frames"
            else:
                return f"Audio: Play Music {command.params[0]} at {command.params[1]} Volume\n" \
                       f"Variation Command? (0x8c)"
        elif command.command in [0x6a, 0x6b]:
            return f"Screen: Shake {'Bottom' if command.command == 0x6a else 'Top'}\n" \
                   f"Unk0: {command.params[0]}"
        elif command.command == 0x70:
            return f"Progression: Unlocking Journal {command.params[0]}"
        elif command.command in [0x71, 0x7d]:
            return f"Progression: {'Reveal' if command.command == 0x71 else 'Solve'} Mystery {command.params[0]}"
        elif command.command == 0x73:
            return f"Minigame: Start Tea\n" \
                   f"Hint ID: {command.params[0]}, Solution ID: {command.params[1]}"
        elif command.command == 0x76:
            return f"Progression: Send Puzzles to Granny Riddleton\n" \
                   f"Puzzle Group: {command.params[0]}"
        elif command.command in [0x77, 0x7a]:
            return f"Progression: {'Pick Up' if command.command == 0x77 else 'Remove'} Item {command.params[0]}"
        elif command.command == 0x7b:
            return f"Progression: Save Progress Prompt\n" \
                   f"Next Event: {command.params[0]}"
        elif command.command == 0x79:
            return f"Progression: Unlocking Minigame {command.params[0]}"
        elif command.command == 0x7e:
            char_id = self._event.characters[command.params[0]]
            char_name = self.settings_manager.character_id_to_name[char_id]
            return f"Character {char_name}: {char_id} Shake\n" \
                   f"Duration?: {command.params[1]}"
        elif command.command == 0x82:
            return "Screen: Flash Bottom Screen"
        elif command.command == 0x89:
            return "Audio: Stop Train Sound"
        elif command.command in [0x8a, 0x8b]:
            tm_def = TimeDefinitionsDlz(rom=self._event.rom, filename="data_lt2/rc/tm_def.dlz")
            frames = tm_def[command.params[1]]
            return f"Audio: Fade Music {'Out' if command.command == 0x8a else 'In'}\n" \
                   f"In Time Definition {command.params[1]} ({frames} frames)"
        elif command.command in [0x96, 0x97]:
            return f"Progression: {'Add' if command.command == 0x96 else 'Remove'} Companion {command.params[0]}"
        elif command.command == 0xa1:
            return "Progression: Complete Game"
        else:
            return f"Command {hex(command.command)}\n" \
                   f"Parameters: {command.params}"
