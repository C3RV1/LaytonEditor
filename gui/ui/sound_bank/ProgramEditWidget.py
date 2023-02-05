from PySide6 import QtCore, QtWidgets, QtGui


class ProgramEditWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ProgramEditWidgetUI, self).__init__(*args, **kwargs)

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        # TODO: Sliders instead of spinbox?
        self.fine_tune = QtWidgets.QSpinBox()
        self.coarse_tune = QtWidgets.QSpinBox()
        self.root_key = QtWidgets.QSpinBox()
        self.volume = QtWidgets.QSpinBox()
        self.pan = QtWidgets.QSpinBox()
        self.loop_enabled = QtWidgets.QCheckBox()
        self.sample_rate = QtWidgets.QSpinBox()

        # TODO: Loop live preview?
        self.loop_beginning = QtWidgets.QSpinBox()
        self.loop_length = QtWidgets.QSpinBox()

        self.enable_envelope = QtWidgets.QCheckBox()
        self.attack_volume = QtWidgets.QSpinBox()
        self.attack = QtWidgets.QSpinBox()
        self.decay = QtWidgets.QSpinBox()
        self.decay2 = QtWidgets.QSpinBox()
        self.sustain = QtWidgets.QSpinBox()
        self.hold = QtWidgets.QSpinBox()
        self.release = QtWidgets.QSpinBox()
