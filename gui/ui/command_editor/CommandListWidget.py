from PySide6 import QtCore, QtWidgets, QtGui


class CommandListEditorUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.h_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.h_layout)

        self.command_list = QtWidgets.QListView()
        self.command_list.setMovement(QtWidgets.QListView.Movement.Snap)
        self.command_list.setDragDropMode(QtWidgets.QListView.DragDropMode.InternalMove)
        self.command_list.setSelectionMode(QtWidgets.QListView.SelectionMode.SingleSelection)
        self.command_list.setAcceptDrops(True)
        self.command_list.setDragEnabled(True)
        self.command_list.setDropIndicatorShown(True)
        self.command_list.selectionChanged = self.command_list_selection_ui
        self.command_list.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.command_list.customContextMenuRequested.connect(self.command_list_context_menu)
        self.h_layout.addWidget(self.command_list, 1)

    def command_list_selection_ui(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection):
        QtWidgets.QListView.selectionChanged(self.command_list, selected, deselected)
        if selected.indexes():
            self.command_list_selection(selected.indexes()[0])
        else:
            self.command_list_selection(QtCore.QModelIndex())

    def command_list_selection(self, selected: QtCore.QModelIndex):
        pass

    def command_list_context_menu(self, point: QtCore.QPoint):
        pass
