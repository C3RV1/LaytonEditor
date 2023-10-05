from PySide6 import QtCore, QtWidgets, QtGui
from .ui.MainEditor import MainEditorUI
from pg_utils.rom.RomSingleton import RomSingleton
from .PygamePreviewer import PygamePreviewer
from .tabs import *

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

        self.pg_previewer = PygamePreviewer()
        self.pg_previewer.start()

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

        tabs = []
        if SettingsManager().advanced_mode:
            tabs.append(("Filesystem", FilesystemTab(self.rom)))
        if rom.name == b"LAYTON2":
            tabs.extend([
                ("Graphics", GraphicsTab(self.rom)),
                ("Sound", SoundTab(self.rom, self.pg_previewer)),
                ("Places", PlacesTab(self.rom, self.pg_previewer)),
                ("Events", EventsTab(self.rom, self.pg_previewer)),
                ("Puzzles", PuzzlesTab(self.rom, self.pg_previewer)),
                ("Other", OtherTab(self.rom))
            ])
        else:
            tabs.extend([
                ("Graphics", GraphicsTab(self.rom)),
                ("Sound", SoundTab(self.rom, self.pg_previewer)),
                ("Other", OtherTab(self.rom))
            ])

        self.setup_tabs(tabs)

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
