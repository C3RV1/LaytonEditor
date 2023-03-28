from PySide6 import QtCore, QtWidgets, QtGui
from gui.ui.command_editor.CommandListWidget import CommandListEditorUI


class ScriptWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ScriptWidgetUI, self).__init__(*args, **kwargs)

        self.v_layout = QtWidgets.QVBoxLayout()

        self.script_editor = self.get_command_editor_widget()

        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_btn.clicked.connect(self.save_btn_click)

        self.v_layout.addWidget(self.script_editor, 4)
        self.v_layout.addWidget(self.save_btn, 1)

        self.setLayout(self.v_layout)

    def get_command_editor_widget(self):
        return CommandListEditorUI()

    def save_btn_click(self):
        pass
