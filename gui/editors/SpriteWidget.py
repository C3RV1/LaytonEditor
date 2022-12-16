from ..ui.SpriteWidget import SpriteWidgetUI
from formats.graphics.ani import AniSprite
from PySide6 import QtCore, QtWidgets, QtGui
from .SpriteImagesModel import ImagesModel
from .SpriteAnimsModel import AnimsModel
from .SpriteFramesModel import FramesModel
from .SpriteAnimPropertiesModel import SpriteAnimPropertiesModel


class SpriteEditor(SpriteWidgetUI):
    def __init__(self, *args, **kwargs):
        super(SpriteEditor, self).__init__(*args, **kwargs)
        self.sprite: AniSprite = None
        self.images_model = ImagesModel()
        self.anims_model = AnimsModel()
        self.frames_model = FramesModel()
        self.anim_properties_model = SpriteAnimPropertiesModel()

    def set_sprite(self, sprite: AniSprite):
        self.sprite = sprite
        self.images_model.set_sprite(sprite)
        self.image_list.setModel(self.images_model)
        self.anims_model.set_sprite(sprite)
        self.anim_list.setModel(self.anims_model)

    def save_btn_click(self):
        self.sprite.save()

    def image_list_selection(self, selected: QtCore.QModelIndex, deselected: QtCore.QModelIndex):
        if not selected.isValid():
            return
        index = selected.row()
        self.image_view.setPixmap(self.sprite.extract_image_qt(index))

    def image_list_context_menu(self, point: QtCore.QPoint):
        index = self.image_list.indexAt(point)
        self.context_menu.clear()

        action = QtGui.QAction("Append Image", self.context_menu)
        action.triggered.connect(self.images_model.append_image)
        self.context_menu.addAction(action)

        if index.isValid():
            def replace_image(index_):
                self.images_model.replace_image(index_)
                self.image_list_selection(index_, None)

            action = QtGui.QAction("Replace Image", self.context_menu)
            action.triggered.connect(lambda: replace_image(index))
            self.context_menu.addAction(action)

            action = QtGui.QAction("Export Image", self.context_menu)
            action.triggered.connect(lambda: self.images_model.export_image(index))
            self.context_menu.addAction(action)

            action = QtGui.QAction("Remove Image", self.context_menu)
            action.triggered.connect(lambda: self.images_model.remove_image(index))
            self.context_menu.addAction(action)

        self.context_menu.exec(self.image_list.mapToGlobal(point))

    def anim_change_selection(self, selected: QtCore.QModelIndex, deselected: QtCore.QModelIndex):
        if not selected.isValid():
            self.anim_data_tab.hide()
            return
        self.anim_data_tab.show()
        self.frames_model.set_animation(self.sprite, selected.row())
        self.frame_list.setModel(self.frames_model)
        self.anim_properties_model.set_animation(self.sprite, selected.row())
        self.anim_properties.setModel(self.anim_properties_model)

    def anim_context_menu(self, point: QtCore.QPoint):
        index = self.anim_list.indexAt(point)
        self.context_menu.clear()

        action = QtGui.QAction("Append Animation", self.context_menu)
        action.triggered.connect(self.anims_model.append_animation)
        self.context_menu.addAction(action)

        if index.isValid():
            action = QtGui.QAction("Remove Animation", self.context_menu)
            action.triggered.connect(lambda: self.anims_model.remove_animation(index))
            self.context_menu.addAction(action)

        self.context_menu.exec(self.image_list.mapToGlobal(point))
