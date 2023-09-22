from PySide6 import QtCore, QtWidgets, QtGui


class SoundProfileUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SoundProfileUI, self).__init__(*args, **kwargs)
        self.v_layout = QtWidgets.QVBoxLayout()

        self.h_layout = QtWidgets.QHBoxLayout()

        self.sound_profiles_list = QtWidgets.QListView()
        self.sound_profiles_list.setWrapping(False)
        self.sound_profiles_list.selectionChanged = self.sound_profiles_list_selection_ui
        self.h_layout.addWidget(self.sound_profiles_list, 1)

        self.form_widget = QtWidgets.QWidget()
        self.form_layout = QtWidgets.QFormLayout()

        self.music_id_spin = QtWidgets.QSpinBox()
        self.music_id_spin.setMaximum(65535)
        self.music_id_spin.valueChanged.connect(self.music_id_spin_edit)
        self.form_layout.addRow("Music ID", self.music_id_spin)

        self.unk0_spin = QtWidgets.QSpinBox()
        self.unk0_spin.valueChanged.connect(self.unk0_spin_edit)
        self.unk0_spin.setMaximum(65535)
        self.form_layout.addRow("Unk0", self.unk0_spin)

        self.unk1_spin = QtWidgets.QSpinBox()
        self.unk1_spin.valueChanged.connect(self.unk1_spin_edit)
        self.unk1_spin.setMaximum(65535)
        self.form_layout.addRow("Unk1", self.unk1_spin)
        self.form_widget.setLayout(self.form_layout)

        self.form_widget.hide()

        self.h_layout.addWidget(self.form_widget, 1)

        self.v_layout.addLayout(self.h_layout, 9)

        self.save_btn = QtWidgets.QPushButton("Save", self)
        self.save_btn.clicked.connect(self.save_btn_click)
        self.v_layout.addWidget(self.save_btn, 1)

        self.setLayout(self.v_layout)

    def sound_profiles_list_selection_ui(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection):
        QtWidgets.QListView.selectionChanged(self.sound_profiles_list, selected, deselected)
        if selected.indexes():
            self.sound_profiles_list_selection(selected.indexes()[0])
        else:
            self.sound_profiles_list_selection(QtCore.QModelIndex())

    def sound_profiles_list_selection(self, selected: QtCore.QModelIndex):
        pass

    def save_btn_click(self):
        pass

    def music_id_spin_edit(self, value: int):
        pass

    def unk0_spin_edit(self, value: int):
        pass

    def unk1_spin_edit(self, value: int):
        pass
