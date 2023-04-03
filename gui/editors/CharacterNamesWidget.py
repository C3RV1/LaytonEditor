from gui.ui.CharacterNamesWidget import CharacterNamesWidgetUI
from PySide6 import QtCore, QtWidgets
from ..SettingsManager import SettingsManager
from formats.filesystem import NintendoDSRom


class CharacterNamesEditor(CharacterNamesWidgetUI):
    def __init__(self, rom: NintendoDSRom, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rom: NintendoDSRom = rom

        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Name", "Create Name Sprite"])
        self.table_widget.setRowCount(256)
        self.table_widget.setVerticalHeaderLabels([str(i) for i in range(256)])
        names_dict = SettingsManager().character_id_to_name
        for char_id in range(256):
            table_widget_item = QtWidgets.QTableWidgetItem()
            table_widget_item.setData(QtCore.Qt.ItemDataRole.DisplayRole, names_dict.get(char_id, ""))
            self.table_widget.setItem(char_id, 0, table_widget_item)

            create_name_sprite_button = QtWidgets.QPushButton("Generate")
            create_name_sprite_button.clicked.connect(
                lambda *_args, l_char_id=char_id: self.generate_name_sprite(l_char_id)
            )
            self.table_widget.setCellWidget(char_id, 1, create_name_sprite_button)

        self.setFixedSize(QtCore.QSize(600, 600))
        self.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.show()

    def generate_name_sprite(self, char_id):
        pass
