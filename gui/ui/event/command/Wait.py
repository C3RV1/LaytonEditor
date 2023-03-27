from PySide6 import QtWidgets, QtGui, QtCore


class WaitUI(QtWidgets.QWidget):
    def __init__(self):
        super(WaitUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.time_definition = QtWidgets.QCheckBox("From Time Definition")
        self.time_definition.stateChanged.connect(self.time_definition_edit)
        self.form_layout.addWidget(self.time_definition)

        self.time_definition_id = QtWidgets.QSpinBox()
        self.time_definition_id.setMaximum(65535)
        self.form_layout.addRow("Time Definition ID", self.time_definition_id)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.form_layout.addWidget(line)

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

    def time_definition_edit(self, state: int):
        pass
