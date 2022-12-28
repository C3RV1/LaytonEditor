from PySide6 import QtCore, QtWidgets, QtGui
from .PuzzlePropertiesWidget import PuzzlePropertiesWidgetUI


class PuzzleWidgetUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(PuzzleWidgetUI, self).__init__(*args, **kwargs)

        self.v_layout = QtWidgets.QVBoxLayout()

        self.tab_widget = QtWidgets.QTabWidget(self)

        self.puzzle_properties = self.get_puzzle_properties_widget()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidget(self.puzzle_properties)
        self.scroll_area.setWidgetResizable(True)
        self.tab_widget.addTab(self.scroll_area, "Properties")

        self.text_editor = QtWidgets.QPlainTextEdit(self)
        self.tab_widget.addTab(self.text_editor, "Script")

        self.v_layout.addWidget(self.tab_widget, 8)

        self.preview_dcc_btn = QtWidgets.QPushButton("Preview DCC", self)
        self.preview_dcc_btn.clicked.connect(self.preview_dcc_btn_click)

        self.save_dcc_btn = QtWidgets.QPushButton("Save DCC", self)
        self.save_dcc_btn.clicked.connect(self.save_dcc_btn_click)

        self.v_layout.addWidget(self.preview_dcc_btn, 1)
        self.v_layout.addWidget(self.save_dcc_btn, 1)

        self.setLayout(self.v_layout)

    def get_puzzle_properties_widget(self):
        return PuzzlePropertiesWidgetUI(self)

    def preview_dcc_btn_click(self):
        pass

    def save_dcc_btn_click(self):
        pass
