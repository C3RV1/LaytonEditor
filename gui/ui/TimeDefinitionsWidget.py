from PySide6 import QtCore, QtWidgets, QtGui


class TimeDefinitionsUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.v_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.v_layout)

        self.h_layout = QtWidgets.QHBoxLayout()
        self.v_layout.addLayout(self.h_layout)

        self.time_def_list = QtWidgets.QListView()
        self.time_def_list.setWrapping(False)
        self.time_def_list.selectionChanged = self.time_def_list_selection_ui
        self.h_layout.addWidget(self.time_def_list, 1)

        self.form_widget = QtWidgets.QWidget()
        self.h_layout.addWidget(self.form_widget, 1)
        self.form_layout = QtWidgets.QFormLayout()
        self.form_widget.setLayout(self.form_layout)

        self.time_def_spin = QtWidgets.QSpinBox()
        self.time_def_spin.setMaximum(65535)
        self.time_def_spin.valueChanged.connect(self.time_def_spin_edit)
        self.form_layout.addRow("Frames", self.time_def_spin)

        self.save_btn = QtWidgets.QPushButton("Save", self)
        self.save_btn.clicked.connect(self.save_btn_click)
        self.v_layout.addWidget(self.save_btn, 1)

        self.form_widget.hide()

    def time_def_list_selection_ui(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection):
        QtWidgets.QListView.selectionChanged(self.time_def_list, selected, deselected)
        if selected.indexes():
            self.time_def_list_selection(selected.indexes()[0])
        else:
            self.time_def_list_selection(QtCore.QModelIndex())

    def time_def_list_selection(self, selected: QtCore.QModelIndex):
        pass

    def save_btn_click(self):
        pass

    def time_def_spin_edit(self, value: int):
        pass
