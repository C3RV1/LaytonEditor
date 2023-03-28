from gui.ui.command_editor.CommandListWidget import CommandListEditorUI
from .CommandListModel import CommandListModel
from .ContextMenu import CommandListContextMenu
from .commands.CommandEditor import CommandEditor
from PySide6 import QtCore, QtWidgets


class CommandListEditor(CommandListEditorUI):
    def __init__(self, get_widget_function, command_parser, context_menu_structure):
        super().__init__()
        self.active_editor: [CommandEditor] = None
        self.get_widget_func = get_widget_function
        self.command_model = CommandListModel(command_parser)
        self.context_menu = CommandListContextMenu(context_menu_structure)

    def clear_selection(self):
        self.command_list.setCurrentIndex(QtCore.QModelIndex())

    def save(self):
        if isinstance(self.active_editor, CommandEditor):
            self.active_editor.save()

    def set_gds_and_data(self, gds, **kwargs):
        self.command_model.set_gds_and_data(gds, **kwargs)
        self.command_list.setModel(self.command_model)

    def command_list_selection(self, selected: QtCore.QModelIndex):
        if self.active_editor is not None:
            self.active_editor: CommandEditor
            if isinstance(self.active_editor, CommandEditor):
                self.active_editor.save()
            if isinstance(self.active_editor, QtWidgets.QWidget):
                self.h_layout.removeWidget(self.active_editor)
                self.active_editor.deleteLater()
            self.active_editor = None

        if not selected.isValid():
            return

        self.active_editor = self.get_widget_func(
            selected.data(QtCore.Qt.ItemDataRole.UserRole),
            **self.command_model.cmd_data
        )
        if isinstance(self.active_editor, QtWidgets.QWidget):
            self.h_layout.addWidget(self.active_editor, 1)

    def command_list_context_menu(self, point: QtCore.QPoint):
        self.context_menu.exec(self.command_list.mapToGlobal(point))

