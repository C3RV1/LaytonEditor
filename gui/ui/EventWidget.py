from PySide6 import QtCore, QtWidgets, QtGui


class EventWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(EventWidgetUI, self).__init__(*args, **kwargs)

        self.v_layout = QtWidgets.QVBoxLayout()

        self.text_editor = QtWidgets.QPlainTextEdit(self)

        self.btn_window_layout = QtWidgets.QGridLayout()

        self.preview_dcc_btn = QtWidgets.QPushButton("Preview DCC")
        self.preview_dcc_btn.clicked.connect(self.preview_dcc_btn_click)
        self.btn_window_layout.addWidget(self.preview_dcc_btn, 0, 0)

        self.save_dcc_btn = QtWidgets.QPushButton("Save DCC")
        self.btn_window_layout.addWidget(self.save_dcc_btn, 0, 1)

        self.preview_ev_script_btn = QtWidgets.QPushButton("Preview EventScript")
        self.btn_window_layout.addWidget(self.preview_ev_script_btn, 1, 0)

        self.save_ev_script_btn = QtWidgets.QPushButton("Save EventScript")
        self.btn_window_layout.addWidget(self.save_ev_script_btn, 1, 1)

        self.v_layout.addWidget(self.text_editor, 4)
        self.v_layout.addLayout(self.btn_window_layout, 1)

        self.setLayout(self.v_layout)

    def preview_dcc_btn_click(self):
        print("Preview DCC")
