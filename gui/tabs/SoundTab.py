import logging

from PySide6 import QtCore

from gui.tabs.BaseTab import BaseTab
from gui.EditorTree import MultipleCategoriesEditorTree
from gui.EditorTypes import EditorObject
from gui.editor_categories import *
from gui.editors import *
from previewers import *
from gui.PygamePreviewer import PygamePreviewer

from pg_utils.sound.SADLStreamPlayer import SADLStreamPlayer
from pg_utils.sound.SMDLStreamPlayer import SMDLStreamPlayer


class SoundTab(BaseTab):
    def __init__(self, rom, pg_previewer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rom = rom
        self.pg_previewer: PygamePreviewer = pg_previewer

        if self.rom.name == B"LAYTON2":
            categories = [
                StreamedAudioCategory(),
                SequencedAudioCategory(),
                SoundEffectCategory(),
                SoundBankCategory(),
                SoundFixCategory()
            ]
        else:
            categories = [
                StreamedAudioCategory(),
                SequencedAudioCategory(),
                SoundEffectCategory(),
                SoundBankCategory()
            ]

        self.tree_model = MultipleCategoriesEditorTree(categories)
        self.tree_model.set_rom(rom)
        self.file_tree.setModel(self.tree_model)

        self.sound_profile_editor = SoundFixEditor()
        self.sound_bank_editor = SoundBankEditor()
        self.stream_editor = StreamEditor(self)

        self.sound_profile_editor.hide()
        self.sound_bank_editor.hide()
        self.stream_editor.hide()

        self.h_layout.addWidget(self.sound_profile_editor, 3)
        self.h_layout.addWidget(self.sound_bank_editor, 3)
        self.h_layout.addWidget(self.stream_editor, 3)

        self.active_editor = self.empty_editor

    def tree_changed_selection(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex):
        node: EditorObject = current.internalPointer()
        if not node:
            return

        logging.info(f"Opening {node.name_str()}, category {node.category_str()}")

        self.active_editor.hide()
        self.active_editor = None

        set_previewer = False

        if isinstance(node, SADLNode):
            self.active_editor = self.stream_editor
            sadl = node.get_sadl()
            sadl_player = SADLStreamPlayer()
            name = node.data()
            self.stream_editor.set_sadl(sadl, name)
            self.pg_previewer.start_renderer(
                SoundPreview(sadl_player, sadl, name)
            )
            set_previewer = True
        elif isinstance(node, SoundFixCategory):
            self.active_editor = self.sound_profile_editor
            self.sound_profile_editor.set_snd_profile(node.get_sound_profile_dlz())
        elif isinstance(node, SWDLNode):
            self.active_editor = self.sound_bank_editor
            self.sound_bank_editor.set_swdl(node.get_swdl())
        elif isinstance(node, SMDLNode):
            smdl_player = SMDLStreamPlayer()
            smdl, swdl = node.get_smdl(), node.get_swdl()
            sample_bank = node.sample_bank()
            smdl_player.create_temporal_sf2(swdl, sample_bank)
            self.pg_previewer.start_renderer(SoundPreview(smdl_player, smdl,
                                                          node.data()))
            set_previewer = True

        if self.active_editor is None:
            self.active_editor = self.empty_editor

        if not set_previewer:
            self.pg_previewer.stop_renderer()

        self.active_editor.show()
