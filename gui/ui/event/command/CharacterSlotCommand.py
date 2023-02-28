from PySide6 import QtWidgets, QtGui, QtCore


class CharacterSlotCommandUI(QtWidgets.QWidget):
    def __init__(self):
        super(CharacterSlotCommandUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.character = QtWidgets.QComboBox()
        self.form_layout.addRow("Character", self.character)

        self.slot = QtWidgets.QComboBox()
        self.slot_names = {
            0: "Left 1",
            1: "Center (looking right)",
            2: "Right 1",
            3: "Left 2",
            4: "Left Center",
            5: "Right Center",
            6: "Right 2"
        }

        for i, name in self.slot_names.items():
            self.slot.addItem(name, i)
        self.form_layout.addRow("Slot", self.slot)
