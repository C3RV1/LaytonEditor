from PySide6 import QtCore, QtWidgets, QtGui


class CharacterNamesWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.v_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.v_layout)

        self.table_widget = QtWidgets.QTableWidget()
        self.v_layout.addWidget(self.table_widget)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.v_layout.addLayout(self.buttons_layout)

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self.save_clicked)
        self.buttons_layout.addWidget(self.save_button)

        self.save_button = QtWidgets.QPushButton("Reset")
        self.save_button.clicked.connect(self.save_clicked)
        self.buttons_layout.addWidget(self.save_button)

    def save_clicked(self):
        pass

    def reset_clicked(self):
        pass
