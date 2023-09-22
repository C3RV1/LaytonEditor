import logging

from PySide6 import QtCore

from gui.tabs.BaseTab import BaseTab
from gui.EditorTree import MultipleCategoriesEditorTree
from gui.EditorTypes import EditorObject
from gui.editor_categories import *
from gui.editors import *


class GraphicsTab(BaseTab):
    def __init__(self, rom, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rom = rom

        if self.rom.name == B"LAYTON2":
            categories = [
                SpriteCategory(),
                BackgroundsCategory(),
                MoviesCategory(),
                FontsCategory()
            ]
        else:
            categories = [
                SpriteCategory(),
                BackgroundsCategory(),
                FontsCategory()
            ]

        self.tree_model = MultipleCategoriesEditorTree(categories)
        self.tree_model.set_rom(rom)
        self.file_tree.setModel(self.tree_model)

        self.background_editor = BackgroundEditor(self)
        self.sprite_editor = SpriteEditor(self)
        self.movie_editor = MovieEditor()

        self.background_editor.hide()
        self.sprite_editor.hide()
        self.movie_editor.hide()

        self.h_layout.addWidget(self.background_editor, 3)
        self.h_layout.addWidget(self.sprite_editor, 3)
        self.h_layout.addWidget(self.movie_editor, 3)

        self.active_editor = self.empty_editor

    def tree_changed_selection(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex):
        node: EditorObject = current.internalPointer()
        if not node:
            return

        logging.info(f"Opening {node.name_str()}, category {node.category_str()}")

        self.active_editor.hide()
        self.active_editor = None

        set_previewer = False

        if isinstance(node, BackgroundAsset):
            self.active_editor = self.background_editor
            self.background_editor.set_image(node.get_bg())
        elif isinstance(node, SpriteAsset):
            self.active_editor = self.sprite_editor
            self.sprite_editor.set_sprite(node.get_sprite())
        elif isinstance(node, MovieAsset):
            self.active_editor = self.movie_editor
            self.movie_editor.set_movie(node)

        if self.active_editor is None:
            self.active_editor = self.empty_editor

        self.active_editor.show()


