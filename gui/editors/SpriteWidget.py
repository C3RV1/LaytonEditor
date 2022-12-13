from typing import List

from ..ui.SpriteWidget import SpriteWidgetUI
from formats.graphics.ani import AniSprite
from PySide6 import QtCore, QtWidgets, QtGui


class ImagesModel(QtCore.QAbstractListModel):
    def __init__(self):
        super(ImagesModel, self).__init__()
        self.sprite: AniSprite = None

    def set_sprite(self, sprite: AniSprite):
        self.layoutAboutToBeChanged.emit()
        self.sprite = sprite
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.sprite.images)

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or role != QtCore.Qt.ItemDataRole.DecorationRole:
            return None
        return QtGui.QIcon(self.sprite.extract_image_qt(index.row()))

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(ImagesModel, self).flags(index)
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
        print(int(data.text()), row)
        src_row = int(data.text())
        if src_row < row:
            row -= 1
        if src_row == row:
            return False
        image = self.sprite.images[src_row]
        self.sprite.images.remove(image)
        self.sprite.images.insert(row, image)
        return True


class SpriteEditor(SpriteWidgetUI):
    def __init__(self, *args, **kwargs):
        super(SpriteEditor, self).__init__(*args, **kwargs)
        self.sprite: AniSprite = None
        self.images_model = ImagesModel()

    def set_sprite(self, sprite: AniSprite):
        self.sprite = sprite
        self.images_model.set_sprite(sprite)
        self.image_list.setModel(self.images_model)

    def image_list_selection(self, selected: QtCore.QModelIndex, deselected: QtCore.QModelIndex):
        if not selected.isValid():
            return
        index = selected.row()
        self.image_view.setPixmap(self.sprite.extract_image_qt(index))

