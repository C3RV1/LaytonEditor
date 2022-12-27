from gui.ui.sprite.SpriteWidget import SpriteWidgetUI
from formats.graphics.ani import AniSprite, AnimationFrame
from PySide6 import QtCore, QtGui
from . import *


class SpriteEditor(SpriteWidgetUI):
    def __init__(self, *args, **kwargs):
        super(SpriteEditor, self).__init__(*args, **kwargs)
        self.sprite: AniSprite = None
        self.variables_model = VariablesModel()
        self.images_model = ImagesModel()
        self.anims_model = AnimsModel()
        self.frames_model = FramesModel(self.anim_properties.frame_order_edit)
        self.selected_frame: AnimationFrame = None

    def get_anim_properties_widget(self):
        return AnimPropertiesWidget([self.frame_next_index_label, self.frame_next_index_input])

    def set_sprite(self, sprite: AniSprite):
        self.sprite = sprite
        self.variables_model.set_sprite(sprite)
        self.variables_table.setModel(self.variables_model)
        self.images_model.set_sprite(sprite)
        self.image_list.setModel(self.images_model)
        self.anims_model.set_sprite(sprite)
        self.anim_list.setModel(self.anims_model)

    def save_btn_click(self):
        self.sprite.save()

    def image_list_selection(self, selected: QtCore.QModelIndex):
        if not selected.isValid():
            self.image_view.clear()
            return
        index = selected.row()
        self.image_view.setPixmap(self.sprite.extract_image_qt(index))

    def image_list_context_menu(self, point: QtCore.QPoint):
        index = self.image_list.indexAt(point)
        self.context_menu.clear()

        action = QtGui.QAction("Append PNG", self.context_menu)
        action.triggered.connect(self.images_model.append_image)
        self.context_menu.addAction(action)

        if index.isValid():
            self.context_menu.addSeparator()

            action = QtGui.QAction("Remove Image", self.context_menu)
            action.triggered.connect(lambda: self.images_model.remove_image(index))
            self.context_menu.addAction(action)

            def replace_image(index_):
                self.images_model.replace_image(index_)
                self.image_list_selection(index_)

            action = QtGui.QAction("Import PNG", self.context_menu)
            action.triggered.connect(lambda: replace_image(index))
            self.context_menu.addAction(action)

            action = QtGui.QAction("Export PNG", self.context_menu)
            action.triggered.connect(lambda: self.images_model.export_image(index))
            self.context_menu.addAction(action)

        self.context_menu.exec(self.image_list.mapToGlobal(point))

    def anim_change_selection(self, selected: QtCore.QModelIndex):
        if not selected.isValid():
            self.anim_data_tab.hide()
            return
        self.anim_data_tab.show()
        self.frames_model.set_animation(self.sprite, selected.row())
        self.frame_list.setModel(self.frames_model)
        self.frame_list.clearSelection()
        self.anim_properties.set_animation(self.sprite, selected.row())

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

    def frame_change_selection(self, selected: QtCore.QModelIndex):
        if not selected.isValid():
            self.selected_frame = None
            self.frame_edit_data.hide()
            return
        animation = self.frames_model.animation
        self.selected_frame = animation.frames[selected.row()]
        self.frame_edit_data.show()
        if self.selected_frame.image_index < len(self.sprite.images):
            self.frame_preview.setPixmap(self.sprite.extract_image_qt(self.selected_frame.image_index))
        self.frame_image_index_input.setRange(0, len(self.sprite.images) - 1)
        self.frame_next_index_input.setRange(0, len(animation.frames) - 1)
        self.frame_duration_input.setRange(0, 360)
        self.frame_image_index_input.setValue(self.selected_frame.image_index)
        self.frame_next_index_input.setValue(self.selected_frame.next_frame_index)
        self.frame_duration_input.setValue(self.selected_frame.duration)

    def frame_context_menu(self, point: QtCore.QPoint):
        index = self.frame_list.indexAt(point)
        self.context_menu.clear()

        action = QtGui.QAction("Append Frame", self.context_menu)
        action.triggered.connect(self.frames_model.append_frame)
        self.context_menu.addAction(action)

        if index.isValid():
            action = QtGui.QAction("Remove Frame", self.context_menu)
            action.triggered.connect(lambda: self.frames_model.remove_frame(index))
            self.context_menu.addAction(action)

        self.context_menu.exec(self.frame_list.mapToGlobal(point))

    def frame_next_index_changed(self, value: int):
        self.selected_frame.next_frame_index = value

    def frame_image_index_changed(self, value: int):
        self.selected_frame.image_index = value
        if self.selected_frame.image_index < len(self.sprite.images):
            self.frame_preview.setPixmap(self.sprite.extract_image_qt(self.selected_frame.image_index))

    def frame_duration_changed(self, value: int):
        self.selected_frame.duration = value
