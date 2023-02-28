from PySide6 import QtWidgets, QtGui, QtCore


class CharacterShakeCommandUI(QtWidgets.QWidget):
    def __init__(self):
        super(CharacterShakeCommandUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.character = QtWidgets.QComboBox()
        self.form_layout.addRow("Character", self.character)

        self.duration = QtWidgets.QSpinBox()
        self.form_layout.addRow("Duration?", self.duration)
