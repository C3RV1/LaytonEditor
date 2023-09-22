from PySide6 import QtCore, QtWidgets, QtGui


class BaseTab(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.h_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.h_layout)

        self.file_tree = QtWidgets.QTreeView(self)
        self.file_tree.setSelectionMode(self.file_tree.SelectionMode.SingleSelection)
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(
            self.file_tree_context_menu
        )
        self.file_tree.currentChanged = self.tree_changed_selection_ui
        self.h_layout.addWidget(self.file_tree, 1)

        self.empty_editor = QtWidgets.QWidget()
        self.h_layout.addWidget(self.empty_editor, 3)

        self.ft_context_menu = QtWidgets.QMenu()

    def tree_changed_selection_ui(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex):
        QtWidgets.QTreeView.currentChanged(self.file_tree, current, previous)
        self.tree_changed_selection(current, previous)

    def tree_changed_selection(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex):
        pass

    def file_tree_context_menu(self, point: QtCore.QPoint):
        index = self.file_tree.indexAt(point)
        if index.isValid():
            self.ft_context_menu.clear()
            category = index.internalPointer().category
            actions = category.get_context_menu(index, self.tree_changed_selection)
            if not actions:
                return
            for i, action_data in enumerate(actions):
                if action_data is None and i != 0 and i != len(actions) - 1:
                    self.ft_context_menu.addSeparator()
                    continue
                elif action_data is None:
                    continue
                name, callback = action_data
                action = QtGui.QAction(name, self.ft_context_menu)
                action.triggered.connect(callback)
                self.ft_context_menu.addAction(action)
            self.ft_context_menu.exec(self.file_tree.mapToGlobal(point))
