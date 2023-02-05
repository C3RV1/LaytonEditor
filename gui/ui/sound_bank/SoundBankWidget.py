from PySide6 import QtCore, QtWidgets, QtGui


class SoundBankWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SoundBankWidgetUI, self).__init__(*args, **kwargs)

        self.v_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.v_layout)

        self.tab_widget = QtWidgets.QTabWidget()
        self.v_layout.addWidget(self.tab_widget, 4)

        self.sample_tab = QtWidgets.QWidget()
        self.tab_widget.addTab(self.sample_tab, "Samples")

        self.sample_h_layout = QtWidgets.QHBoxLayout()
        self.sample_tab.setLayout(self.sample_h_layout)

        self.sample_list = QtWidgets.QListView()
        self.sample_list.selectionChanged = self.sample_list_selection_ui
        self.sample_h_layout.addWidget(self.sample_list, 1)

        self.sample_edit = self.get_sample_edit_widget()
        self.sample_edit.hide()
        self.sample_h_layout.addWidget(self.sample_edit, 1)

        self.key_group_tab = QtWidgets.QWidget()
        self.tab_widget.addTab(self.sample_tab, "Key Groups")

        self.key_group_h_layout = QtWidgets.QHBoxLayout()
        self.key_group_tab.setLayout(self.key_group_h_layout)

        self.key_group_list = QtWidgets.QListView()
        self.key_group_list.selectionChanged = self.key_group_list_selection_ui
        self.key_group_h_layout.addWidget(self.key_group_list, 1)

        self.key_group_edit = self.get_key_group_edit_widget()
        self.key_group_edit.hide()
        self.key_group_h_layout.addWidget(self.key_group_edit, 1)

        self.program_tab = QtWidgets.QWidget()
        self.tab_widget.addTab(self.sample_tab, "Programs")

        self.program_h_layout = QtWidgets.QHBoxLayout()
        self.program_tab.setLayout(self.program_h_layout)

        self.program_list = QtWidgets.QListView()
        self.program_list.selectionChanged = self.program_list_selection_ui
        self.program_h_layout.addWidget(self.program_list, 1)

        self.program_edit = self.get_program_edit_widget()
        self.program_edit.hide()
        self.program_h_layout.addWidget(self.program_edit, 1)

        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_btn.clicked.connect(self.save_btn_click)
        self.v_layout.addWidget(self.save_btn, 1)

    def get_sample_edit_widget(self):
        return QtWidgets.QWidget()

    def get_key_group_edit_widget(self):
        return QtWidgets.QWidget()

    def get_program_edit_widget(self):
        return QtWidgets.QWidget()

    def sample_list_selection_ui(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection):
        QtWidgets.QListView.selectionChanged(self.sample_list, selected, deselected)
        if selected.indexes():
            self.sample_list_selection(selected.indexes()[0])
        else:
            self.sample_list_selection(QtCore.QModelIndex())

    def sample_list_selection(self, selected: QtCore.QModelIndex):
        pass

    def key_group_list_selection_ui(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection):
        QtWidgets.QListView.selectionChanged(self.key_group_list, selected, deselected)
        if selected.indexes():
            self.key_group_list_selection(selected.indexes()[0])
        else:
            self.key_group_list_selection(QtCore.QModelIndex())

    def key_group_list_selection(self, selected: QtCore.QModelIndex):
        pass

    def program_list_selection_ui(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection):
        QtWidgets.QListView.selectionChanged(self.program_list, selected, deselected)
        if selected.indexes():
            self.program_list_selection(selected.indexes()[0])
        else:
            self.program_list_selection(QtCore.QModelIndex())

    def program_list_selection(self, selected: QtCore.QModelIndex):
        pass

    def save_btn_click(self):
        pass
