from ..ui.SpriteWidget import SpriteWidgetUI
from formats.graphics.ani import AniSprite
from PySide6 import QtCore, QtWidgets, QtGui
from .SpriteImagesModel import ImagesModel


class SpriteEditor(SpriteWidgetUI):
    def __init__(self, *args, **kwargs):
        super(SpriteEditor, self).__init__(*args, **kwargs)
        self.sprite: AniSprite = None
        self.images_model = ImagesModel()

    def set_sprite(self, sprite: AniSprite):
        self.sprite = sprite
        self.images_model.set_sprite(sprite)
        self.image_list.setModel(self.images_model)

    def save_btn_click(self):
        self.sprite.save()

    def image_list_selection(self, selected: QtCore.QModelIndex, deselected: QtCore.QModelIndex):
        if not selected.isValid():
            return
        index = selected.row()
        self.image_view.setPixmap(self.sprite.extract_image_qt(index))

    def image_list_context_menu(self, point: QtCore.QPoint):
        index = self.image_list.indexAt(point)
        self.il_context_menu.clear()

        action = QtGui.QAction("Append Image", self.il_context_menu)
        action.triggered.connect(self.images_model.append_image)
        self.il_context_menu.addAction(action)

        if index.isValid():
            action = QtGui.QAction("Replace Image", self.il_context_menu)
            action.triggered.connect(lambda x: self.images_model.replace_image(index))
            self.il_context_menu.addAction(action)

            action = QtGui.QAction("Export Image", self.il_context_menu)
            action.triggered.connect(lambda x: self.images_model.export_image(index))
            self.il_context_menu.addAction(action)

            action = QtGui.QAction("Remove Image", self.il_context_menu)
            action.triggered.connect(lambda x: self.images_model.remove_image(index))
            self.il_context_menu.addAction(action)

        self.il_context_menu.exec(self.image_list.mapToGlobal(point))
