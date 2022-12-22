from PySide6 import QtCore, QtWidgets, QtGui
from formats.graphics.ani import AniSprite, Animation, AnimationFrame
from typing import List, Callable


class FramesModel(QtCore.QAbstractListModel):
    def __init__(self, update_frame_next: Callable):
        super(FramesModel, self).__init__()
        self.sprite: AniSprite = None
        self.animation: Animation = None
        self.update_frame_next = update_frame_next

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
        if frame_idx >= len(self.animation.frames):
            return None
        if role == QtCore.Qt.ItemDataRole.DisplayRole or role == QtCore.Qt.ItemDataRole.EditRole:
            return frame_idx
        if role == QtCore.Qt.ItemDataRole.DecorationRole:
            frame = self.animation.frames[frame_idx]
            return QtGui.QIcon(self.sprite.extract_image_qt(frame.image_index))
        return None

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(FramesModel, self).flags(index)
        if not index.isValid():
            return default_flags | QtCore.Qt.ItemFlag.ItemIsDropEnabled
        return default_flags | QtCore.Qt.ItemFlag.ItemIsDragEnabled

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
        self.update_frame_next()
        return True

    def append_frame(self):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.animation.frames),
                             len(self.animation.frames))
        self.animation.frames.append(AnimationFrame(next_frame_index=0, image_index=0, duration=0))
        self.update_frame_next()
        self.endInsertRows()

    def remove_frame(self, index: QtCore.QModelIndex):
        self.beginRemoveRows(QtCore.QModelIndex(), index.row(), index.row())
        self.animation.frames.pop(index.row())
        self.update_frame_next()
        self.endInsertRows()
