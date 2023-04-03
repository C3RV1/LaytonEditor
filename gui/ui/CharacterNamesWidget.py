from PySide6 import QtCore, QtWidgets, QtGui


class CharacterNamesWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.v_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.v_layout)

        self.table_widget = QtWidgets.QTableWidget()
        self.v_layout.addWidget(self.table_widget)

        self.save_button = QtWidgets.QPushButton("Save")
        self.v_layout.addWidget(self.save_button)
