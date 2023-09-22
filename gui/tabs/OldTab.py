from gui.tabs.BaseTab import BaseTab
from gui.editors import *
from gui.EditorTree import DefaultEditorTree
from PySide6 import QtCore, QtGui

from gui.EditorTypes import EditorObject
from gui.editor_categories import *
from previewers import *

import logging


class OldTab(BaseTab):
    def __init__(self, rom, pg_previewer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rom = rom
        self.pg_previewer = pg_previewer

        self.tree_model = DefaultEditorTree()
        self.file_tree.setModel(self.tree_model)

        self.tree_model.set_rom(rom)

        self.event_editor = EventEditor(self)
        self.puzzle_editor = PuzzleEditor(self)
        self.text_editor = TextEditor(self)
        self.script_editor = ScriptEditor(self)
        self.place_editor = PlaceEditor(self)
        self.time_definitions_editor = TimeDefinitionsEditor()

        self.event_editor.hide()
        self.puzzle_editor.hide()
        self.text_editor.hide()
        self.script_editor.hide()
        self.place_editor.hide()
        self.time_definitions_editor.hide()

        self.h_layout.addWidget(self.event_editor, 3)
        self.h_layout.addWidget(self.puzzle_editor, 3)
        self.h_layout.addWidget(self.text_editor, 3)
        self.h_layout.addWidget(self.script_editor, 3)
        self.h_layout.addWidget(self.place_editor, 3)
        self.h_layout.addWidget(self.time_definitions_editor, 3)

        self.active_editor = self.empty_editor

    def tree_changed_selection(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex):
        node: EditorObject = current.internalPointer()
        if not node:
            return

        logging.info(f"Opening {node.name_str()}, category {node.category_str()}")

        self.active_editor.hide()
        self.active_editor = None

        set_previewer = False

        if isinstance(node, EventNode):
            self.active_editor = self.event_editor
            event = node.get_event()
            self.event_editor.set_event(event, current)

            self.pg_previewer.start_renderer(EventPlayer(event))
            set_previewer = True
        elif isinstance(node, PuzzleNode):
            self.active_editor = self.puzzle_editor
            puzzle = node.get_puzzle()
            self.puzzle_editor.set_puzzle(puzzle)

            self.pg_previewer.start_renderer(get_puzzle_player(puzzle))
            set_previewer = True
        elif isinstance(node, TextAsset):
            self.active_editor = self.text_editor
            self.text_editor.set_text(node)
        elif isinstance(node, ScriptAsset):
            self.active_editor = self.script_editor
            self.script_editor.set_script(node.to_gds())
        elif isinstance(node, PlaceVersion):
            self.active_editor = self.place_editor
            place = node.get_place()
            self.place_editor.set_place(place)

            self.pg_previewer.start_renderer(PlacePreview(place))
            set_previewer = True
        elif isinstance(node, TimeDefinitionsNode):
            self.active_editor = self.time_definitions_editor
            self.time_definitions_editor.set_time_dlz(node.get_time_definitions_dlz())

        if self.active_editor is None:
            self.active_editor = self.empty_editor

        if not set_previewer:
            self.pg_previewer.stop_renderer()

        self.active_editor.show()
