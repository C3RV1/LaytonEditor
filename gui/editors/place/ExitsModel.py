from .PlaceAbstractTableModel import PlaceAbstractTableModel
from PySide6 import QtCore, QtGui, QtWidgets


class ExitsModel(PlaceAbstractTableModel):
    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return len(self.place.exits)
        return 0

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 11

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return ["X", "Y", "Width", "Height", "Image Index", "Unk0",
                    "Unk1", "Unk2", "Next Map X", "Next Map Y", "Event or Place Index"][section]
        return f"Exit {section}"

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        exit_ = self.place.exits[index.row()]
        return [
            exit_.x,
            exit_.y,
            exit_.width,
            exit_.height,
            exit_.image_index,
            exit_.unk0,
            exit_.unk1,
            exit_.unk2,
            exit_.next_map_x,
            exit_.next_map_y,
            exit_.event_or_place_index,
        ][index.column()]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(ExitsModel, self).flags(index)
        if not index.isValid():
            return default_flags
        return default_flags | QtCore.Qt.ItemFlag.ItemIsEditable

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        exit_ = self.place.exits[index.row()]
        if index.column() == 0:
            exit_.x = value
        elif index.column() == 1:
            exit_.y = value
        elif index.column() == 2:
            exit_.width = value
        elif index.column() == 3:
            exit_.height = value
        elif index.column() == 4:
            exit_.image_index = value
        elif index.column() == 5:
            exit_.unk0 = value
        elif index.column() == 6:
            exit_.unk1 = value
        elif index.column() == 7:
            exit_.unk2 = value
        elif index.column() == 8:
            exit_.next_map_x = value
        elif index.column() == 9:
            exit_.next_map_y = value
        elif index.column() == 10:
            exit_.event_or_place_index = value
        return True
