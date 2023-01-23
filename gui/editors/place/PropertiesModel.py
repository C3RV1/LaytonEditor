from .PlaceAbstractTableModel import PlaceAbstractTableModel
from PySide6 import QtCore, QtGui, QtWidgets


class PropertiesModel(PlaceAbstractTableModel):
    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return 6
        return 0

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 1

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return "Value"
        return [
            "Index",
            "Map X",
            "Map Y",
            "Background Image Index",
            "Map Image Index",
            "Sound Profile"
        ][section]

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        return [
            self.place.index,
            self.place.map_x,
            self.place.map_y,
            self.place.background_image_index,
            self.place.map_image_index,
            self.place.sound_profile
        ][index.row()]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(PropertiesModel, self).flags(index)
        if not index.isValid():
            return default_flags
        return default_flags | QtCore.Qt.ItemFlag.ItemIsEditable

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        if index.row() == 0:
            self.place.index = value
        elif index.row() == 1:
            self.place.map_x = value
        elif index.row() == 2:
            self.place.map_y = value
        elif index.row() == 3:
            self.place.background_image_index = value
        elif index.row() == 4:
            self.place.map_image_index = value
        elif index.row() == 5:
            self.place.sound_profile = value
        return True
