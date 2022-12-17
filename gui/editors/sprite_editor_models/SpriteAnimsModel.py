from PySide6 import QtCore, QtWidgets, QtGui
from formats.graphics.ani import AniSprite, Animation
from typing import List


class AnimsModel(QtCore.QAbstractListModel):
    def __init__(self):
        super(AnimsModel, self).__init__()
        self.sprite: AniSprite = None

    def set_sprite(self, sprite: AniSprite):
        self.layoutAboutToBeChanged.emit()
        self.sprite = sprite
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.sprite.animations)

    def data(self, index: QtCore.QModelIndex, role: int):
        if not index.isValid():
            return None
        if role != QtCore.Qt.ItemDataRole.DisplayRole and role != QtCore.Qt.ItemDataRole.EditRole:
            return None
        return self.sprite.animations[index.row()].name

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(AnimsModel, self).flags(index)
        if not index.isValid():
            return default_flags | QtCore.Qt.ItemFlag.ItemIsDropEnabled
        return default_flags | QtCore.Qt.ItemFlag.ItemIsDragEnabled | QtCore.Qt.ItemFlag.ItemIsEditable

    def supportedDropActions(self) -> QtCore.Qt.DropAction:
        return QtCore.Qt.DropAction.MoveAction

    def mimeData(self, indexes: List[QtCore.QModelIndex]) -> QtCore.QMimeData:
        mimeData = super().mimeData(indexes)
        if not indexes:
            return mimeData
        index = indexes[0].row()
        mimeData.setText(str(index))
        return mimeData

    def dropMimeData(self, data: QtCore.QMimeData, action: QtCore.Qt.DropAction, row: int, column: int,
                     parent: QtCore.QModelIndex) -> bool:
        if row == -1:
            return False
        src_row = int(data.text())
        if src_row < row:
            row -= 1
        if src_row == row:
            return False
        anim = self.sprite.animations[src_row]
        self.sprite.animations.pop(src_row)
        self.sprite.animations.insert(row, anim)
        return True

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        anim = self.sprite.animations[index.row()]
        anim.name = value
        return True

    def append_animation(self):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.sprite.animations),
                             len(self.sprite.animations))
        self.sprite.animations.append(Animation())
        self.endInsertRows()

    def remove_animation(self, index: QtCore.QModelIndex):
        self.beginRemoveRows(QtCore.QModelIndex(), index.row(),
                             index.row())
        self.sprite.animations.pop(index.row())
        self.endRemoveRows()
