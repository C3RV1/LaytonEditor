from PySide6 import QtCore, QtWidgets, QtGui


class PuzzleWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(PuzzleWidgetUI, self).__init__(*args, **kwargs)

        self.v_layout = QtWidgets.QVBoxLayout()

        self.text_editor = QtWidgets.QPlainTextEdit(self)

        self.preview_dcc_btn = QtWidgets.QPushButton("Preview DCC")
        self.preview_dcc_btn.clicked.connect(self.preview_dcc_btn_click)

        self.save_dcc_btn = QtWidgets.QPushButton("Save DCC")
        self.save_dcc_btn.clicked.connect(self.save_dcc_btn_click)

        self.v_layout.addWidget(self.text_editor, 8)
        self.v_layout.addWidget(self.preview_dcc_btn, 1)
        self.v_layout.addWidget(self.save_dcc_btn, 1)

        self.setLayout(self.v_layout)

    def preview_dcc_btn_click(self):
        pass

    def save_dcc_btn_click(self):
        pass
