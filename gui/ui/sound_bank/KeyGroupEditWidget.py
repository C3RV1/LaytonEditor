from PySide6 import QtCore, QtWidgets, QtGui


class KeyGroupEditWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(KeyGroupEditWidgetUI, self).__init__(*args, **kwargs)

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.polyphony = QtWidgets.QSpinBox()
        self.polyphony.setRange(0, 255)
        self.form_layout.addRow("Polyphony", self.polyphony)

        self.priority = QtWidgets.QSpinBox()
        self.priority.setRange(0, 255)
        self.form_layout.addRow("Priority", self.priority)

        self.voice_channel_low = QtWidgets.QSpinBox()
        self.voice_channel_low.setRange(0, 255)
        self.form_layout.addRow("Voice channel low", self.voice_channel_low)

        self.voice_channel_high = QtWidgets.QSpinBox()
        self.voice_channel_high.setRange(0, 255)
        self.form_layout.addRow("Voice channel high", self.voice_channel_high)
