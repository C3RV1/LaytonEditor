import PIL.Image
import wx
import wx.stc

import utility.gdstextscript
from formats.filesystem import *
from formats.gds import GDS
from formats.event import Event
from formats.graphics.ani import AniSprite, AniSubSprite
from formats.graphics.bg import BGImage
from formats.place import Place
from formats.puzzle import Puzzle
from formats.sound.swd import swd_read_samplebank, swd_read_presetbank
from formats.sound import wav, sadl, sample_transform
import numpy as np
import pygame as pg
from formats.sound.SMDLMidiSequencer import SMDLMidiSequencer
import mido
from gui import generated
from gui.place_editor import PlaceEditor

from gui.PygamePreviewer import PygamePreviewer
from pg_utils.sound.SADLStreamPlayer import SADLStreamPlayer
from pg_utils.sound.SMDLStreamPlayer import SMDLStreamPlayer
from previewers.place.PlacePreview import PlacePreview
from utility.path import set_extension
from previewers.event.EventPlayer import EventPlayer
from previewers.puzzle.PuzzlePlayer import PuzzlePlayer
from previewers.sound.SoundPreview import SoundPreview

from pg_utils.rom.rom_extract import load_sadl, load_smd


class ClipBoardFile:
    def __init__(self, name: str, raw: bytes):
        self.name = name
        self.raw = raw

    name: str
    raw: bytes


gds_cmd_help = {
    "sleep": "(int) ticks",
    "fade_out": "",
    "fade_in": "",
    "idle": "(int) ticks",
    "load_bg_bottom": "(str) filename, (int) mode?",
    "load_bg_top": "(str) filename, (int) mode?",
    "play_st_stream": "(int) index, (float) volume?"
}


def skip_event_dat(archive: str, filename: str):
    if re.match(r"^ev_d([0-9]{1,2})[abc]?\.plz$", archive.split("/")[-1]):
        if filename[0] != "e":
            return True
    return False


# Trees
def treenode_import_from_plz_file(tree: wx.TreeCtrl, treenode: wx.TreeItemId,
                                  archive: str, rom: NintendoDSRom) -> wx.TreeItemId:
    tree.DeleteChildren(treenode)
    for name in rom.get_archive(archive).filenames:
        if skip_event_dat(archive, name):  # Skip dat files for events
            continue
        _node = tree.AppendItem(treenode, name, data=(name, rom.get_archive(archive)))
    return treenode


def folder_get_subfolder_name(folder: Folder, subfolder: Folder, prefix=""):
    for nm, fd in folder.folders:
        if fd == subfolder:
            return prefix + nm + "/"
        elif nm := folder_get_subfolder_name(fd, subfolder, prefix + nm + "/"):
            return nm
    return None


def treenode_import_from_nds_folder(tree: wx.TreeCtrl, treenode: wx.TreeItemId,
                                    folder: Folder, rom: NintendoDSRom) -> wx.TreeItemId:
    tree.DeleteChildren(treenode)
    for index, name in enumerate(folder.files, folder.firstID):
        _node = tree.AppendItem(treenode, name, data=(rom.filenames[index], rom))

    for name, fd in folder.folders:
        node = tree.AppendItem(treenode, name, data=(folder_get_subfolder_name(rom.filenames, fd), rom))
        treenode_import_from_nds_folder(tree, node, fd, rom)
    return treenode


def tree_import_from_nds_folder(tree: wx.TreeCtrl, folder: Folder, rom: NintendoDSRom,
                                root_name="root") -> None:
    tree.DeleteAllItems()
    root = tree.AddRoot(root_name)
    treenode_import_from_nds_folder(tree, root, folder, rom)


