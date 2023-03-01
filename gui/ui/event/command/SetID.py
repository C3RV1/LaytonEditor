from PySide6 import QtWidgets, QtGui, QtCore


class SetIDUI(QtWidgets.QWidget):
    def __init__(self):
        super(SetIDUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.mode = QtWidgets.QComboBox()
        self.mode.addItem("Place", 0x5)
        self.mode.addItem("Movie", 0x8)
        self.mode.addItem("Event", 0x9)
        self.mode.addItem("Puzzle", 0xb)
        self.form_layout.addRow("Mode", self.mode)

        self.value = QtWidgets.QSpinBox()
        self.value.setRange(0, 100000)
        self.form_layout.addRow("ID", self.value)
