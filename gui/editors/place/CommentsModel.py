from .PlaceAbstractTableModel import PlaceAbstractTableModel
from PySide6 import QtCore, QtGui, QtWidgets


class CommentsModel(PlaceAbstractTableModel):
    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return len(self.place.comments)
        return 0

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 6

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return ["X", "Y", "Width", "Height", "Character Index", "Text Index"][section]
        return f"Comment {section}"

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        comment = self.place.comments[index.row()]
        return [
            comment.x,
            comment.y,
            comment.width,
            comment.height,
            comment.character_index,
            comment.text_index,
        ][index.column()]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(CommentsModel, self).flags(index)
        if not index.isValid():
            return default_flags
        return default_flags | QtCore.Qt.ItemFlag.ItemIsEditable

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        comment = self.place.comments[index.row()]
        if index.column() == 0:
            comment.x = value
        elif index.column() == 1:
            comment.y = value
        elif index.column() == 2:
            comment.width = value
        elif index.column() == 3:
            comment.height = value
        elif index.column() == 4:
            comment.character_index = value
        elif index.column() == 5:
            comment.text_index = value
        return True
