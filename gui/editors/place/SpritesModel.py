from .PlaceAbstractTableModel import PlaceAbstractTableModel
from PySide6 import QtCore, QtGui, QtWidgets


class SpritesModel(PlaceAbstractTableModel):
    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return len(self.place.sprites)
        return 0

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 3

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return ["X", "Y", "Filename"][section]
        return f"Sprite {section}"

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        spr = self.place.sprites[index.row()]
        return [
            spr.x,
            spr.y,
            spr.filename
        ][index.column()]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(SpritesModel, self).flags(index)
        if not index.isValid():
            return default_flags
        return default_flags | QtCore.Qt.ItemFlag.ItemIsEditable

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        spr = self.place.sprites[index.row()]
        if index.column() == 0:
            spr.x = value
        elif index.column() == 1:
            spr.y = value
        elif index.column() == 2:
            spr.filename = value
        return True
