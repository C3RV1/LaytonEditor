from PySide6 import QtCore, QtWidgets, QtGui


class SoundProfileUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SoundProfileUI, self).__init__(*args, **kwargs)
        self.v_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()

        self.bg_music_id_spin = QtWidgets.QSpinBox()
        self.bg_music_id_spin.setMaximum(65535)
        self.bg_music_id_spin.valueChanged.connect(self.bg_music_id_spin_edit)
        self.form_layout.addRow("Background Music ID", self.bg_music_id_spin)

        self.unk0_spin = QtWidgets.QSpinBox()
        self.unk0_spin.valueChanged.connect(self.unk0_spin_edit)
        self.unk0_spin.setMaximum(65535)
        self.form_layout.addRow("Unk0", self.unk0_spin)

        self.unk1_spin = QtWidgets.QSpinBox()
        self.unk1_spin.valueChanged.connect(self.unk1_spin_edit)
        self.unk1_spin.setMaximum(65535)
        self.form_layout.addRow("Unk1", self.unk1_spin)

        self.v_layout.addLayout(self.form_layout, 9)

        self.save_btn = QtWidgets.QPushButton("Save", self)
        self.save_btn.clicked.connect(self.save_btn_click)
        self.v_layout.addWidget(self.save_btn, 1)

        self.setLayout(self.v_layout)

    def save_btn_click(self):
        pass

    def bg_music_id_spin_edit(self, value: int):
        pass

    def unk0_spin_edit(self, value: int):
        pass

    def unk1_spin_edit(self, value: int):
        pass
