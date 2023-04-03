from gui.ui.CharacterNamesWidget import CharacterNamesWidgetUI
from PySide6 import QtCore, QtWidgets
from ..SettingsManager import SettingsManager
from formats.filesystem import NintendoDSRom


class CharacterNamesEditor(CharacterNamesWidgetUI):
    def __init__(self, rom: NintendoDSRom, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rom: NintendoDSRom = rom

        self.setup_table(SettingsManager().character_id_to_name)

        self.setFixedSize(QtCore.QSize(600, 600))
        self.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.show()

    def setup_table(self, names_dict):
        self.table_widget.setColumnCount(2)
        self.table_widget.setColumnWidth(1, 200)
        self.table_widget.setHorizontalHeaderLabels(["Name", "Create Name Sprite"])
        self.table_widget.setRowCount(256)
        self.table_widget.setVerticalHeaderLabels([str(i) for i in range(256)])
        for char_id in range(256):
            table_widget_item = QtWidgets.QTableWidgetItem()
            table_widget_item.setData(QtCore.Qt.ItemDataRole.DisplayRole, names_dict.get(char_id, ""))
            self.table_widget.setItem(char_id, 0, table_widget_item)

            create_name_sprite_button = QtWidgets.QPushButton("Generate")
            create_name_sprite_button.clicked.connect(
                lambda *_args, l_char_id=char_id: self.generate_name_sprite(l_char_id)
            )
            if self.rom is None:
                create_name_sprite_button.setEnabled(False)
            self.table_widget.setCellWidget(char_id, 1, create_name_sprite_button)

    def generate_name_sprite(self, char_id):
        if self.rom is None:
            return

    def save_clicked(self):
        name_dict = {}
        for char_id in range(256):
            name = self.table_widget.item(char_id, 0).data(QtCore.Qt.ItemDataRole.DisplayRole)
            if name == "":
                continue
            name_dict[char_id] = name
        SettingsManager().character_id_to_name = name_dict
        SettingsManager().save_character_names()

    def reset_clicked(self):
        self.setup_table(SettingsManager.original_character_names())
