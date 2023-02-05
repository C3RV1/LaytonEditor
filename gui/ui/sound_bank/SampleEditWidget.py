from PySide6 import QtCore, QtWidgets, QtGui


class SampleEditWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SampleEditWidgetUI, self).__init__(*args, **kwargs)

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        # TODO: Sliders instead of spinbox?
        self.fine_tune = QtWidgets.QSpinBox()
        self.fine_tune.setRange(-128, 127)
        self.form_layout.addRow("Fine Tune", self.fine_tune)

        self.coarse_tune = QtWidgets.QSpinBox()
        self.coarse_tune.setRange(-128, 127)
        self.form_layout.addRow("Coarse Tune", self.coarse_tune)

        self.root_key = QtWidgets.QSpinBox()
        self.root_key.setRange(-128, 127)
        self.form_layout.addRow("Root Key", self.root_key)

        self.volume = QtWidgets.QSpinBox()
        self.volume.setRange(0, 127)
        self.form_layout.addRow("Volume", self.volume)

        self.pan = QtWidgets.QSpinBox()
        self.pan.setRange(0, 127)
        self.form_layout.addRow("Pan", self.pan)

        self.loop_enabled = QtWidgets.QCheckBox("Loop Enabled")
        self.form_layout.addRow(self.loop_enabled)

        self.sample_rate = QtWidgets.QSpinBox()
        self.form_layout.addRow("Sample Rate", self.sample_rate)

        # TODO: Sample format?

        # TODO: Loop live preview?
        self.loop_beginning = QtWidgets.QSpinBox()
        self.form_layout.addRow("Loop Beginning", self.loop_beginning)

        self.loop_length = QtWidgets.QSpinBox()
        self.form_layout.addRow("Loop Length", self.loop_length)

        self.enable_envelope = QtWidgets.QCheckBox("Enable Envelope")
        self.form_layout.addRow(self.enable_envelope)

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

        play_pixmap = QtWidgets.QStyle.StandardPixmap.SP_MediaPlay
        play_icon = self.style().standardIcon(play_pixmap)
        self.play_button = QtWidgets.QPushButton(play_icon)
