from PySide6 import QtWidgets, QtCore, QtGui


class LFOEditWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(LFOEditWidgetUI, self).__init__(*args, **kwargs)

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.destination = QtWidgets.QComboBox()
        self.destination.addItem("None", 0)
        self.destination.addItem("Pitch", 1)
        self.destination.addItem("Volume", 2)
        self.destination.addItem("Pan", 3)
        self.destination.addItem("Low Pass/Cut Off Filter", 4)
        self.form_layout.addRow("Destination", self.destination)

        self.w_shape = QtWidgets.QComboBox()
        self.w_shape.addItem("None?", 0)
        self.w_shape.addItem("Square?", 1)
        self.w_shape.addItem("Triangle?", 2)
        self.w_shape.addItem("Sinus?", 3)
        self.w_shape.addItem("?", 4)
        self.w_shape.addItem("Saw?", 5)
        self.w_shape.addItem("Noise?", 6)
        self.w_shape.addItem("Random?", 7)
        self.form_layout.addRow("Wave Shape", self.w_shape)

        self.rate = QtWidgets.QSpinBox()
        self.rate.setRange(0, 16_777_215)
        self.form_layout.addRow("Rate", self.rate)

        self.depth = QtWidgets.QSpinBox()
        self.depth.setRange(0, 16_777_215)
        self.form_layout.addRow("Depth", self.depth)

        self.delay = QtWidgets.QSpinBox()
        self.delay.setToolTip("Delay until the LFO starts in milliseconds.")
        self.depth.setRange(0, 16_777_215)
        self.form_layout.addRow("Delay", self.delay)
