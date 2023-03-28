from PySide6 import QtCore, QtWidgets, QtGui
from .EventPropertiesWidget import EventPropertiesWidgetUI
from gui.ui.command_editor.CommandListWidget import CommandListEditorUI


class EventWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(EventWidgetUI, self).__init__(*args, **kwargs)

        self.v_layout = QtWidgets.QVBoxLayout()

        self.tab_widget = QtWidgets.QTabWidget(self)

        self.character_widget = self.get_event_properties_widget()
        self.tab_widget.addTab(self.character_widget, "Properties")

        self.script_editor = self.get_command_editor_widget()
        self.tab_widget.addTab(self.script_editor, "Visual Script")

        self.btn_window_layout = QtWidgets.QVBoxLayout()

        self.preview_btn = QtWidgets.QPushButton("Preview")
        self.preview_btn.clicked.connect(self.preview_click)
        self.btn_window_layout.addWidget(self.preview_btn, 1)

        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_btn.clicked.connect(self.save_click)
        self.btn_window_layout.addWidget(self.save_btn, 1)

        self.v_layout.addWidget(self.tab_widget, 4)
        self.v_layout.addLayout(self.btn_window_layout, 1)

        self.setLayout(self.v_layout)

        self.tab_widget.currentChanged.connect(self.tab_changed)

    def get_command_editor_widget(self):
        return CommandListEditorUI()

    def tab_changed(self, current: int):
        pass

    def get_event_properties_widget(self):
        return EventPropertiesWidgetUI(self)

    def preview_click(self):
        pass

    def save_click(self):
        pass

    def add_character_click(self):
        pass

    def remove_character_click(self):
        pass