class FilesystemEditor(generated.FilesystemEditor):
    PUZZLE_REGEX = re.compile("^n([0-9]+).dat")
    base_folder: Folder = None
    rom: NintendoDSRom = None
    preview_data = None
    preview_save = False
    opened_archives: list

    clipboard: ClipBoardFile = None
    fp_gds_stc_last_command = ""

    fs_menu: wx.Menu
    fp_bg_menu: wx.Menu
    fp_ani_menu: wx.Menu
    fp_place_menu: wx.Menu
    fp_soundbank_menu: wx.Menu
    fp_menus_loaded: list

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opened_archives = []
        self.fp_menus_loaded = []

        maineditor = self.GetGrandParent()
        self.fs_menu = wx.Menu()
        self.fp_bg_menu = wx.Menu()
        self.fp_ani_menu = wx.Menu()
        self.fp_place_menu = wx.Menu()
        self.fp_soundbank_menu = wx.Menu()
        self.fp_puzzle_menu = wx.Menu()
        self.fp_event_menu = wx.Menu()
        self.fp_gds_menu = wx.Menu()
        self.fp_stream_menu = wx.Menu()
        self.fp_sequenced_menu = wx.Menu()
        self.fp_text_menu = wx.Menu()

        def add_menu_item(menu, title, handler):
            fs_menu_item = wx.MenuItem(menu, wx.ID_ANY, title)
            menu.Append(fs_menu_item)
            maineditor.Bind(wx.EVT_MENU, handler, id=fs_menu_item.GetId())

        add_menu_item(self.fs_menu, "Reload", self.fs_reload_clicked)
        add_menu_item(self.fs_menu, "Remove Item", self.fs_remove_clicked)
        self.fs_menu.AppendSeparator()
        add_menu_item(self.fs_menu, "Cut Item", self.fs_cut_clicked)
        add_menu_item(self.fs_menu, "Copy Item", self.fs_copy_clicked)
        add_menu_item(self.fs_menu, "Paste Item", self.fs_paste_clicked)
        self.fs_menu.AppendSeparator()
        add_menu_item(self.fs_menu, "Extract Item", self.fs_extract_clicked)
        add_menu_item(self.fs_menu, "Replace Item", self.fs_replace_clicked)

        add_menu_item(self.fp_bg_menu, "Export Image", self.fp_bg_export_clicked)
        add_menu_item(self.fp_bg_menu, "Import Image", self.fp_bg_import_clicked)

        add_menu_item(self.fp_ani_menu, "Edit Sprite", self.fp_ani_edit_clicked)

        add_menu_item(self.fp_place_menu, "Edit Place", self.fp_place_edit_clicked)

        add_menu_item(self.fp_soundbank_menu, "Play Selected", self.fp_samplebank_play_clicked)

        add_menu_item(self.fp_puzzle_menu, "Apply changes", self.fp_puzzle_apply_mods)
        add_menu_item(self.fp_puzzle_menu, "Save changes", self.fp_puzzle_save)

        add_menu_item(self.fp_event_menu, "Apply changes DCC", self.fp_event_apply_changes)
        add_menu_item(self.fp_event_menu, "Apply changes EventScript", self.fp_event_apply_changes_evscript)
        add_menu_item(self.fp_event_menu, "Save changes DCC", self.fp_event_save_changes)
        add_menu_item(self.fp_event_menu, "Save changes EventScript", self.fp_event_save_changes_evscript)
        add_menu_item(self.fp_event_menu, "Edit Visually", self.fp_open_event_editor)

        add_menu_item(self.fp_gds_menu, "Save", self.fp_gds_save_changes)

        add_menu_item(self.fp_stream_menu, "Export to WAV", self.fp_stream_export_wav)
        add_menu_item(self.fp_stream_menu, "Replace with WAV", self.fp_stream_import_wav)

        add_menu_item(self.fp_sequenced_menu, "Export to MID", self.fp_sequenced_export_mid)

        add_menu_item(self.fp_text_menu, "Save", self.fp_text_save)

        self.previewer: PygamePreviewer = PygamePreviewer.INSTANCE

        self.dcc_editor.SetEOLMode(wx.stc.STC_EOL_LF)

    def set_folder_and_rom(self, folder: Folder, rom: NintendoDSRom):
        self.base_folder = folder
        self.rom = rom
        tree_import_from_nds_folder(self.ft_filetree, folder, rom)

    def enter(self):
        self.GetGrandParent().add_menu(self.fs_menu, "Filesystem")

        # TODO: Version checking and reloading
        self.refresh_preview()

    def exit(self):
        for menu_title in self.fp_menus_loaded:
            self.GetGrandParent().remove_menu(menu_title)
        self.GetGrandParent().remove_menu("Filesystem")

    def close(self):
        # Filesystem can't be closed
        return False

    def refresh_preview(self):
        try:
            if not self.ft_filetree.GetSelections():
                return
        except RuntimeError:
            # wrapped c/c++ object of type TreeCtrl has been deleted
            return

        name, archive = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())
        for menu_title in self.fp_menus_loaded:
            self.GetGrandParent().remove_menu(menu_title)
        self.fp_menus_loaded = []

        self.preview_data = None

        set_previewer = False

        if name.endswith(".arc") and name.split("/")[1] == "bg":
            background = BGImage(name, rom=archive)
            self.fp_bg_viewimage_scaled.load_bitmap(background.extract_image_wx_bitmap())
            self.fp_formats_book.SetSelection(3)  # Background page
            self.preview_data = background
            self.fp_menus_loaded.append("Background")
            self.GetGrandParent().add_menu(self.fp_bg_menu, "Background")
        elif name.endswith(".arc") or name.endswith(".arj") and name.split("/")[1] == "ani":
            self.fp_formats_book.SetSelection(4)  # Animation page
            if name.endswith(".arc"):
                sprite = AniSprite(name, rom=archive)
            else:
                sprite = AniSubSprite(name, rom=archive)
            self.preview_data = sprite
            self.fp_ani_viewimage_scaled.load_bitmap(sprite.extract_image_wx_bitmap(0))
            self.fp_ani_imageindex.SetMax(len(sprite.images) - 1)
            self.fp_menus_loaded.append("Sprite")
            self.GetGrandParent().add_menu(self.fp_ani_menu, "Sprite")
        elif name.lower().endswith("999.swd") and name.split("/")[1] == "sound":
            self.fp_samplebank_list.Clear()
            samplebank = swd_read_samplebank(archive.open(name))
            for sample in samplebank.samples:
                self.fp_samplebank_list.AppendItems(f"Sample {sample}")
            self.fp_menus_loaded.append("Samplebank")
            self.GetGrandParent().add_menu(self.fp_soundbank_menu, "Samplebank")
            self.fp_formats_book.SetSelection(6)  # samplebank page
            self.preview_data = samplebank
        elif name.lower().endswith(".swd"):
            presetbank = swd_read_presetbank(archive.open(name))
            self.fp_info_text.Clear()
            text = "using samples: " + ", ".join([str(x) for x in presetbank.samples_info.keys()])
            self.fp_info_text.WriteText(text)
            self.fp_formats_book.SetSelection(7)  # Info page
        elif name.startswith("n_place"):
            place = Place(name, rom=archive)
            self.previewer.start_renderer(PlacePreview(place))
            set_previewer = True
            self.fp_place_viewer.load_place(place, self.rom)
            self.fp_place_viewer.Refresh()
            self.fp_formats_book.SetSelection(5)  # Placeviewer page
            self.fp_menus_loaded.append("Place")
            self.GetGrandParent().add_menu(self.fp_place_menu, "Place")
        elif name.endswith(".txt"):
            textfile = archive.open(name, "r")
            self.fp_text_edit.Clear()
            try:
                text = textfile.read()
                self.preview_data = (name, archive)
                self.fp_text_edit.WriteText(text)
                self.fp_formats_book.SetSelection(1)  # Text page
            except UnicodeDecodeError:  # uses shift-jis
                print("Shift-jis text cannot be previewed for now")
            finally:
                textfile.close()
            self.fp_menus_loaded.append("Text")
            self.GetGrandParent().add_menu(self.fp_text_menu, "Text")
        elif res := self.PUZZLE_REGEX.search(name):
            puzzle = Puzzle(self.rom, id_=res.group(1))
            self.preview_data = puzzle
            puzzle.set_internal_id(int(res.group(1)))
            puzzle.load_from_rom()
            self.previewer.start_renderer(PuzzlePlayer(puzzle))
            set_previewer = True
            self.dcc_editor.SetText(puzzle.to_readable())
            self.dcc_editor.ConvertEOLs(wx.stc.STC_EOL_LF)
            self.fp_formats_book.SetSelection(8)  # DCC Page
            self.fp_menus_loaded.append("Puzzle")
            self.GetGrandParent().add_menu(self.fp_puzzle_menu, "Puzzle")
        elif name.endswith(".gds"):
            if name.startswith("e"):
                index = int(name[1:7])
                event = Event(self.rom)
                self.preview_data = event
                event.set_event_id(index)
                event.load_from_rom()
                self.previewer.start_renderer(EventPlayer(event))
                set_previewer = True
                self.dcc_editor.SetText(event.to_readable())
                self.dcc_editor.ConvertEOLs(wx.stc.STC_EOL_LF)
                self.fp_formats_book.SetSelection(8)  # DCC Page
                self.fp_menus_loaded.append("Event")
                self.GetGrandParent().add_menu(self.fp_event_menu, "Event")
            else:
                gds = GDS(name, rom=archive)
                self.preview_data = gds
                self.dcc_editor.SetText(gds.to_readable())
                self.dcc_editor.ConvertEOLs(wx.stc.STC_EOL_LF)
                self.fp_formats_book.SetSelection(8)  # DCC Page
                self.fp_menus_loaded.append("GDS Script")
                self.GetGrandParent().add_menu(self.fp_gds_menu, "GDS Script")
        elif name.endswith(".plz"):
            if name not in self.opened_archives:
                self.opened_archives.append(name)
                treenode_import_from_plz_file(self.ft_filetree, self.ft_filetree.GetSelection(), name, self.rom)
            self.fp_formats_book.SetSelection(0)  # Empty page
        elif name.lower().endswith(".sad"):
            sound_previewer = SoundPreview(SADLStreamPlayer(), load_sadl(name), name)
            self.previewer.start_renderer(sound_previewer)
            set_previewer = True
            self.fp_formats_book.SetSelection(0)  # Empty page
            self.fp_menus_loaded.append("Stream")
            self.GetGrandParent().add_menu(self.fp_stream_menu, "Stream")
        elif name.lower().endswith(".smd"):
            smdl_stream_player = SMDLStreamPlayer()
            smdl, swd_presets = load_smd(name)
            smdl_stream_player.set_preset_dict(swd_presets)
            sound_previewer = SoundPreview(smdl_stream_player, smdl, name)
            self.previewer.start_renderer(sound_previewer)
            set_previewer = True
            self.fp_formats_book.SetSelection(0)
            self.fp_menus_loaded.append("Sequenced")
            self.GetGrandParent().add_menu(self.fp_sequenced_menu, "Sequenced")
        else:
            self.fp_formats_book.SetSelection(0)  # Empty page

        if not set_previewer:
            self.previewer.stop_renderer()

    def ft_filetree_selchanged(self, event: wx.TreeEvent):
        self.refresh_preview()

    def fp_ani_imageindex_on_slider(self, event):
        self.preview_data: AniSprite
        self.fp_ani_viewimage_scaled.load_bitmap(
            self.preview_data.extract_image_wx_bitmap(self.fp_ani_imageindex.GetValue()))

    def ft_filetree_end_label_edit(self, event: wx.TreeEvent):
        wx.CallAfter(self.ft_filetree_finalize_label_edit, event)

    def ft_filetree_finalize_label_edit(self, _: wx.TreeEvent):
        selection = self.ft_filetree.GetSelection()
        oldpath, archive = self.ft_filetree.GetItemData(selection)
        newname = self.ft_filetree.GetItemText(selection)

        if oldpath.endswith("/"):  # folder
            *oldparents, oldname, noend = oldpath.split("/")
            if noend:
                oldparents.append(oldname)
            oldparent = "/".join(oldparents) + "/"
            newpath = oldparent + newname + "/"
            self.rom.rename_folder(oldpath, newpath)
        else:  # file
            oldfolder, oldname = os.path.split(oldpath)
            newpath = os.path.join(oldfolder, newname).replace("\\", "/")
            self.rom.rename_file(oldpath, newpath)

        self.ft_filetree.SetItemData(selection, (newpath, archive))

    def ft_filetree_keydown(self, event: wx.TreeEvent):
        if event.GetKeyCode() == wx.WXK_DELETE:
            self.fs_remove_clicked(event)

    def fs_remove_clicked(self, _event):  # TODO: Connect with event from MainEditor
        selection = self.ft_filetree.GetSelection()
        path, archive = self.ft_filetree.GetItemData(selection)
        if path.endswith("/"):  # folder
            self.rom.remove_folder(path)
        else:
            self.rom.remove_file(path)
        self.ft_filetree.Delete(selection)

    def ft_filetree_activated(self, event: wx.TreeEvent):
        path, archive = self.ft_filetree.GetItemData(event.GetItem())
        if path.endswith("/"):  # folder
            self.GetGrandParent().open_filesystem_page(self.ft_filetree.GetItemText(event.GetItem()),
                                                       self.rom.filenames[path])
        else:  # file
            pass

    def fs_reload_clicked(self, _event):
        self.opened_archives = []
        tree_import_from_nds_folder(self.ft_filetree, self.base_folder, self.rom)

    def fp_ani_edit_clicked(self, _):
        path, _archive = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())
        filename = path.split("/")[-1]
        self.GetGrandParent().open_sprite_editor_page(self.preview_data, filename)

    def fp_samplebank_play_clicked(self, _):
        index = list(self.preview_data.samples.keys())[self.fp_samplebank_list.GetSelection()]
        sample = self.preview_data.samples[index]
        sample_pcm = np.reshape(sample.pcm, (1, sample.pcm.shape[0]))
        target_rate = pg.mixer.get_init()[0]
        target_channels = pg.mixer.get_init()[2]
        sample_pcm = sample_transform.change_sample_rate(sample_pcm, sample.samplerate, target_rate)
        sample_pcm = sample_transform.change_channels(sample_pcm, target_channels)
        sample_pcm = sample_pcm.swapaxes(0, 1)
        sample_pcm = np.ascontiguousarray(sample_pcm)
        sound = pg.sndarray.make_sound(sample_pcm)
        sound.set_volume(0.5)
        sound.play()
        # sd.play(sample.pcm, sample.samplerate)

    def fs_replace_clicked(self, _event):  # TODO: Connect with MenuItem
        path, _archive = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())
        if path.endswith("/"):
            raise NotImplementedError("Extracting directories not implemented")
        with wx.FileDialog(self, "Replace file",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            if pathname:
                with open(pathname, "rb") as in_file:
                    with _archive.open(path, "wb") as game_file:
                        game_file.write(in_file.read())

        self.refresh_preview()

    def fs_extract_clicked(self, _event):  # TODO: Connect with MenuItem
        path, _archive = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())
        if path.endswith("/"):
            raise NotImplementedError("Extracting directories not implemented.")
        with wx.FileDialog(self, "Extract file",
                           defaultFile=path.split("/")[-1], style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            if pathname:
                with open(pathname, "wb+") as out_file:
                    with _archive.open(path, "rb") as game_file:
                        out_file.write(game_file.read())

    def fs_cut_clicked(self, _event):  # TODO: Connect with MenuItem
        path, archive = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())
        with archive.open(path, "rb") as file:
            raw = file.read()
        self.clipboard = ClipBoardFile(path.split("/")[-1], raw)
        archive.remove_file(path)
        self.ft_filetree.Delete(self.ft_filetree.GetSelection())

    def fs_copy_clicked(self, _event):  # TODO: Connect with MenuItem
        path, archive = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())
        if path.endswith("/"):
            raise NotImplementedError("Copying directories not implemented.")
        with archive.open(path, "rb") as file:
            raw = file.read()
        self.clipboard = ClipBoardFile(path.split("/")[-1], raw)

    def fs_paste_clicked(self, _event):  # TODO: Connect with MenuItem
        selection = self.ft_filetree.GetSelection()
        path, archive = self.ft_filetree.GetItemData(selection)
        if not path.endswith("/"):  # selected a file
            parent_item = self.ft_filetree.GetItemParent(selection)
            folder = "/".join(path.split("/")[:-1])
            folder += "/" if path else ""
        else:  # selected a folder
            parent_item = selection
            folder = path
        path = folder + self.clipboard.name
        with archive.open(path, "wb+") as file:
            file.write(self.clipboard.raw)

        self.ft_filetree.AppendItem(parent_item, self.clipboard.name, data=(path, archive))

    def fp_bg_export_clicked(self, _):
        self.preview_data: BGImage
        image = self.preview_data.extract_image_pil()
        path, _archive = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())
        with wx.FileDialog(self, "Save image", wildcard="PNG file (*.png)|*.png",
                           defaultFile=set_extension(path.split("/")[-1], ".png"),
                           style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            if pathname:
                image.save(pathname)

    def fp_bg_import_clicked(self, _):
        self.preview_data: BGImage
        with wx.FileDialog(self, "Open image", wildcard="PNG file (*.png)|*.png",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            if pathname:
                image = PIL.Image.open(pathname)
        self.preview_data.import_image_pil(image)
        self.preview_data.save()
        self.fp_bg_viewimage_scaled.load_bitmap(
            self.preview_data.extract_image_wx_bitmap())

    def fp_gds_stc_updateui(self, event):
        command = self.fp_gds_stc.GetCurLine()[0].split(" ")[0]
        if self.fp_gds_stc_last_command != command:
            if command in utility.gdstextscript.command_names:
                self.fp_gds_stc_last_command = command
                self.fp_gds_cmd_name.SetLabel(command)
                self.fp_gds_cmd_help.SetLabel(gds_cmd_help[command] if command in gds_cmd_help else "(params unknown)")
                self.fp_gds_cmd_help.GetParent().Layout()
            else:
                self.fp_gds_cmd_name.SetLabel("")
                self.fp_gds_cmd_help.SetLabel("")

    def fp_place_edit_clicked(self, _):
        # TODO: Cleanup with utility functions in editor window
        path, _archive = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())
        finds = re.findall(r"n_place([0-9]+)_([0-9]+)\.dat", path)
        index, subindex = int(finds[0][0]), int(finds[0][1])
        editor_window = self.GetGrandParent()
        page = PlaceEditor(editor_window.le_editor_pages, name=f"Place {index}")
        page.load_place(self.rom, index)
        editor_window.le_editor_pages.AddPage(page, f"Place {index}")
        self.exit()
        editor_window.le_editor_pages.ChangeSelection(editor_window.le_editor_pages.GetPageIndex(page))
        page.enter()

    def fp_puzzle_apply_mods(self, _):
        puzzle_data = self.preview_data
        successful, error_msg = puzzle_data.from_readable(self.dcc_editor.GetText())
        if not successful:
            error_dialog = wx.MessageDialog(self, error_msg, style=wx.ICON_ERROR | wx.OK)
            error_dialog.ShowModal()
        else:
            self.previewer.start_renderer(PuzzlePlayer(self.preview_data))

    def fp_puzzle_save(self, _):
        puzzle_data = self.preview_data
        successful, error_msg = puzzle_data.from_readable(self.dcc_editor.GetText())
        if not successful:
            error_dialog = wx.MessageDialog(self, error_msg, style=wx.ICON_ERROR | wx.OK)
            error_dialog.ShowModal()
        else:
            puzzle_data.save_to_rom()

    def fp_event_apply_changes(self, _):
        event_data = self.preview_data
        successful, error_msg = event_data.from_readable(self.dcc_editor.GetText())
        if not successful:
            error_dialog = wx.MessageDialog(self, error_msg, style=wx.ICON_ERROR | wx.OK)
            error_dialog.ShowModal()
        else:
            self.previewer.start_renderer(EventPlayer(event_data))

    def fp_event_save_changes(self, _):
        event_data = self.preview_data
        successful, error_msg = event_data.from_readable(self.dcc_editor.GetText())
        if not successful:
            error_dialog = wx.MessageDialog(self, error_msg, style=wx.ICON_ERROR | wx.OK)
            error_dialog.ShowModal()
        else:
            event_data.save_to_rom()
            self.previewer.start_renderer(EventPlayer(event_data))

    def fp_event_apply_changes_evscript(self, _):
        event_data: Event = self.preview_data
        successful, error_msg = event_data.from_event_script(self.dcc_editor.GetText())
        if not successful:
            error_dialog = wx.MessageDialog(self, error_msg, style=wx.ICON_ERROR | wx.OK)
            error_dialog.ShowModal()
        else:
            self.previewer.start_renderer(EventPlayer(event_data))

    def fp_event_save_changes_evscript(self, _):
        event_data = self.preview_data
        successful, error_msg = event_data.from_event_script(self.dcc_editor.GetText())
        if not successful:
            error_dialog = wx.MessageDialog(self, error_msg, style=wx.ICON_ERROR | wx.OK)
            error_dialog.ShowModal()
        else:
            event_data.save_to_rom()
            self.previewer.start_renderer(EventPlayer(event_data))

    def fp_gds_save_changes(self, _):
        gds: GDS = self.preview_data
        successful, error_msg = gds.from_readable(self.dcc_editor.GetText())
        if not successful:
            error_dialog = wx.MessageDialog(self, error_msg, style=wx.ICON_ERROR | wx.OK)
            error_dialog.ShowModal()
        else:
            gds.save()

    def fp_stream_export_wav(self, _):
        with wx.FileDialog(self, "Export to WAV", wildcard="WAV Files (*.wav)|*.wav", style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()

            with wx.ProgressDialog("Exporting to WAV", "This could take several minutes.", parent=self,
                                   style=wx.PD_APP_MODAL) as progressDialog:
                sadl_file_path, _ = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())
                sadl_file: sadl.SADL = load_sadl(sadl_file_path, self.rom)
                wav_obj = sadl_file.to_wav()
                with open(pathname, "wb") as f:
                    wav_obj.write_stream(f)
                progressDialog.Update(100, "Completed")

    def fp_stream_import_wav(self, _):
        with wx.FileDialog(self, "Import WAV", wildcard="WAV Files (*.wav)|*.wav",
                           style=wx.FD_OPEN) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            sadl_file_path, _ = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())

            with wx.ProgressDialog("Importing WAV...", "This could take several minutes.", parent=self,
                                   style=wx.PD_APP_MODAL | wx.PD_REMAINING_TIME | wx.PD_CAN_ABORT) as progressDialog:
                print("Loading sadl")
                sadl_obj: sadl.SADL = load_sadl(sadl_file_path)
                print("Importing")
                with open(pathname, "rb") as f:
                    wav_obj = wav.WAV()
                    wav_obj.read_stream(f)
                print("Encoding")
                sadl_obj.from_wav(wav_obj)
                print("Encoded")
                sadl_obj.save()

                self.refresh_preview()
                progressDialog.Update(100, "Completed")

    def fp_sequenced_export_mid(self, _):
        with wx.FileDialog(self, "Export to MID", wildcard="MID Files (*.mid)|*.mid", style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()

            with wx.ProgressDialog("Exporting to MID", "This could take several minutes.", parent=self,
                                   style=wx.PD_APP_MODAL) as progressDialog:
                smdl_file_path, _ = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())
                smdl, presets = load_smd(smdl_file_path, self.rom)
                smdl_seq = SMDLMidiSequencer(smdl)
                smdl_seq.create_program_map(presets)
                mid: mido.MidiFile = smdl_seq.generate_mid()
                mid.save(pathname)
                progressDialog.Update(100, "Completed")

    def fp_open_event_editor(self, _event):
        path, _archive = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())
        filename = path.split("/")[-1]
        self.GetGrandParent().open_event_editor_page(self.preview_data, filename)

    def fp_text_save(self, _event):
        name, archive = self.preview_data
        with archive.open(name, "w+") as file:
            file.write(self.fp_text_edit.GetValue())
