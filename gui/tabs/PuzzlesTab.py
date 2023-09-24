import logging

from PySide6 import QtCore

from gui.EditorTypes import EditorObject
from gui.tabs.BaseTab import BaseTab
from gui.EditorTree import OneCategoryEditorTree
from gui.editor_categories import *
from gui.editors import *

from formats.filesystem import NintendoDSRom
from previewers import EventPlayer, get_puzzle_player


class PuzzlesTab(BaseTab):
    def __init__(self, rom, pg_previewer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rom: NintendoDSRom = rom
        self.pg_previewer = pg_previewer

        self.tree_model = OneCategoryEditorTree(
            PuzzleCategory()
        )
        self.tree_model.set_rom(self.rom)
        self.file_tree.setModel(self.tree_model)

        self.puzzle_editor = PuzzleEditor(self)
        self.puzzle_editor.hide()
        self.h_layout.addWidget(self.puzzle_editor, 3)

        self.active_editor = self.empty_editor

    def tree_changed_selection(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex):
        node: EditorObject = current.internalPointer()
        if not node:
            return

        logging.info(f"Opening {node.name_str()}, category {node.category_str()}")

        self.active_editor.hide()
        self.active_editor = None

        set_previewer = False

        if isinstance(node, PuzzleNode):
            self.active_editor = self.puzzle_editor
            puzzle = node.get_puzzle()
            self.puzzle_editor.set_puzzle(puzzle)

            self.pg_previewer.start_renderer(get_puzzle_player(puzzle))
            set_previewer = True

        if self.active_editor is None:
            self.active_editor = self.empty_editor

        if not set_previewer:
            self.pg_previewer.stop_renderer()

        self.active_editor.show()

