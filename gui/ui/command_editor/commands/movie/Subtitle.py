from PySide6 import QtWidgets, QtGui, QtCore


class SubtitleUI(QtWidgets.QWidget):
    def __init__(self):
        super(SubtitleUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.start_time = QtWidgets.QDoubleSpinBox()
        self.start_time.setMaximum(100000.0)
        self.form_layout.addRow("Start Time (sec)", self.start_time)

        self.end_time = QtWidgets.QDoubleSpinBox()
        self.end_time.setMaximum(100000.0)
        self.form_layout.addRow("End Time (sec)", self.end_time)

        self.sub_text = QtWidgets.QPlainTextEdit()
        self.form_layout.addRow("Text", self.sub_text)
