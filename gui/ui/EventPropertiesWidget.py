from PySide6 import QtCore, QtWidgets, QtGui
import enum


class FrameOrders(enum.IntEnum):
    LOOPING = 0
    NO_LOOPING = 1
    CUSTOM = 2


class EventPropertiesWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(EventPropertiesWidgetUI, self).__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()

        self.form_layout = QtWidgets.QFormLayout()

        self.map_top_id_input = QtWidgets.QSpinBox(self)
        self.map_top_id_input.valueChanged.connect(self.map_top_id_edit)
        self.form_layout.addRow("Map Top ID", self.map_top_id_input)

        self.map_btm_id_input = QtWidgets.QSpinBox(self)
        self.map_btm_id_input.valueChanged.connect(self.map_btm_id_edit)
        self.form_layout.addRow("Map Bottom ID", self.map_btm_id_input)

        self.layout.addLayout(self.form_layout)

        self.character_table = QtWidgets.QTableView()
        self.layout.addWidget(self.character_table)

        self.character_buttons_layout = QtWidgets.QHBoxLayout()

        self.add_character = QtWidgets.QPushButton("Add Character")
        self.add_character.clicked.connect(self.add_character_click)
        self.character_buttons_layout.addWidget(self.add_character)

        self.remove_character = QtWidgets.QPushButton("Remove Character")
        self.remove_character.clicked.connect(self.remove_character_click)
        self.character_buttons_layout.addWidget(self.remove_character)

        self.layout.addLayout(self.character_buttons_layout)

        self.setLayout(self.layout)

    def map_top_id_edit(self, value: int):
        pass

    def map_btm_id_edit(self, value: int):
        pass

    def add_character_click(self):
        pass

    def remove_character_click(self):
        pass
