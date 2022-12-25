from .PlaceAbstractTableModel import PlaceAbstractTableModel
from PySide6 import QtCore, QtGui, QtWidgets


class ObjectsModel(PlaceAbstractTableModel):
    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return len(self.place.objects)
        return 0

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 7

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return ["X", "Y", "Width", "Height", "Character Index", "Event Index", "Unk"][section]
        return f"Object {section}"

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        obj = self.place.objects[index.row()]
        return [
            obj.x,
            obj.y,
            obj.width,
            obj.height,
            obj.character_index,
            obj.event_index,
            obj.unk
        ][index.column()]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(ObjectsModel, self).flags(index)
        if not index.isValid():
            return default_flags
        return default_flags | QtCore.Qt.ItemFlag.ItemIsEditable

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        obj = self.place.objects[index.row()]
        if index.column() == 0:
            obj.x = value
        elif index.column() == 1:
            obj.y = value
        elif index.column() == 2:
            obj.width = value
        elif index.column() == 3:
            obj.height = value
        elif index.column() == 4:
            obj.character_index = value
        elif index.column() == 5:
            obj.event_index = value
        elif index.column() == 6:
            obj.unk = value
        return True
