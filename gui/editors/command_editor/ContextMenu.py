from typing import Callable

from PySide6 import QtWidgets, QtGui
from .command_parsers import CommandFactory
from formats.gds import GDS, GDSCommand


class CommandListContextMenu(QtWidgets.QMenu):
    def __init__(self, structure: tuple, on_pre_update: Callable, on_update: Callable,
                 on_remove: Callable):
        super().__init__()

        self.gds: GDS = None
        self.data: dict = {}
        self.on_update = on_update
        self.on_pre_update = on_pre_update
        self.on_remove = on_remove

        self.showing_remove = False
        self.remove_action: QtGui.QAction = None
        self.active_command: GDSCommand = None

        self.clear_action = self.addAction("Clear All")
        self.clear_action.triggered.connect(self.clear_all_command)
        self.addSeparator()

        def helper(menu: QtWidgets.QMenu, menu_struct: tuple):
            for name, element in menu_struct:
                if isinstance(element, tuple):
                    new_menu = menu.addMenu(name)
                    helper(new_menu, element)
                elif name is None:
                    menu.addSeparator()
                else:
                    new_action = menu.addAction(name)
                    if isinstance(element, CommandFactory):
                        new_action.triggered.connect(lambda *args, factory=element: self.action_clicked(factory))
        helper(self, structure)

    def show_remove(self, active_command):
        if self.showing_remove:
            self.hide_remove()
        self.showing_remove = True
        first_action = self.actions()[0]
        self.remove_action = QtGui.QAction("Remove")
        self.remove_action.triggered.connect(self.remove_command)
        self.insertAction(first_action, self.remove_action)
        self.active_command = active_command

    def hide_remove(self):
        if not self.showing_remove:
            return
        self.showing_remove = False
        self.removeAction(self.remove_action)
        self.remove_action.deleteLater()
        self.remove_action = None
        self.active_command = None

    def remove_command(self):
        self.on_pre_update()
        self.gds.commands.remove(self.active_command)
        self.on_update()
        self.on_remove()

    def clear_all_command(self):
        self.on_pre_update()
        self.gds.commands = []
        self.on_update()
        self.on_remove()

    def set_gds_and_data(self, gds: GDS, **kwargs):
        self.gds = gds
        self.data = kwargs

    def action_clicked(self, factory: CommandFactory):
        new_command = factory.create(**self.data)
        if new_command is None:
            return
        self.on_pre_update()
        self.gds.commands.append(new_command)
        self.on_update()


