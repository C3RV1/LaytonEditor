from PySide6 import QtWidgets, QtGui, QtCore


class SetModeUI(QtWidgets.QWidget):
    def __init__(self):
        super(SetModeUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.next_mode_type = QtWidgets.QComboBox()
        self.next_mode_type.addItem("Next Mode", 0x6)
        self.next_mode_type.addItem("Queue Following Mode", 0x7)
        self.form_layout.addRow(self.next_mode_type)

        self.mode = QtWidgets.QComboBox()
        self.mode_list = {
            "narration": "Narration",
            "movie": "Movie",
            "puzzle": "Puzzle",
            "drama event": "Event",
            "room": "Place",
            "name": "Name",
            "staff": "Staff",
            "nazoba": "Nazoba",
            "menu": "Menu",
            "challenge": "Challenge",
            "sub herb": "Herbal tea",
            "sub camera": "Camera",
            "sub ham": "Hamster",
            "passcode": "Passcode"
        }
        for key, value in self.mode_list.items():
            self.mode.addItem(value, key)
        self.form_layout.addRow("Mode", self.mode)
