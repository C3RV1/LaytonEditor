import PIL.Image
import numpy as np
import sounddevice as sd
import wx
import wx.stc

import utility.gdstextscript
from formats.filesystem import *
from formats.gds import GDS
from formats.graphics.ani import AniSprite, AniSubSprite
from formats.graphics.bg import BGImage
from formats.place import Place
from formats.sound.swd import swd_read_samplebank, swd_read_presetbank
from gui import generated
from gui.place_editor import PlaceEditor

from gui.PygamePreviewer import PygamePreviewer
from previewers.event_preview.EventPlayer import EventPlayer
from previewers.puzzle_preview.PuzzlePlayer import PuzzlePlayer
from previewers.sadl_preview.SADLPreview import SADLPreview


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


def replace_extension(filename, extension):
    return ".".join(filename.split(".")[:-1]) + extension


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
        node = tree.AppendItem(treenode, name, data=(name, rom.get_archive(archive)))
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
        node = tree.AppendItem(treenode, name, data=(rom.filenames[index], rom))

    for name, fd in folder.folders:
        node = tree.AppendItem(treenode, name, data=(folder_get_subfolder_name(rom.filenames, fd), rom))
        treenode_import_from_nds_folder(tree, node, fd, rom)
    return treenode


def tree_import_from_nds_folder(tree: wx.TreeCtrl, folder: Folder, rom: NintendoDSRom,
                                root_name="root") -> wx.TreeItemId:
    tree.DeleteAllItems()
    root = tree.AddRoot(root_name)
    treenode_import_from_nds_folder(tree, root, folder, rom)


