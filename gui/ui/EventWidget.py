from PySide6 import QtCore, QtWidgets, QtGui


class EventWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(EventWidgetUI, self).__init__(*args, **kwargs)

        self.v_layout = QtWidgets.QVBoxLayout()

        self.tab_widget = QtWidgets.QTabWidget(self)

        self.character_widget = QtWidgets.QWidget(self.tab_widget)
        self.character_widget_layout = QtWidgets.QVBoxLayout()

        self.character_table = QtWidgets.QTableView(self.character_widget)
        self.character_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.character_widget_layout.addWidget(self.character_table)

        self.character_btn_layout = QtWidgets.QHBoxLayout()

        self.add_character = QtWidgets.QPushButton("Add Character")
        self.add_character.clicked.connect(self.add_character_click)
        self.remove_character = QtWidgets.QPushButton("Remove Character")
        self.remove_character.clicked.connect(self.remove_character_click)

        self.character_btn_layout.addWidget(self.add_character)
        self.character_btn_layout.addWidget(self.remove_character)
        self.character_widget_layout.addLayout(self.character_btn_layout)

        self.character_widget.setLayout(self.character_widget_layout)

        self.tab_widget.addTab(self.character_widget, "Properties")

        self.text_editor = QtWidgets.QPlainTextEdit(self.tab_widget)
        self.tab_widget.addTab(self.text_editor, "Script")

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
