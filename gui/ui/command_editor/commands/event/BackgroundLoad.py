from PySide6 import QtWidgets, QtGui, QtCore


class BackgroundLoadUI(QtWidgets.QWidget):
    def __init__(self):
        super(BackgroundLoadUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.screens = QtWidgets.QComboBox()
        self.screens.addItem("Bottom", 0x21)
        self.screens.addItem("Top", 0x22)
        self.form_layout.addRow("Screen", self.screens)

        self.path = QtWidgets.QLineEdit()
        self.form_layout.addRow("Path", self.path)
