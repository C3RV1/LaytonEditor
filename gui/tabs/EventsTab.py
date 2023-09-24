import logging

from PySide6 import QtCore

from gui.EditorTypes import EditorObject
from gui.tabs.BaseTab import BaseTab
from gui.EditorTree import OneCategoryEditorTree
from gui.editor_categories import *
from gui.editors import *

from formats.filesystem import NintendoDSRom
from previewers import EventPlayer


class EventsTab(BaseTab):
    def __init__(self, rom, pg_previewer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rom: NintendoDSRom = rom
        self.pg_previewer = pg_previewer

        self.tree_model = OneCategoryEditorTree(
            EventCategory()
        )
        self.tree_model.set_rom(self.rom)
        self.file_tree.setModel(self.tree_model)

        self.event_editor = EventEditor(self)
        self.event_editor.hide()
        self.h_layout.addWidget(self.event_editor, 3)

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

        if self.active_editor is None:
            self.active_editor = self.empty_editor

        if not set_previewer:
            self.pg_previewer.stop_renderer()

        self.active_editor.show()

