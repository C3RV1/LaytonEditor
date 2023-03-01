from PySide6 import QtWidgets, QtGui, QtCore


class WaitUI(QtWidgets.QWidget):
    def __init__(self):
        super(WaitUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.tap_checkbox = QtWidgets.QCheckBox("Tap")
        self.tap_checkbox.stateChanged.connect(self.tap_edit)
        self.form_layout.addWidget(self.tap_checkbox)

        self.frames_checkbox = QtWidgets.QCheckBox("Frames")
        self.frames_checkbox.stateChanged.connect(self.frames_edit)
        self.form_layout.addWidget(self.frames_checkbox)

        self.frame_value = QtWidgets.QSpinBox()
        self.frame_value.setRange(0, 100000)
        self.form_layout.addRow("Frames", self.frame_value)

    def tap_edit(self, state: int):
        pass

    def frames_edit(self, state: int):
        pass
