from PySide6 import QtWidgets, QtGui, QtCore


class MusicPlayUI(QtWidgets.QWidget):
    def __init__(self):
        super(MusicPlayUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.music_id = QtWidgets.QSpinBox()
        self.music_id.setMaximum(1000)
        self.form_layout.addRow("Music ID", self.music_id)

        self.volume = QtWidgets.QDoubleSpinBox()
        self.form_layout.addRow("Volume", self.volume)

        self.variation_checkbox = QtWidgets.QCheckBox("Use Variation Command 0x8c")
        self.variation_checkbox.stateChanged.connect(self.variation_edit)
        self.form_layout.addWidget(self.variation_checkbox)

        self.fade_in_frames = QtWidgets.QSpinBox()
        self.fade_in_frames.setMaximum(65536)
        self.form_layout.addRow("Fade In Frames", self.fade_in_frames)

    def variation_edit(self, state: int):
        pass
