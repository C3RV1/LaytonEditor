from PySide6 import QtWidgets, QtGui, QtCore


class StartTeaUI(QtWidgets.QWidget):
    def __init__(self):
        super(StartTeaUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.hint_id = QtWidgets.QSpinBox()
        self.hint_id.setRange(0, 10000)
        self.form_layout.addRow("Hint ID", self.hint_id)

        self.solution_id = QtWidgets.QSpinBox()
        self.solution_id.setRange(0, 10000)
        self.form_layout.addRow("Solution ID", self.solution_id)
