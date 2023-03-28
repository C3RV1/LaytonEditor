from PySide6 import QtWidgets, QtGui, QtCore


class CompanionUI(QtWidgets.QWidget):
    def __init__(self):
        super(CompanionUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.mode = QtWidgets.QComboBox()
        self.mode.addItem("Add", 0x96)
        self.mode.addItem("Remove", 0x97)
        self.form_layout.addWidget(self.mode)

        self.companion_id = QtWidgets.QSpinBox()
        self.form_layout.addRow("Companion ID", self.companion_id)
