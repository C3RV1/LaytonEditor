from .PlaceAbstractTableModel import PlaceAbstractTableModel
from PySide6 import QtCore, QtGui, QtWidgets


class HintcoinModel(PlaceAbstractTableModel):
    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return len(self.place.hintcoins)
        return 0

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 4

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return ["X", "Y", "Width", "Height"][section]
        return f"Hintcoin {section}"

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        hintcoin = self.place.hintcoins[index.row()]
        return [
            hintcoin.x,
            hintcoin.y,
            hintcoin.width,
            hintcoin.height
        ][index.column()]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(HintcoinModel, self).flags(index)
        if not index.isValid():
            return default_flags
        return default_flags | QtCore.Qt.ItemFlag.ItemIsEditable

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        hintcoin = self.place.hintcoins[index.row()]
        if index.column() == 0:
            hintcoin.x = value
        elif index.column() == 1:
            hintcoin.y = value
        elif index.column() == 2:
            hintcoin.width = value
        elif index.column() == 3:
            hintcoin.height = value
        return True
