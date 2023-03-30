from PySide6 import QtCore, QtWidgets, QtGui


class MainEditorUI(QtWidgets.QMainWindow):
    FILE_ICON = None
    DIR_ICON = None

    def __init__(self, *args, **kwargs):
        super(MainEditorUI, self).__init__(*args, **kwargs)

        self.setWindowTitle("Layton Editor")

        save_pixmap = QtWidgets.QStyle.StandardPixmap.SP_DialogSaveButton
        save_icon = self.style().standardIcon(save_pixmap)
        open_pixmap = QtWidgets.QStyle.StandardPixmap.SP_DialogOpenButton
        open_icon = self.style().standardIcon(open_pixmap)

        file_pixmap = QtWidgets.QStyle.StandardPixmap.SP_FileIcon
        MainEditorUI.FILE_ICON = self.style().standardIcon(file_pixmap)

        dir_pixmap = QtWidgets.QStyle.StandardPixmap.SP_DirIcon
        MainEditorUI.DIR_ICON = self.style().standardIcon(dir_pixmap)

        menu_bar = self.menuBar()
        self.file_menu = menu_bar.addMenu("File")

        self.file_open_action = self.file_menu.addAction("Open ROM")
        self.file_open_action.setIcon(open_icon)
        self.file_open_action.triggered.connect(self.file_menu_open)

        self.file_save_action = self.file_menu.addAction("Save ROM")
        self.file_save_action.setIcon(save_icon)
        self.file_save_action.triggered.connect(self.file_menu_save)
        self.file_save_action.setEnabled(False)

        self.file_save_as_action = self.file_menu.addAction("Save ROM as...")
        self.file_save_as_action.setIcon(save_icon)
        self.file_save_as_action.triggered.connect(self.file_menu_save_as)
        self.file_save_as_action.setEnabled(False)

        self.settings_menu = menu_bar.addMenu("Settings")

        self.toggle_theme_action = self.settings_menu.addAction("Toggle Theme")
        self.toggle_theme_action.triggered.connect(self.toggle_theme)

        self.character_names_action = self.settings_menu.addAction("Set Character ID to Name")
        self.character_names_action.triggered.connect(self.character_id_to_name)

        self.window = QtWidgets.QWidget()

        self.horizontal_layout = QtWidgets.QHBoxLayout()

        self.file_tree = QtWidgets.QTreeView(self.window)
        self.file_tree.setSelectionMode(self.file_tree.SelectionMode.SingleSelection)
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self.file_tree_context_menu)
        self.file_tree.currentChanged = self.tree_changed_selection
        self.horizontal_layout.addWidget(self.file_tree, 1)

        self.ft_context_menu = QtWidgets.QMenu()

        self.empty_editor = QtWidgets.QWidget()
        self.horizontal_layout.addWidget(self.empty_editor, 3)

        self.window.setLayout(self.horizontal_layout)
        self.setCentralWidget(self.window)

        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.setBaseSize(QtCore.QSize(1280, 720))

        self.show()

    def file_tree_context_menu(self, point: QtCore.QPoint):
        pass

    def file_menu_open(self):
        pass

    def file_menu_save(self):
        pass

    def file_menu_save_as(self):
        pass

    def toggle_theme(self):
        pass

    def character_id_to_name(self):
        pass

    def tree_changed_selection(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex):
        pass
