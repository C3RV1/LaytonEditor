from PySide6 import QtWidgets, QtGui, QtCore


class UnlockMinigameUI(QtWidgets.QWidget):
    def __init__(self):
        super(UnlockMinigameUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.minigame_id = QtWidgets.QSpinBox()
        self.form_layout.addRow("Minigame ID", self.minigame_id)
