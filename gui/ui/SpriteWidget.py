from typing import List

from PySide6 import QtCore, QtWidgets, QtGui


class SpriteWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SpriteWidgetUI, self).__init__(*args, **kwargs)

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
        self.image_list.setDragDropMode(self.image_list.DragDropMode.InternalMove)
        self.image_list.setSelectionMode(self.image_list.SelectionMode.SingleSelection)
        self.image_list.setAcceptDrops(True)
        self.image_list.setDragEnabled(True)
        self.image_list.setDropIndicatorShown(True)
        self.image_list.currentChanged = self.image_list_selection
        self.images_layout.addWidget(self.image_list, 1)

        self.image_view = QtWidgets.QLabel()
        self.image_view.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.images_layout.addWidget(self.image_view, 3)

        self.images_tab.setLayout(self.images_layout)

        self.animations_tab = QtWidgets.QWidget()
        self.tab_widget.addTab(self.animations_tab, "Animations")

        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_btn.clicked.connect(self.save_btn_click)
        self.v_layout.addWidget(self.save_btn, 1)

        self.setLayout(self.v_layout)

    def image_list_selection(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection):
        pass

    def save_btn_click(self):
        pass
