from PySide6 import QtWidgets, QtGui, QtCore


class SendPuzzlesToGrannyRUI(QtWidgets.QWidget):
    def __init__(self):
        super(SendPuzzlesToGrannyRUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.puzzle_group_id = QtWidgets.QSpinBox()
        self.puzzle_group_id.setRange(0, 10000)
        self.form_layout.addRow("Puzzle Group ID", self.puzzle_group_id)
