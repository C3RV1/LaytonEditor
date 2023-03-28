from PySide6 import QtWidgets


class CommandListContextMenu(QtWidgets.QMenu):
    def __init__(self, structure: tuple):
        super().__init__()

        def helper(menu: QtWidgets.QMenu, menu_struct: tuple):
            for name, element in menu_struct:
                if isinstance(element, tuple):
                    new_menu = menu.addMenu(name)
                    helper(new_menu, element)
                elif name is None:
                    menu.addSeparator()
                else:
                    new_action = menu.addAction(name)
        helper(self, structure)

