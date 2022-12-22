from gui.ui.event.EventPropertiesWidget import EventPropertiesWidgetUI
from PySide6 import QtCore
from formats.event import Event


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
            return self.char_count

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 4

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Vertical:
            return f"Character {section}"
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
        if index.column() == 0:
            return self.event.characters[index.row()]
        elif index.column() == 1:
            return self.event.characters_pos[index.row()]
        elif index.column() == 2:
            return self.event.characters_shown[index.row()]
        elif index.column() == 3:
            return self.event.characters_anim_index[index.row()]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(EventCharacterTable, self).flags(index)
        if not index.isValid():
            return default_flags
        default_flags |= QtCore.Qt.ItemFlag.ItemIsEditable
        return default_flags

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        if index.column() == 0:
            self.event.characters[index.row()] = value
        elif index.column() == 1:
            self.event.characters_pos[index.row()] = value
        elif index.column() == 2:
            self.event.characters_shown[index.row()] = value
        elif index.column() == 3:
            self.event.characters_anim_index[index.row()] = value
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


class EventPropertiesWidget(EventPropertiesWidgetUI):
    def __init__(self, *args, **kwargs):
        super(EventPropertiesWidget, self).__init__(*args, **kwargs)
        self.event: Event = None
        self.char_table_model = EventCharacterTable()
        self.character_table.setModel(self.char_table_model)

    def set_event(self, ev: Event):
        self.event = ev
        self.char_table_model.set_event(ev)
        self.map_top_id_input.setValue(self.event.map_top_id)
        self.map_btm_id_input.setValue(self.event.map_bottom_id)

    def map_top_id_edit(self, value: int):
        self.event.map_top_id = value

    def map_btm_id_edit(self, value: int):
        self.event.map_bottom_id = value

    def add_character_click(self):
        self.char_table_model.add_character()

    def remove_character_click(self):
        self.char_table_model.remove_character()
