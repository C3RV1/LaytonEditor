from PySide6 import QtWidgets, QtGui, QtCore


class FadeUI(QtWidgets.QWidget):
    def __init__(self):
        super(FadeUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.fade_type = QtWidgets.QComboBox()
        self.fade_type.addItem("In", True)
        self.fade_type.addItem("Out", False)
        self.form_layout.addRow("Fade Type", self.fade_type)

        self.fade_screens = QtWidgets.QComboBox()
        self.fade_screens.addItem("Bottom", 0)
        self.fade_screens.addItem("Top", 1)
        self.fade_screens.addItem("Both", 2)
        self.form_layout.addRow("Screen(s)", self.fade_screens)

        self.fade_duration = QtWidgets.QSpinBox()
        self.fade_duration.setRange(0, 10000)
        self.form_layout.addRow("Duration (frames)", self.fade_duration)

        self.default_duration = QtWidgets.QCheckBox("Default duration")
        self.default_duration.stateChanged.connect(self.default_duration_edit)
        self.form_layout.addWidget(self.default_duration)

    def default_duration_edit(self, state: int):
        pass
