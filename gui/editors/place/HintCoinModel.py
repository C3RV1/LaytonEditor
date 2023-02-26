from .PlaceAbstractTableModel import PlaceAbstractTableModel
from PySide6 import QtCore, QtGui, QtWidgets


class HintCoinModel(PlaceAbstractTableModel):
    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return len(self.place.hint_coins)
        return 0

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 4

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Orientation.Horizontal:
            return ["X", "Y", "Width", "Height"][section]
        return f"Hint Coin {section}"

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        hint_coin = self.place.hint_coins[index.row()]
        return [
            hint_coin.x,
            hint_coin.y,
            hint_coin.width,
            hint_coin.height
        ][index.column()]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(HintCoinModel, self).flags(index)
        if not index.isValid():
            return default_flags
        return default_flags | QtCore.Qt.ItemFlag.ItemIsEditable

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        hint_coin = self.place.hint_coins[index.row()]
        if index.column() == 0:
            hint_coin.x = value
        elif index.column() == 1:
            hint_coin.y = value
        elif index.column() == 2:
            hint_coin.width = value
        elif index.column() == 3:
            hint_coin.height = value
        return True
