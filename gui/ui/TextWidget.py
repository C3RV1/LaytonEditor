from PySide6 import QtCore, QtWidgets, QtGui


class TextWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(TextWidgetUI, self).__init__(*args, **kwargs)

        self.v_layout = QtWidgets.QVBoxLayout()

        self.text_editor = QtWidgets.QPlainTextEdit(self)

        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_btn.clicked.connect(self.save_btn_click)

        self.v_layout.addWidget(self.text_editor, 4)
        self.v_layout.addWidget(self.save_btn, 1)

        self.setLayout(self.v_layout)

    def save_btn_click(self):
        pass
