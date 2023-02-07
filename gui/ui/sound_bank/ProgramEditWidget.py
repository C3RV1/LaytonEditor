from PySide6 import QtCore, QtWidgets, QtGui
from .LFOEditWidget import LFOEditWidgetUI
from .SplitEditWidget import SplitEditWidgetUI


class ProgramEditWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ProgramEditWidgetUI, self).__init__(*args, **kwargs)

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        # TODO: Sliders instead of spinbox?
        self.volume = QtWidgets.QSpinBox()
        self.form_layout.addRow("Volume", self.volume)

        self.pan = QtWidgets.QSpinBox()
        self.form_layout.addRow("Pan", self.pan)

        self.lfo_v_layout = QtWidgets.QVBoxLayout()
        self.form_layout.addRow(self.lfo_v_layout)

        self.lfo_label = QtWidgets.QLabel("LFOs")
        self.lfo_v_layout.addWidget(self.lfo_label)

        self.lfo_h_layout = QtWidgets.QHBoxLayout()
        self.lfo_v_layout.addLayout(self.lfo_h_layout)

        self.lfo_list = QtWidgets.QListView()
        self.lfo_h_layout.addWidget(self.lfo_list, 1)

        self.lfo_edit = self.get_lfo_edit_widget()
        self.lfo_h_layout.addWidget(self.lfo_edit, 2)

        self.split_v_layout = QtWidgets.QVBoxLayout()
        self.form_layout.addRow(self.split_v_layout)

        self.split_label = QtWidgets.QLabel("Splits")
        self.split_v_layout.addWidget(self.split_label)

        self.split_h_layout = QtWidgets.QHBoxLayout()
        self.split_v_layout.addLayout(self.split_h_layout)

        self.split_list = QtWidgets.QListView()
        self.split_h_layout.addWidget(self.split_list, 1)

        self.split_edit = self.get_split_edit_widget()
        self.split_edit_scroll = QtWidgets.QScrollArea()
        self.split_edit_scroll.setWidget(self.split_edit)
        self.split_edit_scroll.setWidgetResizable(True)
        # self.split_edit.hide()
        self.split_h_layout.addWidget(self.split_edit_scroll, 2)

    def get_lfo_edit_widget(self):
        return LFOEditWidgetUI()

    def get_split_edit_widget(self):
        return SplitEditWidgetUI()
