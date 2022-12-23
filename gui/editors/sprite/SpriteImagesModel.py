from PySide6 import QtCore, QtWidgets, QtGui
from formats.graphics.ani import AniSprite
from typing import List
from PIL import Image
from gui.SettingsManager import SettingsManager


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
        if row == -1:
            return False
        src_row = int(data.text())
        if src_row < row:
            row -= 1
        if src_row == row:
            return False
        image = self.sprite.images[src_row]
        self.sprite.images.pop(src_row)
        self.sprite.images.insert(row, image)
        max_row = max(src_row, row)
        min_row = min(src_row, row)
        for animation in self.sprite.animations:
            for frame in animation.frames:
                if frame.image_index == src_row:
                    frame.image_index = row
                elif src_row < row:
                    # moved element forward
                    if src_row < frame.image_index <= row:
                        frame.image_index -= 1
                elif src_row > row:
                    if row <= frame.image_index <= src_row:
                        frame.image_index += 1
        return True

    def append_image(self):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.sprite.images),
                             len(self.sprite.images))
        import_path, _ = SettingsManager().import_file(None, "Import PNG...", "PNG Files (*.png)")
        if import_path == "":
            return

        image: Image.Image = Image.open(import_path)
        self.sprite.append_image_pil(image)
        self.endInsertRows()

    def replace_image(self, index: QtCore.QModelIndex):
        import_path, _ = SettingsManager().import_file(None, "Import PNG...", "PNG Files (*.png)")
        if import_path == "":
            return

        image: Image.Image = Image.open(import_path)
        self.sprite.replace_image_pil(index.row(), image)
        self.dataChanged.emit(index, index, index.parent())

    def export_image(self, index: QtCore.QModelIndex):
        filename = f"{index.row()}.png"
        export_path = SettingsManager().export_file(None, "Export PNG...", filename, "PNG Files (*.png)")
        if export_path == "":
            return

        image: Image.Image = self.sprite.extract_image_pil(index.row())
        image.save(export_path)

    def remove_image(self, index: QtCore.QModelIndex):
        self.beginRemoveRows(QtCore.QModelIndex(), index.row(),
                             index.row())
        self.sprite.remove_image(index.row())
        self.endRemoveRows()
