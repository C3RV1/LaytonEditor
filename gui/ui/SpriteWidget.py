from typing import List

from PySide6 import QtCore, QtWidgets, QtGui


class SpriteWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SpriteWidgetUI, self).__init__(*args, **kwargs)

        self.context_menu = QtWidgets.QMenu()

        self.v_layout = QtWidgets.QVBoxLayout()

        self.tab_widget = QtWidgets.QTabWidget()
        self.v_layout.addWidget(self.tab_widget, 4)

        self.images_tab = QtWidgets.QWidget()
        self.tab_widget.addTab(self.images_tab, "Images")

        self.images_layout = QtWidgets.QVBoxLayout()

        self.image_list = QtWidgets.QListView()
        self.image_list.setFlow(QtWidgets.QListView.Flow.LeftToRight)
        self.image_list.setViewMode(QtWidgets.QListView.ViewMode.ListMode)
        self.image_list.setMovement(QtWidgets.QListView.Movement.Snap)
        self.image_list.setIconSize(QtCore.QSize(100, 100))
        self.image_list.setWrapping(False)
        self.image_list.setDragDropMode(QtWidgets.QListView.DragDropMode.InternalMove)
        self.image_list.setSelectionMode(QtWidgets.QListView.SelectionMode.SingleSelection)
        self.image_list.setAcceptDrops(True)
        self.image_list.setDragEnabled(True)
        self.image_list.setDropIndicatorShown(True)
        self.image_list.currentChanged = self.image_list_selection
        self.image_list.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.image_list.customContextMenuRequested.connect(self.image_list_context_menu)
        self.images_layout.addWidget(self.image_list, 1)

        self.image_view = QtWidgets.QLabel()
        self.image_view.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.images_layout.addWidget(self.image_view, 3)

        self.images_tab.setLayout(self.images_layout)

        self.animations_tab = QtWidgets.QWidget()
        self.anim_layout = QtWidgets.QHBoxLayout()

        self.anim_list = QtWidgets.QListView()
        self.anim_list.setFlow(QtWidgets.QListView.Flow.TopToBottom)
        self.anim_list.setViewMode(QtWidgets.QListView.ViewMode.ListMode)
        self.anim_list.setMovement(QtWidgets.QListView.Movement.Snap)
        self.anim_list.setWrapping(False)
        self.anim_list.setDragDropMode(QtWidgets.QListView.DragDropMode.InternalMove)
        self.anim_list.setSelectionMode(QtWidgets.QListView.SelectionMode.SingleSelection)
        self.anim_list.setAcceptDrops(True)
        self.anim_list.setDragEnabled(True)
        self.anim_list.setDropIndicatorShown(True)
        self.anim_list.currentChanged = self.anim_change_selection
        self.anim_list.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.anim_list.customContextMenuRequested.connect(self.anim_context_menu)
        self.anim_layout.addWidget(self.anim_list, 1)

        self.anim_data_tab = QtWidgets.QTabWidget()

        self.frame_list_shown = False
        self.frame_list = QtWidgets.QListView()
        self.frame_list.setFlow(QtWidgets.QListView.Flow.TopToBottom)
        self.frame_list.setViewMode(QtWidgets.QListView.ViewMode.ListMode)
        self.frame_list.setIconSize(QtCore.QSize(100, 100))
        self.frame_list.setMovement(QtWidgets.QListView.Movement.Snap)
        self.frame_list.setWrapping(False)
        self.frame_list.setDragDropMode(QtWidgets.QListView.DragDropMode.InternalMove)
        self.frame_list.setSelectionMode(QtWidgets.QListView.SelectionMode.SingleSelection)
        self.frame_list.setAcceptDrops(True)
        self.frame_list.setDragEnabled(True)
        self.frame_list.setDropIndicatorShown(True)
        self.frame_list.currentChanged = self.frame_change_selection
        self.frame_list.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.frame_list.customContextMenuRequested.connect(self.frame_context_menu)
        self.anim_data_tab.addTab(self.frame_list, "Frames")

        self.anim_properties = QtWidgets.QTableView()
        self.anim_data_tab.addTab(self.anim_properties, "Properties")

        self.anim_layout.addWidget(self.anim_data_tab, 1)

        self.animations_tab.setLayout(self.anim_layout)

        self.tab_widget.addTab(self.animations_tab, "Animations")

        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_btn.clicked.connect(self.save_btn_click)
        self.v_layout.addWidget(self.save_btn, 1)

        self.setLayout(self.v_layout)

    def image_list_selection(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection):
        pass

    def image_list_context_menu(self, point: QtCore.QPoint):
        pass

    def save_btn_click(self):
        pass

    def anim_change_selection(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection):
        pass

    def anim_context_menu(self, point: QtCore.QPoint):
        pass

    def frame_change_selection(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection):
        pass

    def frame_context_menu(self, point: QtCore.QPoint):
        pass
