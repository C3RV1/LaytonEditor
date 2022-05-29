from typing import BinaryIO, Union

import ndspy.rom
import wx.aui
import wx.stc

from formats import conf
from formats.filesystem import NintendoDSRom
from gui import generated
from gui.filesystem_editor import FilesystemEditor
from gui.sprite_editor import SpriteEditor
from gui.event_editor import EventEditor
from gui.PygamePreviewer import PygamePreviewer
from pg_utils.rom.RomSingleton import RomSingleton


class MainEditor(generated.MainEditor):
    rom: NintendoDSRom = None
    rom_last_filename: str = ""
    last_page: int = -1

    ASK_BEFORE_OPENING = True

    def __init__(self, *args, **kwargs):
        self.pygame_previewer = PygamePreviewer()
        self.pygame_previewer.start()
        super().__init__(*args, **kwargs)

    # Helper functions
    def open_rom(self, rom: Union[NintendoDSRom, BinaryIO, bytes, str, ndspy.rom.NintendoDSRom]):
        rom_last_filename = self.rom_last_filename
        if isinstance(rom, str):  # Filename
            rom_last_filename = rom
            rom = NintendoDSRom.fromFile(rom)
        elif isinstance(rom, BinaryIO):  # File
            rom = NintendoDSRom(rom.read())
        elif isinstance(rom, bytes):  # Raw bytes
            rom = NintendoDSRom(rom)
        elif isinstance(rom, ndspy.rom.NintendoDSRom):
            rom = NintendoDSRom(rom.save())
        elif isinstance(rom, NintendoDSRom):
            rom = rom

        # Load language from arm9
        if rom.name == b"LAYTON2":
            arm9 = rom.loadArm9()
            lang_address = 0x02000d3c-arm9.ramAddress
            lang_id = rom.arm9[lang_address]
            lang_table = ["jp", "en", "sp", "fr", "it", "ge", "du", "ko", "ch"]
            try:
                conf.LANG = lang_table[lang_id]
            except IndexError:  # US version?
                # TODO: Figure out how to read it properly
                conf.LANG = "en"
            print(f"Game language: {conf.LANG}")
            if conf.LANG == "jp":
                error_dialog = wx.MessageDialog(self, "Japanese is not currently supported",
                                                style=wx.ICON_ERROR | wx.OK)
                error_dialog.ShowModal()
                return
        else:
            warning_game_dialog = wx.MessageDialog(self, "Warning: LaytonEditor is specifically made to edit "
                                                         "Layton 2, and support with other games is not guaranteed.",
                                                   style=wx.ICON_WARNING | wx.OK)
            warning_game_dialog.ShowModal()
            conf.LANG = "en"

        # After checking language
        self.rom = rom
        self.rom_last_filename = rom_last_filename

        RomSingleton(rom=self.rom)

        # Only open the main filesystem page.
        self.le_editor_pages.DeleteAllPages()
        menus_to_remove = []
        for menu in self.le_menu.Menus:
            if menu[1] != "File":
                menus_to_remove.append(menu[1])
        for menu_to_remove in menus_to_remove:
            self.remove_menu(menu_to_remove)
        self.open_filesystem_page("Rom FS")

    def save_rom(self, filename):
        if self.rom is None:
            return
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

    def open_event_editor_page(self, event, name):
        page = EventEditor(self.le_editor_pages, name=name)
        page.load_event(event)
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
        if self.rom is not None and self.ASK_BEFORE_OPENING:
            ask_to_save_dialog = wx.MessageDialog(self, "Do you want to save the currently opened ROM?",
                                                  style=wx.YES_NO | wx.CANCEL)
            v = ask_to_save_dialog.ShowModal()
            if v == wx.ID_YES:
                self.le_menu_file_save_OnMenuSelection(event)
            elif v == wx.ID_NO:
                pass
            else:
                return
        with wx.FileDialog(self, "Open NDS rom", wildcard="NDS rom (*.nds)|*.nds",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            if pathname:
                self.open_rom(pathname)

    def le_menu_file_save_OnMenuSelection(self, event):
        if self.rom is None:
            return
        if not self.rom_last_filename:
            return self.le_menu_file_saveas_OnMenuSelection(event)
        self.save_rom(self.rom_last_filename)

    def le_menu_file_saveas_OnMenuSelection(self, event):
        if self.rom is None:
            return
        with wx.FileDialog(self, "Save NDS ROM", wildcard="NDS files (*.nds)|*.nds",
                           style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            if pathname:
                self.save_rom(pathname)

    def le_page_changed(self, event):
        if self.last_page != -1:
            page = self.le_editor_pages.GetPage(self.last_page)
            page.exit()
        page = self.le_editor_pages.GetPage(self.le_editor_pages.GetSelection())
        page.enter()

    def le_page_changing(self, event: wx.aui.AuiNotebookEvent):
        self.last_page = self.le_editor_pages.GetSelection()
        event.Skip(1)  # Do this so the event doesn't get vetoed.

    def le_page_close(self, event: wx.aui.AuiNotebookEvent):
        page = self.le_editor_pages.GetPage(event.GetOldSelection())
        if not page.close():
            event.Veto()  # Cancel the event as we cannot close the page

    def close_window(self, _event):
        dialog = wx.MessageDialog(self, "Are you sure you want to exit?\nAll unsaved changes won't be saved.",
                                  style=wx.OK | wx.CANCEL)
        result = dialog.ShowModal()
        if result == wx.ID_OK:
            self.pygame_previewer.loop_lock.acquire()
            self.pygame_previewer.gm.exit()
            self.pygame_previewer.loop_lock.release()
            self.Destroy()
