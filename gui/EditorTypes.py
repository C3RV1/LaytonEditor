from PySide6 import QtCore
from formats.filesystem import NintendoDSRom


class EditorObject:
    category: 'EditorCategory'


class EditorCategory(EditorObject):
    def __init__(self):
        self.name = ""
        self.category = self
        self.rom: NintendoDSRom = None

    def set_rom(self, rom):
        self.rom = rom

    def row_count(self, index: QtCore.QModelIndex, model: QtCore.QAbstractItemModel):
        return 0

    def column_count(self, index: QtCore.QModelIndex, model: QtCore.QAbstractItemModel):
        return 1

    def index(self, row: int, column: int, parent: QtCore.QModelIndex,
              model: QtCore.QAbstractItemModel):
        return QtCore.QModelIndex()

    def parent(self, index: QtCore.QModelIndex, category_index: QtCore.QAbstractItemModel,
               model: QtCore.QAbstractItemModel):
        return QtCore.QModelIndex()

    def data(self, index: QtCore.QModelIndex, role, model: QtCore.QAbstractItemModel):
        return QtCore.QModelIndex()