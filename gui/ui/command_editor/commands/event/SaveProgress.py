from PySide6 import QtWidgets, QtGui, QtCore


class SaveProgressUI(QtWidgets.QWidget):
    def __init__(self):
        super(SaveProgressUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.next_event = QtWidgets.QSpinBox()
        self.next_event.setRange(0, 100000)
        self.form_layout.addRow("Next Event", self.next_event)
