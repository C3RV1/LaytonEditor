from PySide6 import QtCore, QtWidgets, QtGui


class TextWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(TextWidgetUI, self).__init__(*args, **kwargs)

        self.v_layout = QtWidgets.QVBoxLayout()

        self.text_editor = QtWidgets.QPlainTextEdit(self)

        self.end_h_layout = QtWidgets.QHBoxLayout()

        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_btn.clicked.connect(self.save_btn_click)
        self.end_h_layout.addWidget(self.save_btn, 2)

        self.encoding_label = QtWidgets.QLabel("Encoding: ")
        self.encoding_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.end_h_layout.addWidget(self.encoding_label, 1)

        self.encoding_combobox = QtWidgets.QComboBox()
        self.encoding_combobox.addItem("CP1252 (EU)")
        self.encoding_combobox.addItem("Shift-jis (JP)")
        self.end_h_layout.addWidget(self.encoding_combobox, 1)

        self.v_layout.addWidget(self.text_editor, 4)
        self.v_layout.addLayout(self.end_h_layout, 1)

        self.setLayout(self.v_layout)

    def save_btn_click(self):
        pass
