from PySide6 import QtCore, QtWidgets, QtGui
import enum


class FrameOrders(enum.IntEnum):
    LOOPING = 0
    NO_LOOPING = 1
    CUSTOM = 2


class EventPropertiesWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(EventPropertiesWidgetUI, self).__init__(*args, **kwargs)

        self.v_layout = QtWidgets.QVBoxLayout()

        self.form_layout = QtWidgets.QFormLayout()

        self.name_input = QtWidgets.QLineEdit(self)
        self.name_input.textChanged.connect(self.name_input_edit)
        self.form_layout.addRow("Event Name", self.name_input)

        self.map_top_id_input = QtWidgets.QSpinBox(self)
        self.map_top_id_input.setMaximum(65535)
        self.map_top_id_input.valueChanged.connect(self.map_top_id_edit)
        self.form_layout.addRow("Map Top ID", self.map_top_id_input)

        self.map_btm_id_input = QtWidgets.QSpinBox(self)
        self.map_btm_id_input.setMaximum(65535)
        self.map_btm_id_input.valueChanged.connect(self.map_btm_id_edit)
        self.form_layout.addRow("Map Bottom ID", self.map_btm_id_input)

        self.unk0_input = QtWidgets.QSpinBox(self)
        self.unk0_input.setMaximum(255)
        self.unk0_input.valueChanged.connect(self.unk0_edit)
        self.form_layout.addRow("Unk0", self.unk0_input)

        self.unk1_input = QtWidgets.QSpinBox(self)
        self.unk1_input.setMaximum(255)
        self.unk1_input.valueChanged.connect(self.unk1_edit)
        self.form_layout.addRow("Unk1", self.unk1_input)

        self.sound_profile_input = QtWidgets.QSpinBox(self)
        self.sound_profile_input.setMaximum(65535)
        self.sound_profile_input.valueChanged.connect(self.sound_profile_edit)
        self.form_layout.addRow("Sound Profile", self.sound_profile_input)

        self.v_layout.addLayout(self.form_layout)

        self.character_table = QtWidgets.QTableView()
        self.v_layout.addWidget(self.character_table)

        self.character_buttons_layout = QtWidgets.QHBoxLayout()

        self.add_character = QtWidgets.QPushButton("Add Character")
        self.add_character.clicked.connect(self.add_character_click)
        self.character_buttons_layout.addWidget(self.add_character)

        self.remove_character = QtWidgets.QPushButton("Remove Character")
        self.remove_character.clicked.connect(self.remove_character_click)
        self.character_buttons_layout.addWidget(self.remove_character)

        self.v_layout.addLayout(self.character_buttons_layout)

        self.setLayout(self.v_layout)

    def name_input_edit(self, value: str):
        pass

    def map_top_id_edit(self, value: int):
        pass

    def map_btm_id_edit(self, value: int):
        pass

    def unk0_edit(self, value: int):
        pass

    def unk1_edit(self, value: int):
        pass

    def sound_profile_edit(self, value: int):
        pass

    def add_character_click(self):
        pass

    def remove_character_click(self):
        pass
