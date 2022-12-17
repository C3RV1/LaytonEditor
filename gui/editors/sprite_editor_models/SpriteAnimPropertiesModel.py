from PySide6 import QtCore, QtWidgets, QtGui
from formats.graphics.ani import AniSprite, Animation


class AnimPropertiesModel(QtCore.QAbstractTableModel):
    def __init__(self, frame_next_input_widgets, *args, **kwargs):
        super(AnimPropertiesModel, self).__init__(*args, **kwargs)
        self.frame_next_input_widgets = frame_next_input_widgets
        self.sprite: AniSprite = None
        self.animation: Animation = None
        self.frame_order_mode = "Looping"

    def show_next_frame_widgets(self):
        for widget in self.frame_next_input_widgets:
            widget: QtWidgets.QWidget
            widget.show()

    def hide_next_frame_widgets(self):
        for widget in self.frame_next_input_widgets:
            widget: QtWidgets.QWidget
            widget.hide()

    def update_frame_next(self):
        if self.frame_order_mode == "Custom":
            self.show_next_frame_widgets()
            return
        self.hide_next_frame_widgets()
        frame_count = len(self.animation.frames)
        for i, frame in enumerate(self.animation.frames):
            if self.frame_order_mode == "Looping":
                frame.next_frame_index = (i + 1) % frame_count
            else:
                frame.next_frame_index = min(i + 1, frame_count - 1)

    def set_animation(self, sprite: AniSprite, anim_idx: int):
        self.layoutAboutToBeChanged.emit()
        self.sprite = sprite
        self.animation = self.sprite.animations[anim_idx]
        next_frame_indexes = [frame.next_frame_index for frame in self.animation.frames]
        frame_count = len(self.animation.frames)
        if next_frame_indexes == [(i + 1) % frame_count for i in range(frame_count)]:
            self.frame_order_mode = "Looping"
        elif next_frame_indexes == [min(i + 1, frame_count - 1) for i in range(frame_count)]:
            self.frame_order_mode = "No looping"
        else:
            self.frame_order_mode = "Custom"
        self.update_frame_next()
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
                f"Frame Order"
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
            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                return self.frame_order_mode
            else:
                return ["Looping", "No looping", "Custom"]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(AnimPropertiesModel, self).flags(index)
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
        else:
            self.frame_order_mode = value
            self.update_frame_next()
        return True
