from PySide6 import QtWidgets, QtGui, QtCore


class DialogueUI(QtWidgets.QWidget):
    def __init__(self):
        super(DialogueUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.character = QtWidgets.QComboBox()
        self.form_layout.addRow("Character", self.character)

        self.start_anim = QtWidgets.QLineEdit()
        self.form_layout.addRow("Start Animation", self.start_anim)

        self.end_anim = QtWidgets.QLineEdit()
        self.form_layout.addRow("End Animation", self.end_anim)

        self.pitch = QtWidgets.QSpinBox()
        self.form_layout.addRow("Pitch", self.pitch)

        self.text = QtWidgets.QPlainTextEdit()
        self.form_layout.addRow("Text", self.text)
