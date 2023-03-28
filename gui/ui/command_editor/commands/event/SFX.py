from PySide6 import QtWidgets, QtGui, QtCore


class SFXUI(QtWidgets.QWidget):
    def __init__(self):
        super(SFXUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.sfx_id = QtWidgets.QSpinBox()
        self.sfx_id.setRange(0, 10000)
        self.form_layout.addRow("Sound Effect ID", self.sfx_id)

        self.sfx_type = QtWidgets.QComboBox()
        self.sfx_type.addItem("Streamed (SAD)", 0x5d)
        self.sfx_type.addItem("Sequenced (SED)", 0x5e)
        self.form_layout.addRow("Sound Effect Type", self.sfx_type)
