from PySide6 import QtCore, QtWidgets, QtGui


class BackgroundWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(BackgroundWidgetUI, self).__init__(*args, **kwargs)

        self.v_layout = QtWidgets.QVBoxLayout()
        self.v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.image_preview = QtWidgets.QLabel()
        self.v_layout.addWidget(self.image_preview)

        self.setLayout(self.v_layout)
