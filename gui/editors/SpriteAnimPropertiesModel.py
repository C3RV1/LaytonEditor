from PySide6 import QtCore, QtWidgets, QtGui
from formats.graphics.ani import AniSprite, Animation


class SpriteAnimPropertiesModel(QtCore.QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super(SpriteAnimPropertiesModel, self).__init__(*args, **kwargs)
        self.sprite: AniSprite = None
        self.animation: Animation = None

    def set_animation(self, sprite: AniSprite, anim_idx: int):
        self.layoutAboutToBeChanged.emit()
        self.sprite = sprite
        self.animation = self.sprite.animations[anim_idx]
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return 4
        return 0

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 1

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Vertical:
            return [
                "Child X",
                "Child Y",
                f"Child Animation Index",
                f"Loops"
            ][section]
        return "Value"

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        if index.row() == 0:
            return self.animation.child_image_x
        elif index.row() == 1:
            return self.animation.child_image_y
        elif index.row() == 2:
            return self.animation.child_image_animation_index
        elif index.row() == 3:
            return self.animation.loops

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(SpriteAnimPropertiesModel, self).flags(index)
        if not index.isValid():
            return default_flags
        if index.column() == 0:
            default_flags |= QtCore.Qt.ItemFlag.ItemIsEditable
        return default_flags

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        if index.row() == 0:
            self.animation.child_image_x = value
        elif index.row() == 1:
            self.animation.child_image_y = value
        elif index.row() == 2:
            self.animation.child_image_animation_index = value
        elif index.row() == 3:
            self.animation.loops = value
        else:
            return False
        return True
