from PySide6 import QtWidgets, QtGui, QtCore


class MusicFadeUI(QtWidgets.QWidget):
    def __init__(self):
        super(MusicFadeUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.fade_type = QtWidgets.QComboBox()
        self.fade_type.addItem("In", 0x8b)
        self.fade_type.addItem("Out", 0x8a)
        self.form_layout.addRow("Fade Type", self.fade_type)

        self.time_def_id = QtWidgets.QSpinBox()
        self.time_def_id.setMaximum(65536)
        self.form_layout.addRow("Time Definition ID", self.time_def_id)
