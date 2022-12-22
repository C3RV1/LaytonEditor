from PySide6 import QtCore, QtWidgets, QtGui
import enum


class FrameOrders(enum.IntEnum):
    LOOPING = 0
    NO_LOOPING = 1
    CUSTOM = 2


class AnimPropertiesWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(AnimPropertiesWidgetUI, self).__init__(*args, **kwargs)

        self.form_layout = QtWidgets.QFormLayout()

        self.child_x_input = QtWidgets.QSpinBox(self)
        self.child_x_input.valueChanged.connect(self.child_x_edit)
        self.form_layout.addRow("Child X", self.child_x_input)

        self.child_y_input = QtWidgets.QSpinBox(self)
        self.child_y_input.valueChanged.connect(self.child_y_edit)
        self.form_layout.addRow("Child Y", self.child_y_input)

        self.child_anim_index = QtWidgets.QSpinBox(self)
        self.child_anim_index.valueChanged.connect(self.child_anim_edit)
        self.form_layout.addRow("Child Animation Index", self.child_anim_index)

        self.frame_order_input = QtWidgets.QComboBox(self)
        self.frame_order_input.addItem("Looping", FrameOrders.LOOPING)
        self.frame_order_input.addItem("No Looping", FrameOrders.NO_LOOPING)
        self.frame_order_input.addItem("Custom", FrameOrders.CUSTOM)
        self.frame_order_input.currentIndexChanged.connect(self.frame_order_edit)
        self.form_layout.addRow("Frame Order", self.frame_order_input)

        self.setLayout(self.form_layout)

    def child_x_edit(self, value: int):
        pass

    def child_y_edit(self, value: int):
        pass

    def child_anim_edit(self, value: int):
        pass

    def frame_order_edit(self, index: int):
        pass
