from PySide6 import QtWidgets, QtGui, QtCore


class CharacterAnimationUI(QtWidgets.QWidget):
    def __init__(self):
        super(CharacterAnimationUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.character = QtWidgets.QComboBox()
        self.form_layout.addRow("Character", self.character)

        self.animation = QtWidgets.QLineEdit()
        self.form_layout.addWidget(self.animation)
