from PySide6 import QtWidgets, QtGui, QtCore


class ShowChapterCommandUI(QtWidgets.QWidget):
    def __init__(self):
        super(ShowChapterCommandUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.chapter = QtWidgets.QSpinBox()
        self.form_layout.addRow("Chapter", self.chapter)
