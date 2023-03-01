from PySide6 import QtWidgets


class UnknownUI(QtWidgets.QWidget):
    def __init__(self):
        super(UnknownUI, self).__init__()

        self.sizer = QtWidgets.QFormLayout()

        self.command_input = QtWidgets.QLineEdit()
        self.sizer.addRow("DCC Code", self.command_input)

        self.setLayout(self.sizer)
