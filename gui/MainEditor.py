import os.path

from gui.ui.MainEditor import MainEditorUI
from PySide6 import QtCore, QtWidgets

from .EditorTree import EditorTree
from .EditorTypes import EditorObject

from .EventWidget import EventWidget
from .editor_categories.Events import EventNode
from previewers.event.EventPlayer import EventPlayer

from .PuzzleWidget import PuzzleWidget
from .editor_categories.Puzzles import PuzzleNode
from previewers.puzzle.PuzzlePlayer import PuzzlePlayer

from .TextWidget import TextWidget
from .editor_categories.Texts import TextAsset

from .ScriptWidget import ScriptWidget
from .editor_categories.Scripts import ScriptAsset

from previewers.sound.SoundPreview import SoundPreview
from pg_utils.sound.SADLStreamPlayer import SADLStreamPlayer
from .editor_categories.StreamedAudio import SADLNode

from previewers.place.PlacePreview import PlacePreview
from .editor_categories.Places import PlaceVersion

from .BackgroundWidget import BackgroundWidget
from .editor_categories.Backgrounds import BackgroundAsset

from pg_utils.rom.RomSingleton import RomSingleton
from .PygamePreviewer import PygamePreviewer

from formats.filesystem import NintendoDSRom
from formats import conf

import logging


class MainEditor(MainEditorUI):
    def __init__(self, *args, **kwargs):
        super(MainEditor, self).__init__(*args, **kwargs)

        self.rom: NintendoDSRom | None = None
        self.last_path = None

        self.tree_model = EditorTree()
        self.file_tree.setModel(self.tree_model)

        self.pg_previewer = PygamePreviewer()
        self.pg_previewer.start()

    def file_menu_open(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open ROM", filter="NDS Rom (*.nds)")
        if file_path == "":
            return

        rom = NintendoDSRom.fromFile(file_path)

        # Load language from arm9
        if rom.name == b"LAYTON2":
            arm9 = rom.loadArm9()
            lang_address = 0x02000d3c - arm9.ramAddress
            lang_id = rom.arm9[lang_address]
            lang_table = ["jp", "en", "sp", "fr", "it", "ge", "du", "ko", "ch"]
            try:
                conf.LANG = lang_table[lang_id]
            except IndexError:  # US version?
                # TODO: Figure out how to read it properly
                logging.warning(f"Game language not recognized: assuming US")
                conf.LANG = "en"
            logging.info(f"Game language: {conf.LANG}")
            if conf.LANG == "jp":
                return
        else:
            logging.warning("Not LAYTON2 game.")
            conf.LANG = "en"

        self.rom = rom
        RomSingleton(rom=self.rom)
        self.last_path = file_path
        self.file_save_action.setEnabled(True)
        self.file_save_as_action.setEnabled(True)
        self.tree_model.set_rom(self.rom)

    def file_menu_save(self):
        if self.last_path:
            self.rom.save()

    def file_menu_save_as(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save ROM", filter="NDS Rom (*.nds)")
        if file_path == "":
            return
        self.last_path = file_path
        self.rom.saveToFile(file_path)

    def tree_changed_selection(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex):
        node: EditorObject = current.internalPointer()
        if not node:
            return
        self.active_editor.hide()
        self.horizontal_layout.removeWidget(self.active_editor)
        self.active_editor.deleteLater()
        self.active_editor = None

        set_previewer = False

        if isinstance(node, EventNode):
            self.active_editor = EventWidget(self)
            event = node.get_event()
            self.active_editor.set_event(event)

            self.pg_previewer.start_renderer(EventPlayer(event))
            set_previewer = True
        elif isinstance(node, PuzzleNode):
            self.active_editor = PuzzleWidget(self)
            puzzle = node.get_puzzle()
            self.active_editor.set_puzzle(puzzle)

            self.pg_previewer.start_renderer(PuzzlePlayer(puzzle))
            set_previewer = True
        elif isinstance(node, TextAsset):
            self.active_editor = TextWidget(self)
            self.active_editor.set_text(node)
        elif isinstance(node, ScriptAsset):
            self.active_editor = ScriptWidget(self)
            self.active_editor.set_script(node.to_gds())
        elif isinstance(node, SADLNode):
            sadl_player = SADLStreamPlayer()
            self.pg_previewer.start_renderer(SoundPreview(sadl_player, node.get_sadl(),
                                                          node.data()))
            set_previewer = True
        elif isinstance(node, PlaceVersion):
            self.pg_previewer.start_renderer(PlacePreview(node.get_place()))
            set_previewer = True
        elif isinstance(node, BackgroundAsset):
            self.active_editor = BackgroundWidget(self)
            self.active_editor.set_image(node.get_bg())

        if self.active_editor is None:
            self.active_editor = QtWidgets.QWidget()

        if not set_previewer:
            self.pg_previewer.stop_renderer()

        self.horizontal_layout.addWidget(self.active_editor, 3)
        self.active_editor.show()

    def closeEvent(self, event) -> None:
        self.pg_previewer.loop_lock.acquire()
        self.pg_previewer.gm.exit()
        self.pg_previewer.loop_lock.release()
