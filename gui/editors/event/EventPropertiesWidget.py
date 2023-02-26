from formats.gds import GDS
from gui.ui.event.EventPropertiesWidget import EventPropertiesWidgetUI
from PySide6 import QtCore, QtWidgets
from formats.event import Event
from gui.SettingsManager import SettingsManager


class EventCharacterTable(QtCore.QAbstractTableModel):
    def __init__(self, view: QtWidgets.QTableView, *args, **kwargs):
        super(EventCharacterTable, self).__init__(*args, **kwargs)
        self.event: Event = None
        self.char_count = 0
        self.char_combobox = []
        self.view = view
        self.settings = SettingsManager()

    def set_event(self, ev: Event):
        self.layoutAboutToBeChanged.emit()
        self.event = ev
        self.char_count = 0
        for character in self.event.characters:
            if character == 0:
                break
            self.char_count += 1
        self.layoutChanged.emit()
        self.generate_combobox()

    def generate_combobox(self):
        self.char_combobox = []
        for i, character in enumerate(self.event.characters[:self.char_count]):
            combobox = QtWidgets.QComboBox()
            index = 0
            for j, (key, value) in enumerate(self.settings.character_id_to_name.items()):
                combobox.addItem(f"{value}: {key}", key)
                if character == key:
                    index = j
            if index != 0:
                combobox.setCurrentIndex(index)
            combobox.currentIndexChanged.connect(lambda _idx, combo_i=i: self.combobox_change(combo_i))
            self.char_combobox.append(combobox)
            self.view.setIndexWidget(self.index(i, 0), combobox)

    def combobox_change(self, char_idx):
        combobox: QtWidgets.QComboBox = self.char_combobox[char_idx]
        data = combobox.currentData(QtCore.Qt.ItemDataRole.UserRole)
        old = self.event.characters[char_idx]
        self.event.characters[char_idx] = data

        for gds_command in self.event.gds.commands:
            if gds_command.command == 0x4:
                text_: GDS = self.event.get_text(gds_command.params[0])
                if text_.params[0] == old:
                    text_.params[0] = data
            elif gds_command.command == 0x3f:
                if gds_command.params[0] == old:
                    gds_command.params[0] = data

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
        self.generate_combobox()

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
        self.generate_combobox()


class EventPropertiesWidget(EventPropertiesWidgetUI):
    def __init__(self, *args, **kwargs):
        super(EventPropertiesWidget, self).__init__(*args, **kwargs)
        self.event: Event = None
        self.char_table_model = EventCharacterTable(self.character_table)
        self.character_table.setModel(self.char_table_model)

    def set_event(self, ev: Event):
        self.event = ev
        self.char_table_model.set_event(ev)
        self.name_input.setText(self.event.name)
        self.map_top_id_input.setValue(self.event.map_top_id)
        self.map_btm_id_input.setValue(self.event.map_bottom_id)
        self.unk0_input.setValue(self.event.unk0)
        self.sound_profile_input.setValue(self.event.sound_profile)

    def name_input_edit(self, value: str):
        self.event.name = value[:48]
        if len(value) > 48:
            self.name_input.setText(value[:48])

    def map_top_id_edit(self, value: int):
        self.event.map_top_id = value

    def map_btm_id_edit(self, value: int):
        self.event.map_bottom_id = value

    def unk0_edit(self, value: int):
        self.event.unk0 = value

    def sound_profile_edit(self, value: int):
        self.event.sound_profile = value

    def add_character_click(self):
        self.char_table_model.add_character()

    def remove_character_click(self):
        self.char_table_model.remove_character()
