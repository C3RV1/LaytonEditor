from PySide6 import QtWidgets, QtGui, QtCore


class CharacterVisibilityUI(QtWidgets.QWidget):
    def __init__(self):
        super(CharacterVisibilityUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.character = QtWidgets.QComboBox()
        self.form_layout.addRow("Character", self.character)

        self.shown = QtWidgets.QComboBox()
        self.shown.addItem("Show", True)
        self.shown.addItem("Hide", False)
        self.form_layout.addWidget(self.shown)

        self.alpha = QtWidgets.QCheckBox("Alpha")
        self.form_layout.addWidget(self.alpha)
