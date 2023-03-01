from PySide6 import QtWidgets, QtGui, QtCore


class MysteryUI(QtWidgets.QWidget):
    def __init__(self):
        super(MysteryUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.mode = QtWidgets.QComboBox()
        self.mode.addItem("Reveal", 0x71)
        self.mode.addItem("Solve", 0x7d)
        self.form_layout.addWidget(self.mode)

        self.mystery_id = QtWidgets.QSpinBox()
        self.form_layout.addRow("Mystery ID", self.mystery_id)
