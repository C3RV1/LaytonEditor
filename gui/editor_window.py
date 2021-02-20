from typing import BinaryIO, Union

import ndspy.rom
import wx.aui
import wx.stc

from formats.filesystem import NintendoDSRom
from gui import generated
from gui.filesystem_editor import FilesystemEditor
from gui.puzzle_base_data_editor import PuzzleBaseDataEditor
from gui.puzzle_general_editor import PuzzleGeneralEditor
from gui.sprite_editor import SpriteEditor


class MainEditor(generated.MainEditor):
    rom: NintendoDSRom = None
    rom_last_filename: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Helper functions
    def open_rom(self, rom: Union[NintendoDSRom, BinaryIO, bytes, str, ndspy.rom.NintendoDSRom]):
        if isinstance(rom, str):  # Filename
            self.rom_last_filename = rom
            self.rom = NintendoDSRom.fromFile(rom)
        elif isinstance(rom, BinaryIO):  # File
            self.rom = NintendoDSRom(rom.read())
        elif isinstance(rom, bytes):  # Raw bytes
            self.rom = NintendoDSRom(rom)
        elif isinstance(rom, ndspy.rom.NintendoDSRom):
            self.rom = NintendoDSRom(rom.save())
        elif isinstance(rom, NintendoDSRom):
            self.rom = rom

        # Only open the main filesystem page.
        self.le_editor_pages.DeleteAllPages()
        self.open_filesystem_page("Rom FS")

    def save_rom(self, filename):
        self.rom.saveToFile(filename)
        self.rom_last_filename = filename

    def open_filesystem_page(self, name, folder=None):
        page = FilesystemEditor(self.le_editor_pages, name=name)
        self.le_editor_pages.AddPage(page, name)
        page.set_folder_and_rom(folder if folder else self.rom.filenames, self.rom)
        self.le_editor_pages.ChangeSelection(self.le_editor_pages.GetPageIndex(page))

    def open_sprite_editor_page(self, sprite, name):
        page = SpriteEditor(self.le_editor_pages, name=name)
        page.load_sprite(sprite)
        self.le_editor_pages.AddPage(page, name)
        current_page = self.le_editor_pages.GetPage(self.le_editor_pages.GetSelection())
        current_page.exit()
        self.le_editor_pages.ChangeSelection(self.le_editor_pages.GetPageIndex(page))
        page.enter()

    def add_menu(self, menu, title):
        self.le_menu.Append(menu, title)

    def remove_menu(self, title):
        index = self.le_menu.FindMenu(title)
        if index != -1:
            self.le_menu.Remove(index)

    # Menu : File
    def le_menu_file_open_OnMenuSelection(self, event):
        # Todo: Ask for saving currently opened rom
        with wx.FileDialog(self, "Open NDS rom", wildcard="NDS rom (*.nds)|*.nds",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            if pathname:
                self.open_rom(pathname)

    def le_menu_file_save_OnMenuSelection(self, event):
        if not self.rom_last_filename:
            return self.le_menu_file_saveas_OnMenuSelection(event)
        self.save_rom(self.rom_last_filename)

    def le_menu_file_saveas_OnMenuSelection(self, event):
        with wx.FileDialog(self, "Save NDS ROM", wildcard="NDS files (*.nds)|*.nds",
                           style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            if pathname:
                self.save_rom(pathname)

    def le_page_changed(self, event):
        page = self.le_editor_pages.GetPage(self.le_editor_pages.GetSelection())
        page.enter()

    def le_page_changing(self, event: wx.aui.AuiNotebookEvent):
        if (selection := self.le_editor_pages.GetSelection()) != -1:
            page = self.le_editor_pages.GetPage(selection)
            page.exit()
        event.Skip(1)  # Do this so the event doesn't get vetoed.

    def le_page_close(self, event: wx.aui.AuiNotebookEvent):
        page = self.le_editor_pages.GetPage(event.GetOldSelection())
        page.exit()

    def le_menu_puzzles_edit_gds_clicked(self, _event):
        if self.rom is None:
            return
        PuzzleGeneralEditor(self).Show(True)

    def le_menu_puzzles_edit_base_data_clicked(self, _event):
        if self.rom is None:
            return
        PuzzleBaseDataEditor(self).Show(True)
