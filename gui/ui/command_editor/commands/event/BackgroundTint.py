from PySide6 import QtWidgets, QtGui, QtCore


class BackgroundTintUI(QtWidgets.QWidget):
    def __init__(self):
        super(BackgroundTintUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.color = QtWidgets.QColorDialog()
        self.color.setOption(QtWidgets.QColorDialog.ColorDialogOption.NoButtons, True)
        self.color.setOption(QtWidgets.QColorDialog.ColorDialogOption.ShowAlphaChannel, True)
        self.form_layout.addWidget(self.color)
