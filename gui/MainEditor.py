from PySide6 import QtCore, QtWidgets, QtGui
from .ui.MainEditor import MainEditorUI

from .EditorTree import EditorTree
from .EditorTypes import EditorObject
from .editors import *
from .editor_categories import *
from previewers import *

from pg_utils.sound.SADLStreamPlayer import SADLStreamPlayer
from pg_utils.sound.SMDLStreamPlayer import SMDLStreamPlayer
from pg_utils.rom.RomSingleton import RomSingleton
from .PygamePreviewer import PygamePreviewer

from formats.filesystem import NintendoDSRom

import logging
from typing import Union
import qdarktheme
from .SettingsManager import SettingsManager
from .editors.CharacterNamesWidget import CharacterNamesEditor


class MainEditor(MainEditorUI):
    def __init__(self, *args, **kwargs):
        self.current_theme = SettingsManager().theme
        qdarktheme.setup_theme(SettingsManager().theme)

        super(MainEditor, self).__init__(*args, **kwargs)

        self.advanced_mode_action.setChecked(SettingsManager().advanced_mode)

        self.rom: Union[NintendoDSRom, None] = None
        self.last_path = None

        self.tree_model = EditorTree()
        self.file_tree.setModel(self.tree_model)

        self.pg_previewer = PygamePreviewer()
        self.pg_previewer.start()

        self.event_editor = EventEditor(self)
        self.puzzle_editor = PuzzleEditor(self)
        self.text_editor = TextEditor(self)
        self.script_editor = ScriptEditor(self)
        self.place_editor = PlaceEditor(self)
        self.background_editor = BackgroundEditor(self)
        self.sprite_editor = SpriteEditor(self)
        self.sound_profile_editor = SoundProfileEditor()
        self.sound_bank_editor = SoundBankEditor()
        self.time_definitions_editor = TimeDefinitionsEditor()
        self.movie_editor = MovieEditor()
        self.stream_editor = StreamEditor(self)

        self.event_editor.hide()
        self.puzzle_editor.hide()
        self.text_editor.hide()
        self.script_editor.hide()
        self.place_editor.hide()
        self.background_editor.hide()
        self.sprite_editor.hide()
        self.sound_profile_editor.hide()
        self.sound_bank_editor.hide()
        self.time_definitions_editor.hide()
        self.movie_editor.hide()
        self.stream_editor.hide()

        self.horizontal_layout.addWidget(self.event_editor, 3)
        self.horizontal_layout.addWidget(self.puzzle_editor, 3)
        self.horizontal_layout.addWidget(self.text_editor, 3)
        self.horizontal_layout.addWidget(self.script_editor, 3)
        self.horizontal_layout.addWidget(self.place_editor, 3)
        self.horizontal_layout.addWidget(self.background_editor, 3)
        self.horizontal_layout.addWidget(self.sprite_editor, 3)
        self.horizontal_layout.addWidget(self.sound_profile_editor, 3)
        self.horizontal_layout.addWidget(self.sound_bank_editor, 3)
        self.horizontal_layout.addWidget(self.time_definitions_editor, 3)
        self.horizontal_layout.addWidget(self.movie_editor, 3)
        self.horizontal_layout.addWidget(self.stream_editor, 3)

        self.active_editor = self.empty_editor

    def file_menu_open(self):
        if self.last_path is not None:
            if not self.unsaved_data_dialog():
                return
        file_path = SettingsManager().open_rom(self)
        if file_path == "":
            return

        rom = NintendoDSRom.fromFile(file_path)

        # Load language from arm9
        if rom.name == b"LAYTON2":
            logging.info(f"Game language: {rom.lang}")
            if not rom.is_eu:
                ret = QtWidgets.QMessageBox.warning(self, "Version is not PAL",
                                                    "Non-PAL Layton2 versions are not fully supported. Proceed?",
                                                    buttons=QtWidgets.QMessageBox.StandardButton.Abort |
                                                            QtWidgets.QMessageBox.StandardButton.Yes,
                                                    defaultButton=QtWidgets.QMessageBox.StandardButton.Abort)
                if ret == QtWidgets.QMessageBox.StandardButton.Abort:
                    return
        else:
            logging.warning("Not LAYTON2 game.")

        self.rom = rom
        RomSingleton(rom=self.rom)
        self.last_path = file_path
        self.file_save_action.setEnabled(True)
        self.file_save_as_action.setEnabled(True)
        self.tree_model.set_rom(self.rom)

        self.active_editor.hide()
        self.active_editor = self.empty_editor
        self.active_editor.show()
        self.pg_previewer.stop_renderer()

    def file_menu_save(self):
        if not self.overwrite_data_dialogue():
            return
        if self.last_path:
            self.rom.saveToFile(self.last_path)

    def file_menu_save_as(self):
        file_path = SettingsManager().save_rom(self)
        if file_path == "":
            return
        self.last_path = file_path
        self.rom.saveToFile(file_path)

    def file_tree_context_menu(self, point: QtCore.QPoint):
        index = self.file_tree.indexAt(point)
        if index.isValid():
            self.ft_context_menu.clear()
            category = index.internalPointer().category
            actions = category.get_context_menu(index, self.tree_changed_selection)
            if not actions:
                return
            for i, action_data in enumerate(actions):
                if action_data is None and i != 0 and i != len(actions) - 1:
                    self.ft_context_menu.addSeparator()
                    continue
                elif action_data is None:
                    continue
                name, callback = action_data
                action = QtGui.QAction(name, self.ft_context_menu)
                action.triggered.connect(callback)
                self.ft_context_menu.addAction(action)
            self.ft_context_menu.exec(self.file_tree.mapToGlobal(point))

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
        elif isinstance(node, SADLNode):
            self.active_editor = self.stream_editor
            sadl = node.get_sadl()
            sadl_player = SADLStreamPlayer()
            name = node.data()
            self.stream_editor.set_sadl(sadl, name)
            self.pg_previewer.start_renderer(
                SoundPreview(sadl_player, sadl, name)
            )
            set_previewer = True
        elif isinstance(node, SMDLNode):
            smdl_player = SMDLStreamPlayer()
            smdl, swdl = node.get_smdl(), node.get_swdl()
            sample_bank = node.sample_bank()
            smdl_player.create_temporal_sf2(swdl, sample_bank)
            self.pg_previewer.start_renderer(SoundPreview(smdl_player, smdl,
                                                          node.data()))
            set_previewer = True
        elif isinstance(node, PlaceVersion):
            self.active_editor = self.place_editor
            place = node.get_place()
            self.place_editor.set_place(place)

            self.pg_previewer.start_renderer(PlacePreview(place))
            set_previewer = True
        elif isinstance(node, BackgroundAsset):
            self.active_editor = self.background_editor
            self.background_editor.set_image(node.get_bg())
        elif isinstance(node, SoundFixNode):
            self.active_editor = self.sound_profile_editor
            self.sound_profile_editor.set_snd_profile(node.get_sound_profile_dlz())
        elif isinstance(node, TimeDefinitionsNode):
            self.active_editor = self.time_definitions_editor
            self.time_definitions_editor.set_time_dlz(node.get_time_definitions_dlz())
        elif isinstance(node, SpriteAsset):
            self.active_editor = self.sprite_editor
            self.sprite_editor.set_sprite(node.get_sprite())
        elif isinstance(node, SWDLNode):
            self.active_editor = self.sound_bank_editor
            self.sound_bank_editor.set_swdl(node.get_swdl())
        elif isinstance(node, MovieAsset):
            self.active_editor = self.movie_editor
            self.movie_editor.set_movie(node)

        if self.active_editor is None:
            self.active_editor = self.empty_editor

        if not set_previewer:
            self.pg_previewer.stop_renderer()

        self.active_editor.show()

    def unsaved_data_dialog(self):
        ret = QtWidgets.QMessageBox.warning(self, "Unsaved data", "Any unsaved data will be lost. Continue?",
                                            buttons=QtWidgets.QMessageBox.StandardButton.Yes |
                                                    QtWidgets.QMessageBox.StandardButton.No)
        return ret == QtWidgets.QMessageBox.StandardButton.Yes

    def overwrite_data_dialogue(self):
        ret = QtWidgets.QMessageBox.warning(self, "Overwrite data", "Any original data will be lost. Continue?",
                                            buttons=QtWidgets.QMessageBox.StandardButton.Yes |
                                                    QtWidgets.QMessageBox.StandardButton.No)
        return ret != QtWidgets.QMessageBox.StandardButton.No

    def closeEvent(self, event) -> None:
        self.pg_previewer.loop_lock.acquire()
        self.pg_previewer.gm.exit()
        self.pg_previewer.loop_lock.release()

    def character_id_to_name(self):
        CharacterNamesEditor(self.rom, self, QtCore.Qt.WindowType.Window)

    def toggle_theme(self):
        SettingsManager().toggle_theme()
        qdarktheme.setup_theme(SettingsManager().theme)

    def advanced_mode_toggled(self, checked: bool):
        SettingsManager().toggle_advanced_mode(checked)
