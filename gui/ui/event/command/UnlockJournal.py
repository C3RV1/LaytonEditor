from PySide6 import QtWidgets, QtGui, QtCore


class UnlockJournalUI(QtWidgets.QWidget):
    def __init__(self):
        super(UnlockJournalUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.entry_id = QtWidgets.QSpinBox()
        self.form_layout.addRow("Entry ID", self.entry_id)
