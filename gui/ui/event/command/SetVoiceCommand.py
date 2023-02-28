from PySide6 import QtWidgets, QtGui, QtCore


class SetVoiceCommandUI(QtWidgets.QWidget):
    def __init__(self):
        super(SetVoiceCommandUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.voice_clip = QtWidgets.QSpinBox()
        self.form_layout.addRow("Voice Clip", self.voice_clip)
