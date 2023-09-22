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

        self.character_names_action = self.settings_menu.addAction("Character ID to Name Table")
        self.character_names_action.triggered.connect(self.character_id_to_name)

        self.advanced_mode_action = self.settings_menu.addAction("Advanced Mode (Requires Restart)")
        self.advanced_mode_action.setCheckable(True)
        self.advanced_mode_action.toggled.connect(self.advanced_mode_toggled)

        self.window = QtWidgets.QTabWidget()
        self.tabs = []
        self.setCentralWidget(self.window)

        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.setBaseSize(QtCore.QSize(1280, 720))

        self.show()

    def setup_tabs(self, tabs):
        self.window.clear()
        for tab in self.tabs:
            tab: QtWidgets.QWidget
            tab.deleteLater()

        self.tabs.clear()
        for tab_name, tab in tabs:
            self.window.addTab(tab, tab_name)
            self.tabs.append(tab)

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

    def advanced_mode_toggled(self, checked: bool):
        pass
