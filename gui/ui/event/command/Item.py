from PySide6 import QtWidgets, QtGui, QtCore


class ItemUI(QtWidgets.QWidget):
    def __init__(self):
        super(ItemUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.mode = QtWidgets.QComboBox()
        self.mode.addItem("Pick up", 0x77)
        self.mode.addItem("Remove", 0x7a)
        self.form_layout.addWidget(self.mode)

        self.item_id = QtWidgets.QSpinBox()
        self.form_layout.addRow("Item ID", self.item_id)
