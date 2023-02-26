from PySide6 import QtWidgets, QtGui, QtCore


class SetModeCommandUI(QtWidgets.QWidget):
    def __init__(self):
        super(SetModeCommandUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.next_mode_type = QtWidgets.QComboBox()
        self.next_mode_type.addItem("Next Mode", 0x6)
        self.next_mode_type.addItem("Queue Following Mode", 0x7)
        self.form_layout.addRow(self.next_mode_type)

        self.value = QtWidgets.QLineEdit()
        self.form_layout.addRow("Mode", self.value)
