from PySide6 import QtWidgets, QtGui, QtCore


class BackgroundShakeUI(QtWidgets.QWidget):
    def __init__(self):
        super(BackgroundShakeUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.fade_screens = QtWidgets.QComboBox()
        self.fade_screens.addItem("Bottom", 0x6a)
        self.fade_screens.addItem("Top", 0x6b)
        self.form_layout.addRow("Screen", self.fade_screens)

        self.unk0 = QtWidgets.QSpinBox()
        self.unk0.setRange(0, 10000)
        self.form_layout.addRow("Unk0 (30 usually)", self.unk0)