class FilesystemEditor(generated.FilesystemEditor):
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
        self.fp_stream_menu = wx.Menu()

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
        add_menu_item(self.fp_ani_menu, "Export Image", self.fp_ani_export_clicked)
        add_menu_item(self.fp_ani_menu, "Replace Image", self.fp_ani_replace_clicked)
        add_menu_item(self.fp_ani_menu, "Add Image", self.fp_ani_add_clicked)
        add_menu_item(self.fp_ani_menu, "Remove Image", self.fp_ani_remove_clicked)

        add_menu_item(self.fp_place_menu, "Edit Place", self.fp_place_edit_clicked)

        add_menu_item(self.fp_soundbank_menu, "Play Selected", self.fp_samplebank_play_clicked)

        add_menu_item(self.fp_puzzle_menu, "Apply changes", self.fp_puzzle_apply_mods)
        add_menu_item(self.fp_puzzle_menu, "Save changes", self.fp_puzzle_save)

        add_menu_item(self.fp_event_menu, "Apply changes and Save", self.fp_event_apply_and_save)

        add_menu_item(self.fp_stream_menu, "Export to WAV", self.fp_stream_export_wav)
        add_menu_item(self.fp_stream_menu, "Replace with WAV", self.fp_stream_import_wav)

        self.pygame_previewer: PygamePreviewer = PygamePreviewer.INSTANCE
        self.event_previewer = EventPlayer()
        self.puzzle_previewer = PuzzlePlayer()
        self.sadl_previewer = SADLPreview()

        self.puzzle_scintilla.SetEOLMode(wx.stc.STC_EOL_LF)

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

        # TODO: Version checking
        pass

    def refresh_preview(self):
        try:
            if not self.ft_filetree.GetSelections():
                return
        except RuntimeError:
            # wrapped c/c++ object of type TreeCtrl has been deleted
            return
        self.pygame_previewer.stop_renderer()

        name, archive = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())
        for menu_title in self.fp_menus_loaded:
            self.GetGrandParent().remove_menu(menu_title)
        self.fp_menus_loaded = []

        if self.preview_save:
            self.save_preview()
        self.preview_save = False
        self.preview_data = None

        if name.endswith(".arc") and name.split("/")[1] == "bg":
            background = BGImage(name, rom=archive)
            self.fp_bg_viewimage_scaled.load_bitmap(background.extract_image_wx_bitmap())
            self.fp_formats_book.SetSelection(3)  # Background page
            self.preview_data = background
            self.fp_menus_loaded.append("Background")
            self.GetGrandParent().add_menu(self.fp_bg_menu, "Background")
        elif name.endswith(".arc") and name.split("/")[1] == "ani":
            self.fp_formats_book.SetSelection(4)  # Animation page
            sprite = AniSprite(name, rom=archive)
            self.preview_data = sprite
            self.fp_ani_viewimage_scaled.load_bitmap(sprite.extract_image_wx_bitmap(0))
            self.fp_ani_imageindex.SetMax(len(sprite.images) - 1)
            self.fp_menus_loaded.append("Sprite")
            self.GetGrandParent().add_menu(self.fp_ani_menu, "Sprite")
        elif name.endswith(".arj") and name.split("/")[1] == "ani":
            sprite = AniSubSprite(name, rom=archive)
            self.preview_data = sprite
            self.fp_ani_viewimage_scaled.load_bitmap(sprite.extract_image_wx_bitmap(0))
            self.fp_ani_imageindex.SetMax(len(sprite.images) - 1)
            self.fp_formats_book.SetSelection(4)  # Animation page
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
            self.fp_place_viewer.load_place(place, self.rom)
            self.fp_place_viewer.Refresh()
            self.fp_formats_book.SetSelection(5)  # Placeviewer page
            self.fp_menus_loaded.append("Place")
            self.GetGrandParent().add_menu(self.fp_place_menu, "Place")
        elif name.endswith(".txt"):
            textfile = archive.open(name, "r")
            self.fp_text_edit.Clear()
            text = textfile.read()
            self.preview_data = (name, archive)
            self.fp_text_edit.WriteText(text)
            self.fp_formats_book.SetSelection(1)  # Text page
        elif res := re.search("^n([0-9]+).dat", name):
            self.puzzle_previewer.set_puzzle_id(int(res.group(1)))
            self.pygame_previewer.start_renderer(self.puzzle_previewer.pz_main)
            self.puzzle_scintilla.SetText(self.puzzle_previewer.puzzle_data.to_readable())
            self.puzzle_scintilla.ConvertEOLs(wx.stc.STC_EOL_LF)
            self.fp_formats_book.SetSelection(8) # DCC Page
            self.fp_menus_loaded.append("Puzzle")
            self.GetGrandParent().add_menu(self.fp_puzzle_menu, "Puzzle")
        elif name.endswith(".gds"):
            gds = GDS(name, rom=archive)
            if name.startswith("e"):
                index = int(name[1:7])
                self.event_previewer.set_event_id(index)
                self.pygame_previewer.start_renderer(self.event_previewer)
                self.puzzle_scintilla.SetText(self.event_previewer.event_data.to_readable())
                self.puzzle_scintilla.ConvertEOLs(wx.stc.STC_EOL_LF)
                self.fp_formats_book.SetSelection(8) # DCC Page
                self.fp_menus_loaded.append("Event")
                self.GetGrandParent().add_menu(self.fp_event_menu, "Event")
            else:
                self.fp_gds_stc.load_gds(gds)
                self.fp_formats_book.SetSelection(2)  # GDS page
        elif name.endswith(".plz"):
            if name not in self.opened_archives:
                self.opened_archives.append(name)
                treenode_import_from_plz_file(self.ft_filetree, self.ft_filetree.GetSelection(), name, self.rom)
            self.fp_formats_book.SetSelection(0)  # Empty page
        elif name.lower().endswith(".sad"):
            self.pygame_previewer.start_renderer(self.sadl_previewer)
            self.sadl_previewer.load_sound(name)
            self.fp_formats_book.SetSelection(0)  # Empty page
            self.fp_menus_loaded.append("Stream")
            self.GetGrandParent().add_menu(self.fp_stream_menu, "Stream")
        else:
            self.fp_formats_book.SetSelection(0)  # Empty page

    def save_preview(self):
        if isinstance(self.preview_data, FileFormat):
            self.preview_data.save()
        elif isinstance(self.preview_data, tuple):
            name, archive = self.preview_data
            if name.endswith(".txt"):
                with archive.open(name, "w+") as file:
                    file.write(self.fp_text_edit.GetValue())

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

    def fp_ani_edit_clicked(self, event):
        path, _archive = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())
        filename = path.split("/")[-1]
        self.GetGrandParent().open_sprite_editor_page(self.preview_data, filename)

    def fp_ani_export_clicked(self, event):
        self.preview_data: AniSprite
        image_index = self.fp_ani_imageindex.GetValue()
        image = self.preview_data.extract_image_pil(image_index)
        path, _archive = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())
        with wx.FileDialog(self, "Save image", wildcard="PNG file (*.png)|*.png",
                           defaultFile=replace_extension(path.split("/")[-1] + str(image_index), ".png"),
                           style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            if pathname:
                image.save(pathname)

    def fp_ani_replace_clicked(self, _event):
        self.preview_data: AniSprite
        image_index = self.fp_ani_imageindex.GetValue()
        with wx.FileDialog(self, "Open image", wildcard="PNG file (*.png)|*.png",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            if pathname:
                image = PIL.Image.open(pathname)
        self.preview_data.replace_image_pil(image_index, image)
        self.fp_ani_viewimage_scaled.load_bitmap(self.preview_data.extract_image_wx_bitmap(image_index))
        self.preview_save = True

    def fp_ani_add_clicked(self, _event):
        self.preview_data: AniSprite
        with wx.FileDialog(self, "Open image", wildcard="PNG file (*.png)|*.png",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            if pathname:
                image = PIL.Image.open(pathname)
        self.preview_data.append_image_pil(image)
        self.fp_ani_viewimage_scaled.load_bitmap(self.preview_data.extract_image_wx_bitmap(-1))
        self.fp_ani_imageindex.SetMax(len(self.preview_data.images) - 1)
        self.fp_ani_imageindex.SetValue(len(self.preview_data.images) - 1)
        self.preview_save = True

    def fp_ani_remove_clicked(self, event):
        # TODO: Completely remove, and fix animation indexes
        self.preview_data: AniSprite
        image_index = self.fp_ani_imageindex.GetValue()
        self.preview_data.images[image_index] = np.ndarray((1, 1), np.uint8)
        self.fp_ani_viewimage_scaled.load_bitmap(image_index)
        self.preview_save = True

    def fp_samplebank_play_clicked(self, event):
        index = list(self.preview_data.samples.keys())[self.fp_samplebank_list.GetSelection()]
        sample = self.preview_data.samples[index]
        sd.play(sample.pcm, sample.samplerate)

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

    def fp_bg_export_clicked(self, event):
        self.preview_data: BGImage
        image = self.preview_data.extract_image_pil()
        path, _archive = self.ft_filetree.GetItemData(self.ft_filetree.GetSelection())
        with wx.FileDialog(self, "Save image", wildcard="PNG file (*.png)|*.png",
                           defaultFile=replace_extension(path.split("/")[-1], ".png"),
                           style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            if pathname:
                image.save(pathname)

    def fp_bg_import_clicked(self, event):
        self.preview_data: BGImage
        with wx.FileDialog(self, "Open image", wildcard="PNG file (*.png)|*.png",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            if pathname:
                image = PIL.Image.open(pathname)
        self.preview_data.import_image_pil(image)
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

    def fp_place_edit_clicked(self, event):
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

    def fp_text_edit_changed(self, _event):
        self.preview_save = True

    def fp_puzzle_apply_mods(self, event):
        successful, error_msg = self.puzzle_previewer.puzzle_data.from_readable(self.puzzle_scintilla.GetText())
        if not successful:
            error_dialog = wx.MessageDialog(self, error_msg, style=wx.ICON_ERROR | wx.OK)
            error_dialog.ShowModal()
        else:
            self.pygame_previewer.start_renderer(self.puzzle_previewer.pz_main)

    def fp_puzzle_save(self, event):
        successful, error_msg = self.puzzle_previewer.puzzle_data.from_readable(self.puzzle_scintilla.GetText())
        if not successful:
            error_dialog = wx.MessageDialog(self, error_msg, style=wx.ICON_ERROR | wx.OK)
            error_dialog.ShowModal()
        else:
            self.puzzle_previewer.puzzle_data.save_to_rom()

    def fp_event_apply_and_save(self, event):
        successful, error_msg = self.event_previewer.event_data.from_readable(self.puzzle_scintilla.GetText())
        if not successful:
            error_dialog = wx.MessageDialog(self, error_msg, style=wx.ICON_ERROR | wx.OK)
            error_dialog.ShowModal()
        else:
            self.event_previewer.event_data.save_to_rom()
            self.pygame_previewer.start_renderer(self.event_previewer)

    def fp_stream_export_wav(self, event):
        pass

    def fp_stream_import_wav(self, event):
        pass
