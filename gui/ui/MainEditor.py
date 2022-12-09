from PySide6 import QtCore, QtWidgets, QtGui


class MainEditorUI(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainEditorUI, self).__init__(*args, **kwargs)

        menu_bar = self.menuBar()
        self.file_menu = menu_bar.addMenu("File")

        self.file_open_action = QtGui.QAction("Open ROM", self)
        self.file_menu.addAction(self.file_open_action)
        self.file_open_action.triggered.connect(self.file_menu_open)

        self.file_save_action = QtGui.QAction("Save ROM", self)
        self.file_menu.addAction(self.file_save_action)
        self.file_save_action.triggered.connect(self.file_menu_save)
        self.file_save_action.setEnabled(False)

        self.file_save_as_action = QtGui.QAction("Save ROM as...", self)
        self.file_menu.addAction(self.file_save_as_action)
        self.file_save_as_action.triggered.connect(self.file_menu_save_as)
        self.file_save_as_action.setEnabled(False)

        self.window = QtWidgets.QWidget()

        self.horizontal_layout = QtWidgets.QHBoxLayout()

        self.file_tree = QtWidgets.QTreeView(self.window)
        self.file_tree.setHeaderHidden(True)
        self.file_tree.currentChanged = self.tree_changed_selection
        self.horizontal_layout.addWidget(self.file_tree, 1)

        self.active_editor = QtWidgets.QWidget()
        self.horizontal_layout.addWidget(self.active_editor, 3)

        self.window.setLayout(self.horizontal_layout)
        self.setCentralWidget(self.window)

        self.setFixedSize(QtCore.QSize(1280, 720))

        self.show()

    def file_menu_open(self):
        pass

    def file_menu_save(self):
        pass

    def file_menu_save_as(self):
        pass

    def tree_changed_selection(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex):
        pass