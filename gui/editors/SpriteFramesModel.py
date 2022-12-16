from PySide6 import QtCore, QtWidgets, QtGui
from formats.graphics.ani import AniSprite, Animation
from typing import List


class FramesModel(QtCore.QAbstractListModel):
    def __init__(self):
        super(FramesModel, self).__init__()
        self.sprite: AniSprite = None
        self.animation: Animation = None

    def set_animation(self, sprite: AniSprite, anim_index: int):
        self.layoutAboutToBeChanged.emit()
        self.sprite = sprite
        self.animation = self.sprite.animations[anim_index]
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.animation.frames)

    def data(self, index: QtCore.QModelIndex, role: int):
        if not index.isValid():
            return None
        frame_idx = index.row()
        if role == QtCore.Qt.ItemDataRole.DisplayRole or role == QtCore.Qt.ItemDataRole.EditRole:
            return self.animation.frames[frame_idx].image_index
        if role == QtCore.Qt.ItemDataRole.DecorationRole:
            frame = self.animation.frames[frame_idx]
            return QtGui.QIcon(self.sprite.extract_image_qt(frame.image_index))
        return None

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(FramesModel, self).flags(index)
        if not index.isValid():
            return default_flags | QtCore.Qt.ItemFlag.ItemIsDropEnabled
        return default_flags | QtCore.Qt.ItemFlag.ItemIsDragEnabled | QtCore.Qt.ItemFlag.ItemIsEditable

    def supportedDropActions(self) -> QtCore.Qt.DropAction:
        return QtCore.Qt.DropAction.MoveAction

    def mimeData(self, indexes: List[QtCore.QModelIndex]) -> QtCore.QMimeData:
        mime_data = super().mimeData(indexes)
        if not indexes:
            return mime_data
        index = indexes[0].row()
        mime_data.setText(str(index))
        return mime_data

    def dropMimeData(self, data: QtCore.QMimeData, action: QtCore.Qt.DropAction, row: int, column: int,
                     parent: QtCore.QModelIndex) -> bool:
        if row == -1:
            return False
        src_row = int(data.text())
        if src_row < row:
            row -= 1
        if src_row == row:
            return False
        frame = self.animation.frames[src_row]
        self.animation.frames.pop(src_row)
        self.animation.frames.insert(row, frame)
        return True

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid() or not isinstance(value, int):
            return False
        if value >= len(self.sprite.images):
            return False
        self.animation.frames[index.row()].image_index = value
        return True
