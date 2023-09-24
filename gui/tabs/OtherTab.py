from gui.tabs.BaseTab import BaseTab
from gui.editors import *
from gui.EditorTree import MultipleCategoriesEditorTree
from PySide6 import QtCore, QtGui

from gui.EditorTypes import EditorObject
from gui.editor_categories import *

import logging


class OtherTab(BaseTab):
    def __init__(self, rom, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rom = rom

        self.tree_model = MultipleCategoriesEditorTree(
            [
                TextsCategory(),
                ScriptsCategory(),
                TimeDefinitionsNode()
            ]
        )
        self.file_tree.setModel(self.tree_model)

        self.tree_model.set_rom(rom)
        self.text_editor = TextEditor(self)
        self.script_editor = ScriptEditor(self)
        self.time_definitions_editor = TimeDefinitionsEditor()

        self.text_editor.hide()
        self.script_editor.hide()
        self.time_definitions_editor.hide()

        self.h_layout.addWidget(self.text_editor, 3)
        self.h_layout.addWidget(self.script_editor, 3)
        self.h_layout.addWidget(self.time_definitions_editor, 3)

        self.active_editor = self.empty_editor

    def tree_changed_selection(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex):
        node: EditorObject = current.internalPointer()
        if not node:
            return

        logging.info(f"Opening {node.name_str()}, category {node.category_str()}")

        self.active_editor.hide()
        self.active_editor = None

        if isinstance(node, TextAsset):
            self.active_editor = self.text_editor
            self.text_editor.set_text(node)
        elif isinstance(node, ScriptAsset):
            self.active_editor = self.script_editor
            self.script_editor.set_script(node.to_gds())
        elif isinstance(node, TimeDefinitionsNode):
            self.active_editor = self.time_definitions_editor
            self.time_definitions_editor.set_time_dlz(node.get_time_definitions_dlz())

        if self.active_editor is None:
            self.active_editor = self.empty_editor

        self.active_editor.show()
