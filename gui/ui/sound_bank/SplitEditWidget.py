from PySide6 import QtCore, QtWidgets, QtGui


class SplitEditWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SplitEditWidgetUI, self).__init__(*args, **kwargs)

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.low_key = QtWidgets.QSpinBox()
        self.form_layout.addRow("Low Key", self.low_key)

        self.high_key = QtWidgets.QSpinBox()
        self.form_layout.addRow("High Key", self.high_key)

        self.low_vel = QtWidgets.QSpinBox()
        self.form_layout.addRow("Low Velocity", self.low_vel)

        self.high_vel = QtWidgets.QSpinBox()
        self.form_layout.addRow("High Velocity", self.high_vel)

        self.sample_id = QtWidgets.QSpinBox()
        self.form_layout.addRow("Sample ID", self.sample_id)

        self.fine_tune = QtWidgets.QSpinBox()
        self.form_layout.addRow("Fine Tune", self.fine_tune)

        self.coarse_tune = QtWidgets.QSpinBox()
        self.form_layout.addRow("Coarse Tune", self.coarse_tune)

        self.root_key = QtWidgets.QSpinBox()
        self.form_layout.addRow("Root Key", self.root_key)

        self.volume = QtWidgets.QSpinBox()
        self.form_layout.addRow("Volume", self.volume)

        self.pan = QtWidgets.QSpinBox()
        self.form_layout.addRow("Pan", self.pan)

        self.key_group_id = QtWidgets.QSpinBox()
        self.form_layout.addRow("Key Group ID", self.key_group_id)

        self.envelope_enabled = QtWidgets.QCheckBox("Envelope enabled")
        self.form_layout.addRow(self.envelope_enabled)

        self.attack_volume = QtWidgets.QSpinBox()
        self.form_layout.addRow("Attack Volume", self.attack_volume)

        self.attack = QtWidgets.QSpinBox()
        self.form_layout.addRow("Attack", self.attack)

        self.decay = QtWidgets.QSpinBox()
        self.form_layout.addRow("Decay", self.decay)

        self.decay2 = QtWidgets.QSpinBox()
        self.form_layout.addRow("Decay2", self.decay2)

        self.sustain = QtWidgets.QSpinBox()
        self.form_layout.addRow("Sustain", self.sustain)

        self.hold = QtWidgets.QSpinBox()
        self.form_layout.addRow("Hold", self.hold)

        self.release = QtWidgets.QSpinBox()
        self.form_layout.addRow("Release", self.release)
