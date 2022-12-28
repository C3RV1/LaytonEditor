from PySide6 import QtCore, QtWidgets, QtGui


class PlaceWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(PlaceWidgetUI, self).__init__(*args, **kwargs)
        self.v_layout = QtWidgets.QVBoxLayout()

        self.tab_widget = QtWidgets.QTabWidget(self)

        self.place_properties_tab = QtWidgets.QTableView()
        self.tab_widget.addTab(self.place_properties_tab, "Properties")

        self.hintcoins_tab = QtWidgets.QTableView()
        self.tab_widget.addTab(self.hintcoins_tab, "Hintcoins")

        self.sprites_tab = QtWidgets.QTableView()
        self.tab_widget.addTab(self.sprites_tab, "Sprites")

        self.objects_tab = QtWidgets.QTableView()
        self.tab_widget.addTab(self.objects_tab, "Objects")

        self.comments_tab = QtWidgets.QTableView()
        self.tab_widget.addTab(self.comments_tab, "Comments")

        self.exits_tab = QtWidgets.QTableView()
        self.tab_widget.addTab(self.exits_tab, "Exits")

        self.v_layout.addWidget(self.tab_widget, 4)

        self.preview_btn = QtWidgets.QPushButton("Preview")
        self.preview_btn.clicked.connect(self.preview_click)
        self.v_layout.addWidget(self.preview_btn, 1)

        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_btn.clicked.connect(self.save_click)
        self.v_layout.addWidget(self.save_btn, 1)

        self.setLayout(self.v_layout)

    def preview_click(self):
        pass

    def save_click(self):
        pass
