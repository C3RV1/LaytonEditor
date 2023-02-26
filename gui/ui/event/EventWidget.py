from PySide6 import QtCore, QtWidgets, QtGui
from .EventPropertiesWidget import EventPropertiesWidgetUI


class EventWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(EventWidgetUI, self).__init__(*args, **kwargs)

        self.v_layout = QtWidgets.QVBoxLayout()

        self.tab_widget = QtWidgets.QTabWidget(self)

        self.character_widget = self.get_event_properties_widget()
        self.tab_widget.addTab(self.character_widget, "Properties")

        self.text_editor = QtWidgets.QPlainTextEdit(self.tab_widget)
        self.tab_widget.addTab(self.text_editor, "Script")

        self.script_editor = QtWidgets.QWidget()
        self.tab_widget.addTab(self.script_editor, "Visual Script")

        self.script_layout = QtWidgets.QHBoxLayout()
        self.script_editor.setLayout(self.script_layout)

        self.command_list = QtWidgets.QListView()
        self.command_list.selectionChanged = self.command_list_selection_ui
        self.script_layout.addWidget(self.command_list, 1)

        self.btn_window_layout = QtWidgets.QGridLayout()

        self.preview_dcc_btn = QtWidgets.QPushButton("Preview DCC")
        self.preview_dcc_btn.clicked.connect(self.preview_dcc_btn_click)
        self.btn_window_layout.addWidget(self.preview_dcc_btn, 0, 0)

        self.save_dcc_btn = QtWidgets.QPushButton("Save DCC")
        self.save_dcc_btn.clicked.connect(self.save_dcc_btn_click)
        self.btn_window_layout.addWidget(self.save_dcc_btn, 1, 0)

        self.preview_ev_script_btn = QtWidgets.QPushButton("Preview EventScript")
        self.preview_ev_script_btn.clicked.connect(self.preview_ev_script_btn_click)
        self.btn_window_layout.addWidget(self.preview_ev_script_btn, 0, 1)

        self.save_ev_script_btn = QtWidgets.QPushButton("Save EventScript")
        self.save_ev_script_btn.clicked.connect(self.save_ev_script_btn_click)
        self.btn_window_layout.addWidget(self.save_ev_script_btn, 1, 1)

        self.v_layout.addWidget(self.tab_widget, 4)
        self.v_layout.addLayout(self.btn_window_layout, 1)

        self.setLayout(self.v_layout)

    def command_list_selection_ui(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection):
        QtWidgets.QListView.selectionChanged(self.command_list, selected, deselected)
        if selected.indexes():
            self.command_list_selection(selected.indexes()[0])
        else:
            self.command_list_selection(QtCore.QModelIndex())

    def command_list_selection(self, selected: QtCore.QModelIndex):
        pass

    def get_event_properties_widget(self):
        return EventPropertiesWidgetUI(self)

    def preview_dcc_btn_click(self):
        pass

    def save_dcc_btn_click(self):
        pass

    def preview_ev_script_btn_click(self):
        pass

    def save_ev_script_btn_click(self):
        pass

    def add_character_click(self):
        pass

    def remove_character_click(self):
        pass
