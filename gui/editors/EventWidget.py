import logging

from ..ui.EventWidget import EventWidgetUI
from formats.event import Event
from formats_parsed.EventDCC import EventDCC
from formats_parsed.EventScript import EventScript

from previewers.event.EventPlayer import EventPlayer
from PySide6 import QtCore, QtWidgets, QtGui

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..MainEditor import MainEditor


class EventCharacterTable(QtCore.QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super(EventCharacterTable, self).__init__(*args, **kwargs)
        self.event: Event = None
        self.char_count = 0

    def set_event(self, ev: Event):
        self.layoutAboutToBeChanged.emit()
        self.event = ev
        self.char_count = 0
        for character in self.event.characters:
            if character == 0:
                break
            self.char_count += 1
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return self.char_count + 2

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 4

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Vertical:
            return [
                "Map Top ID",
                "Map Bottom ID",
                f"Character {section - 2}"
            ][min(section, 2)]
        if section >= 5:
            return None
        return [
            "ID",
            "Position",
            "Shown",
            "Animation Index"
        ][section]

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        if index.row() == 0:
            if index.column() == 0:
                return self.event.map_top_id
            return None
        elif index.row() == 1:
            if index.column() == 0:
                return self.event.map_bottom_id
            return None
        if index.column() == 0:
            return self.event.characters[index.row() - 2]
        elif index.column() == 1:
            return self.event.characters_pos[index.row() - 2]
        elif index.column() == 2:
            return self.event.characters_shown[index.row() - 2]
        elif index.column() == 3:
            return self.event.characters_anim_index[index.row() - 2]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(EventCharacterTable, self).flags(index)
        if not index.isValid():
            return default_flags
        if index.row() == 0 or index.row() == 1:
            if index.column() == 0:
                default_flags |= QtCore.Qt.ItemFlag.ItemIsEditable
        else:
            default_flags |= QtCore.Qt.ItemFlag.ItemIsEditable
        return default_flags

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        if index.row() == 0:
            self.event.map_top_id = value
            return True
        elif index.row() == 1:
            self.event.map_bottom_id = value
            return True
        if index.column() == 0:
            self.event.characters[index.row() - 2] = value
        elif index.column() == 1:
            self.event.characters_pos[index.row() - 2] = value
        elif index.column() == 2:
            self.event.characters_shown[index.row() - 2] = value
        elif index.column() == 3:
            self.event.characters_anim_index[index.row() - 2] = value
        else:
            return False
        return True

    def add_character(self):
        if self.char_count >= 8:
            return
        self.layoutAboutToBeChanged.emit()
        self.char_count += 1
        self.layoutChanged.emit()

    def remove_character(self):
        if self.char_count <= 0:
            return
        self.layoutAboutToBeChanged.emit()
        self.char_count -= 1
        self.event.characters[self.char_count] = 0
        self.event.characters_pos[self.char_count] = 0
        self.event.characters_shown[self.char_count] = False
        self.event.characters_anim_index[self.char_count] = 0
        self.layoutChanged.emit()


class EventEditor(EventWidgetUI):
    def __init__(self, main_editor):
        super(EventEditor, self).__init__()
        self.event = None
        self.char_table_model = EventCharacterTable()
        self.main_editor: MainEditor = main_editor

    def set_event(self, ev: Event):
        self.event = ev
        self.char_table_model.set_event(ev)
        self.character_table.setModel(self.char_table_model)
        dcc_text = EventDCC(ev)
        serialized = dcc_text.serialize(include_character=False)
        self.text_editor.setPlainText(serialized)

    def preview_dcc_btn_click(self):
        text = self.text_editor.toPlainText()
        is_ok, error = EventDCC(self.event).parse(text, include_character=False)
        if is_ok:
            self.main_editor.pg_previewer.start_renderer(EventPlayer(self.event))
        else:
            logging.error(f"Error compiling DCC: {error}")

    def save_dcc_btn_click(self):
        text = self.text_editor.toPlainText()
        is_ok, error = EventDCC(self.event).parse(text)
        if is_ok:
            self.event.save_to_rom()
            self.main_editor.pg_previewer.start_renderer(EventPlayer(self.event))
        else:
            logging.error(f"Error compiling DCC: {error}")

    def preview_ev_script_btn_click(self):
        text = self.text_editor.toPlainText()
        try:
            ev_script = EventScript(text, self.event)
            ev_script.parse()
            self.main_editor.pg_previewer.start_renderer(EventPlayer(self.event))
        except Exception as e:
            logging.error(f"Error compiling EventScript: {e}")

    def save_ev_script_btn_click(self):
        text = self.text_editor.toPlainText()
        try:
            ev_script = EventScript(text, self.event)
            ev_script.parse()
            self.event.save_to_rom()
            self.main_editor.pg_previewer.start_renderer(EventPlayer(self.event))
        except Exception as e:
            logging.error(f"Error compiling EventScript: {e}")

    def add_character_click(self):
        self.char_table_model.add_character()

    def remove_character_click(self):
        self.char_table_model.remove_character()
