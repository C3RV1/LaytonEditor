from PySide6 import QtCore, QtWidgets, QtGui
from .command_editor.CommandListWidget import CommandListEditorUI


class MovieWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.v_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.v_layout)

        self.subtitle_editor = self.get_command_editor()
        self.v_layout.addWidget(self.subtitle_editor)

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self.save_click)
        self.v_layout.addWidget(self.save_button)

    def get_command_editor(self):
        return CommandListEditorUI()

    def save_click(self):
        pass
