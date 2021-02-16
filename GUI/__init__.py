from os import remove
from os.path import join
import codecs
import GUI.generated.MainFrame
import GUI.generated.PuzzleMultipleChoice
import GUI.generated.PuzzleBaseDataEditor
import GUI.generated.ImageEdit
import GUI.generated.PuzzleInputEditor
from ndspy.rom import NintendoDSRom
from ndspy.fnt import Folder
import LaytonLib
from LaytonLib.puzzles import puzzle_data as pzd
import LaytonLib.asm_patching
import LaytonLib.gds
import PIL.Image as imgl
import wx
from wx import propgrid as pg

hexencoder = codecs.getencoder('hex_codec')
hexdecoder = codecs.getdecoder('hex_codec')


def auto_newline(text: str, max_line_length: int):
    def wrap_line_helper(line: str):
        words = line.split(" ")
        wrapped_line = []
        current_line = ""
        for word in words:
            current_line += word
            if len(current_line) > max_line_length:
                current_line = " ".join(current_line.split(" ")[:-1])
                wrapped_line.append(current_line)
                current_line = word
            current_line += " "
        wrapped_line.append(current_line[:-1])
        return "\n".join(wrapped_line)
    lines = text.split("\n")
    wrapped_lines = []
    for line1 in lines:
        wrapped_lines.append(wrap_line_helper(line1))
    return "\n".join(wrapped_lines)



class MainFrame(GUI.generated.MainFrame.MainFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.rom = None
        self.selected_image = 1
        self.selected_imagefile = None
        self.save_location = ""

        # For script/text editing
        self.selected_file = None
        self.selected_pack = None

        self.arm9backup = None

        # For character editing
        self.txt1_file = None
        self.selected_character = 0

    def OnMenuSelectionOpen(self, event):
        self.openFile()

    def openFile(self):
        with wx.FileDialog(self, "Open NDS ROM", wildcard="NDS files (*.nds)|*.nds",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'rb') as file:
                    self.rom = NintendoDSRom(file.read())

            except IOError:
                raise IOError("Unable to load rom.")
        self.setupAfterOpen()

    def setupAfterOpen(self):
        self.rom.arm9 = self.rom.loadArm9().save(compress=False)
        self.arm9backup = self.rom.arm9
        self.updateAniImageList()
        self.updateBGImageList()
        self.updateSimplifiedScriptList()

    def OnMenuSelectionSave(self, event):
        if not self.save_location:
            self.OnMenuSelectionSaveAs(event)
            return
        self.saveFile()

    def OnMenuSelectionSaveAs(self, event):
        with wx.FileDialog(self, "Save NDS ROM", wildcard="NDS files (*.nds)|*.nds",
                           style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

                # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.save_location = pathname
        self.saveFile()

    def saveFile(self):
        if not self.save_location:
            return
        with open(self.save_location, "wb+") as file:
            file.write(self.rom.save())

        successful = wx.MessageDialog(self, "Saved successfully")
        successful.ShowModal()

    # Helper function to update the list of image files
    def updateAniImageList(self):
        self.tree_imagefiles.DeleteAllItems()
        self.rom: NintendoDSRom
        if self.rom.name == b'LAYTON1':
            folder: Folder = self.rom.filenames["data/ani"]
        elif self.rom.name == b'LAYTON2':
            folder: Folder = self.rom.filenames["data_lt2/ani"]
        else:
            print(f"Could get images for: {self.rom.name}")
            return
        root = self.tree_imagefiles.AddRoot("ani")
        for img in folder.files:
            i = self.tree_imagefiles.AppendItem(root, img)
            self.tree_imagefiles.SetItemData(i, folder.idOf(img))
        for f in folder.folders:
            self.addFolder(root, f)

    # Helper function to add the contents of one folder with recursion.
    def addFolder(self, root, folder):
        nroot = self.tree_imagefiles.AppendItem(root, folder[0])
        fol = folder[1]
        for i in fol.files:
            j = self.tree_imagefiles.AppendItem(nroot, i)
            self.tree_imagefiles.SetItemData(j, fol.idOf(i))
        for f in fol.folders:
            self.addFolder(nroot, f)

    # When the user rightclicks on one of the items in the list of image files.
    def tree_imagefilesOnTreeSelChanged(self, event):
        file_id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not file_id:
            return

        self.selected_imagefile = LaytonLib.filesystem.File(self.rom, file_id)
        self.selected_imagefile = LaytonLib.images.ani.AniFile(self.rom, file_id)

        # Load the image from the ani file
        image = self.selected_imagefile.images[0].to_PIL()
        self.swap_preview_image(image)

        self.m_staticText_Colordepth.SetLabel(f"Colordepth: {self.selected_imagefile.colordepth}bit")
        self.m_staticText_imagename.SetLabel(self.rom.filenames[file_id])
        self.m_staticText_imageID.SetLabel(f"ID: {file_id} | {hex(file_id)}")

        self.selected_image = 1
        self.m_staticText_currentimage.SetLabel(f"{self.selected_image}/{len(self.selected_imagefile.images)}")

    def OnButtonClickPreviousImage(self, event):
        if len(self.selected_imagefile.images) < 2:
            return
        self.selected_image -= 1
        if self.selected_image < 1:
            self.selected_image = len(self.selected_imagefile.images)
        self.m_staticText_currentimage.SetLabel(f"{self.selected_image}/{len(self.selected_imagefile.images)}")
        image = self.selected_imagefile.images[self.selected_image - 1].to_PIL()
        self.swap_preview_image(image)

    def OnButtonClickNextImage(self, event):
        if len(self.selected_imagefile.images) < 2:
            return
        self.selected_image += 1
        if self.selected_image > len(self.selected_imagefile.images):
            self.selected_image = 1
        self.m_staticText_currentimage.SetLabel(f"{self.selected_image}/{len(self.selected_imagefile.images)}")
        image = self.selected_imagefile.images[self.selected_image - 1].to_PIL()
        self.swap_preview_image(image)

    def OnButtonClickExtract(self, event):
        with wx.FileDialog(self, "Extract File", style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'wb+') as file:
                    file.write(self.selected_imagefile.read())
            except IOError:
                return

    def OnButtonClickReplace(self, event):
        file_id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not file_id:
            return
        with wx.FileDialog(self, "Replace File", style=wx.FD_OPEN) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'rb') as file:
                    self.selected_imagefile.write(file.read())
                    self.selected_imagefile.reload()
            except IOError:
                return

    def OnButtonClickExtractDecom(self, event):
        file_id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not file_id:
            return
        with wx.FileDialog(self, "Extract Decompressed File", style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'wb+') as file:
                    file.write(LaytonLib.compression.decompress(self.selected_imagefile.read()[4:]))
            except IOError:
                return

    def OnButtonClickReplaceDecom(self, event):
        file_id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not file_id:
            return
        with wx.FileDialog(self, "Replace File", style=wx.FD_OPEN) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'rb') as file:
                    wtr = LaytonLib.binary.BinaryWriter()
                    # Simply compress the given file and pass it trough
                    wtr.writeU32(0x2)
                    wtr.write(LaytonLib.compression.compress(file.read(),
                                                             LaytonLib.compression.LZ10))
                    self.selected_imagefile.write(wtr.data)
                    del wtr
                    self.selected_imagefile.reload()

            except IOError:
                return

    def OnButtonClickSaveImage(self, event):
        file_id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not file_id:
            return
        with wx.FileDialog(self, "Save Image", style=wx.FD_SAVE, wildcard="PNG files (*.png)\
                |*.png;JPG files (*.jpg)|*.jpg;BMP files (*.bmp)|*.bmp;All FIles") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            img = self.selected_imagefile.images[self.selected_image - 1].to_PIL()
            img.save(pathname)

    def OnButtonClickReplaceImage(self, event):
        file_id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not file_id:
            return
        with wx.FileDialog(self, "Choose Image", style=wx.FD_OPEN, wildcard="PNG files (*.png)\
                        |*.png;JPG files (*.jpg)|*.jpg;BMP files (*.bmp)|*.bmp;All FIles") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            img = imgl.open(pathname)
            self.selected_imagefile.frame_from_PIL_nopalswap(self.selected_image - 1, img)
            self.selected_imagefile.save()
        self.swap_preview_image(self.selected_imagefile.frame_to_PIL(self.selected_image - 1))

    def OnButtonClickReplaceImageAddPall(self, event):
        file_id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not file_id:
            return
        with wx.FileDialog(self, "Choose Image", style=wx.FD_OPEN, wildcard="PNG files (*.png)\
                                |*.png;JPG files (*.jpg)|*.jpg;BMP files (*.bmp)|*.bmp;All FIles") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            img = imgl.open(pathname)
            self.selected_imagefile.frame_from_PIL_addpal(self.selected_image - 1, img)
            self.selected_imagefile.save()
        self.swap_preview_image(self.selected_imagefile.frame_to_PIL(self.selected_image - 1))

    # Helper function to swap the previouw image
    def swap_preview_image(self, image: imgl.Image):
        # Create a the full sized image
        fullimage = imgl.new("RGBA", (258, 194))

        # Paste it onto the full sized image
        fullimage.paste(image, (1, 1))
        edit = fullimage.load()
        for i in range(258):
            edit[i, 0] = (0, 0, 0, 255)
            edit[i, -1] = (0, 0, 0, 255)
        for i in range(1, 193):
            edit[0, i] = (0, 0, 0, 255)
            edit[-1, -i] = (0, 0, 0, 255)

        # Temporarely save it as a file to load it in wx
        fullimage.save("temp.bmp")
        wximage = wx.Image("temp.bmp")
        remove("temp.bmp")

        self.previewImage.SetBitmap(wximage.ConvertToBitmap())

    def OnButtonClickEditFile(self, event):
        file_id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not file_id:
            return
        imagefileeditor = ImageEdit(self, self.selected_imagefile)
        imagefileeditor.Show(True)

    def OnButtonClickPatchRom(self, event):
        print(self.arm9backup)
        setupcode_folder = self.m_textCtrl2.GetLabelText()
        gamecode_folder = self.m_textCtrl3.GetLabelText()
        arenalooffsptr = int(self.m_textCtrl31.GetLabelText(), 16)
        self.rom.arm9 = self.arm9backup
        LaytonLib.asm_patching.PatchRom(self.rom, setupcode_folder, gamecode_folder, arenalooffsptr)

    # Helper function to update the list of image files
    def updateBGImageList(self):
        self.tree_imagefiles1.DeleteAllItems()
        if self.rom.name == b'LAYTON1':
            folder: Folder = self.rom.filenames["data/bg"]
        elif self.rom.name == b'LAYTON2':
            folder: Folder = self.rom.filenames["data_lt2/bg"]
        root = self.tree_imagefiles1.AddRoot("bg")
        for img in folder.files:
            i = self.tree_imagefiles1.AppendItem(root, img)
            self.tree_imagefiles1.SetItemData(i, folder.idOf(img))
        for f in folder.folders:
            self.addFolderBG(root, f)

    # Helper function to add the contents of one folder with recursion.
    def addFolderBG(self, root, folder):
        nroot = self.tree_imagefiles1.AppendItem(root, folder[0])
        fol = folder[1]
        for i in fol.files:
            j = self.tree_imagefiles1.AppendItem(nroot, i)
            self.tree_imagefiles1.SetItemData(j, fol.idOf(i))
        for f in fol.folders:
            self.addFolderBG(nroot, f)

    def tree_imagefilesbgOnTreeSelChanged(self, event):
        file_id = self.tree_imagefiles1.GetItemData(self.tree_imagefiles1.GetSelection())
        if not file_id:
            return

        self.selected_imagefile = LaytonLib.filesystem.File(self.rom, file_id)
        self.selected_imagefile = LaytonLib.images.bg.BgFile(self.rom, file_id)

        self.updateBGImagePreview()

    def updateBGImagePreview(self):
        fullimage = self.selected_imagefile.img
        fullimage.save("temp.bmp")
        wximage = wx.Image("temp.bmp")
        remove("temp.bmp")

        self.previewImage1.SetBitmap(wximage.ConvertToBitmap())

    def OnButtonClickReplaceImageBG(self, event):
        file_id = self.tree_imagefiles1.GetItemData(self.tree_imagefiles1.GetSelection())
        if not file_id:
            return
        with wx.FileDialog(self, "Choose Image", style=wx.FD_OPEN, wildcard="PNG files (*.png)\
                                |*.png;JPG files (*.jpg)|*.jpg;BMP files (*.bmp)|*.bmp;All FIles") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            img = imgl.open(pathname)
            self.selected_imagefile.img = img
        self.updateBGImagePreview()
        self.selected_imagefile.save()

    def OnButtonClickSaveImageBG(self, event):
        file_id = self.tree_imagefiles1.GetItemData(self.tree_imagefiles1.GetSelection())
        if not file_id:
            return
        with wx.FileDialog(self, "Save Image", style=wx.FD_SAVE, wildcard="PNG files (*.png)\
                        |*.png;JPG files (*.jpg)|*.jpg;BMP files (*.bmp)|*.bmp;All FIles") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            img = self.selected_imagefile.img
            img.save(pathname)

    def OnButtonClickExtractBG(self, event):
        file_id = self.tree_imagefiles1.GetItemData(self.tree_imagefiles1.GetSelection())
        if not file_id:
            return
        with wx.FileDialog(self, "Extract File", style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'wb+') as file:
                    file.write(self.selected_imagefile.read())
            except IOError:
                return

    def OnButtonClickReplaceBG(self, event):
        file_id = self.tree_imagefiles1.GetItemData(self.tree_imagefiles1.GetSelection())
        if not file_id:
            return
        with wx.FileDialog(self, "Replace File", style=wx.FD_OPEN) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'rb') as file:
                    self.selected_imagefile.write(file.read())
                    self.selected_imagefile.reload()
            except IOError:
                return
        self.updateBGImagePreview()

    # Helper function to update the list of script files
    def updateSimplifiedScriptList(self):
        self.m_tree_scripts_text.DeleteAllItems()
        root = self.m_tree_scripts_text.AddRoot("items")
        event_data_root = self.m_tree_scripts_text.AppendItem(root, "event data")
        event_text_root = self.m_tree_scripts_text.AppendItem(root, "event text")
        pack = None
        for f in str(self.rom.filenames).split("\n"):
            id, filename = [x for x in f.split(" ") if x]
            id: int = int(id)
            filename: str
            if filename.endswith(".gds") or filename.endswith(".txt"):
                self.m_tree_scripts_text.AppendItem(root, filename, data=[id, 0])  # TODO: ADD Data
            if filename.endswith(".plz"):
                has_script_or_text = False
                plz = LaytonLib.filesystem.PlzFile(self.rom, id)
                for f2 in plz.filenames:
                    if f2.endswith(".gds") or f2.endswith(".txt"):
                        if not has_script_or_text:
                            has_script_or_text = True
                            if filename.startswith("ev_d"):
                                pack = self.m_tree_scripts_text.AppendItem(event_data_root, filename)
                            elif filename.startswith("ev_t"):
                                pack = self.m_tree_scripts_text.AppendItem(event_text_root, filename)
                            else:
                                pack = self.m_tree_scripts_text.AppendItem(root, filename)
                        self.m_tree_scripts_text.AppendItem(pack, f2, data=[plz.idOf(f2), id])

    def m_tree_scripts_textOnTreeSelChanged(self, event):
        data = self.m_tree_scripts_text.GetItemData(self.m_tree_scripts_text.GetSelection())
        if not data:
            return

        file_id, pack_id = data
        self.selected_file = file_id
        self.selected_pack = pack_id
        if pack_id:
            plz = LaytonLib.filesystem.PlzFile(self.rom, pack_id)
            filename = plz.filenames[file_id]
            file = plz.files[file_id]
        else:
            filename = self.rom.filenames.filenameOf(file_id).split("/")[-1]
            file = self.rom.files[file_id]
        if filename.endswith(".txt"):
            text = str(file, encoding="shift_jis")
        elif filename.endswith(".gds"):
            text = LaytonLib.gds.GDSScript.from_bytes(file).to_simplified()
        else:
            return
        self.m_textCtrl8.Clear()
        self.m_textCtrl8.WriteText(text)

    def m_button_extr_textOnButtonClick(self, event):
        if self.selected_pack:
            plz = LaytonLib.filesystem.PlzFile(self.rom, self.selected_pack)
            filename = plz.filenames[self.selected_file]
            file_data = plz.files[self.selected_file]
        else:
            filename = self.rom.filenames.filenameOf(self.selected_file).split("/")[-1]
            file_data = self.rom.files[self.selected_file]

        if filename.endswith(".gds"):
            with wx.FileDialog(self, "Save Script", style=wx.FD_SAVE,
                               wildcard="GDS scripts (*.gds)|*.gds;All FIles") as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return
                pathname = fileDialog.GetPath()
                with open(pathname, "wb+") as file:
                    file.write(file_data)

        if filename.endswith(".txt"):
            with wx.FileDialog(self, "Save text", style=wx.FD_SAVE,
                               wildcard="Text file (*.txt)|*.txt;All FIles") as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return
                pathname = fileDialog.GetPath()
                with open(pathname, "wb+") as file:
                    file.write(file_data)

    def m_button_repl_textOnButtonClick(self, event):
        with wx.FileDialog(self, "Replace File", style=wx.FD_OPEN) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'rb') as file:
                    if self.selected_pack:
                        plz = LaytonLib.filesystem.PlzFile(self.rom, self.selected_pack)
                        plz.files[self.selected_file] = file.read()
                        plz.save()

                    else:
                        self.rom.files[self.selected_file] = file.read()

            except IOError:
                return
        self.m_tree_scripts_textOnTreeSelChanged(None)

    def m_button_revert_textOnButtonClick(self, event):
        self.m_tree_scripts_textOnTreeSelChanged(None)

    def m_button_save_textOnButtonClick(self, event):
        if self.selected_pack:
            plz = LaytonLib.filesystem.PlzFile(self.rom, self.selected_pack)
            filename = plz.filenames[self.selected_file]
        else:
            filename = self.rom.filenames.filenameOf(self.selected_file).split("/")[-1]

        if filename.endswith(".txt"):
            if self.selected_pack:
                plz = LaytonLib.filesystem.PlzFile(self.rom, self.selected_pack)
                plz.files[self.selected_file] = self.m_textCtrl8.GetValue()
                plz.save()
            else:
                self.rom.files[self.selected_file] = self.m_textCtrl8.GetValue()
        if filename.endswith(".gds"):
            if self.selected_pack:
                plz = LaytonLib.filesystem.PlzFile(self.rom, self.selected_pack)
                plz.files[self.selected_file] = \
                    LaytonLib.gds.GDSScript.from_simplified(self.m_textCtrl8.GetValue()).to_bytes()
                plz.save()
            else:
                self.rom.files[self.selected_file] = \
                    LaytonLib.gds.GDSScript.from_simplified(self.m_textCtrl8.GetValue()).to_bytes()

    # Puzzles

    def OnMenuBaseDataEdit(self, event):
        if self.rom is None:
            return
        base_edit = PuzzleBaseDataEditor(self)
        base_edit.Show(True)

    def OnMenuPuzzleMultipleChoice(self, event):
        if self.rom is None:
            return
        multiple_choice = PuzzleMultipleChoice(self)
        multiple_choice.Show(True)

    def OnMenuPuzzleInput(self, event):
        if self.rom is None:
            return
        input_editor = PuzzleInputEditor(self)
        input_editor.Show(True)


class ImageEdit(GUI.generated.ImageEdit.ImageEdit):
    def __init__(self, parent: MainFrame, base_image_file):
        super().__init__(parent)
        self.base_image_file: LaytonLib.images.ani.AniFile = base_image_file
        self.imageIndex = 0

        self.update_previewimage()
        self.m_staticText5.SetLabel(f"1/{len(self.base_image_file.images)}")  # Frame Index
        self.m_staticText9.SetLabel(f"ID: {self.base_image_file.id} | {hex(self.base_image_file.id)}")  # File ID
        self.m_staticText11.SetLabel(self.base_image_file.name)  # File Name
        self.m_staticText7.SetLabel(f"Colordepth: {self.base_image_file.colordepth}bit")  # Colordepth

        self.m_text_child_image.SetLabel(f"{self.base_image_file.child_image}")

        # The Animations Part
        self.animationIndex = 0
        self.m_staticText51.SetLabel(f"1/{len(self.base_image_file.animations)}")  # Frame Index
        self.m_textCtrl1.SetLabel(self.base_image_file.animations[0].name)
        self.m_spin_child_img_x.SetMax(255)
        self.m_spin_child_img_y.SetMax(255)
        self.m_spin_child_img_id.SetMax(255)

        self.m_spin_child_img_x.SetValue(f"{self.base_image_file.animations[0].child_spr_x}")
        self.m_spin_child_img_y.SetValue(f"{self.base_image_file.animations[0].child_spr_y}")
        self.m_spin_child_img_id.SetValue(f"{self.base_image_file.animations[0].child_spr_index}")

        self.child_image_file = None
        if self.base_image_file.child_image:
            # search for childimage id
            rom: NintendoDSRom = parent.rom
            for l in str(rom.filenames["data_lt2/ani/"]).split("\n"):
                if l.endswith(self.base_image_file.child_image.replace("ani", "arc")):
                    self.child_image_file = LaytonLib.images.ani.AniFile(rom, int(l[:4]))

        # noinspection PyUnresolvedReferences
        self.m_propertyGrid_vars.SetFont(wx.Font(8, wx.TELETYPE, wx.FONTSTYLE_NORMAL,
                                                 wx.FONTWEIGHT_NORMAL))
        for i in range(len(self.base_image_file.variables)):
            label = self.base_image_file.variables[i].label
            values = [str(hexencoder(self.base_image_file.variables[i].params[x])[0], "ascii") for x in range(8)]
            value = " ".join(values)
            self.m_propertyGrid_vars.Append(pg.StringProperty(label, f"Var{i}", value=value))

        self.animationFrameIndex = 0
        self.main_image = wx.Bitmap(0, 0)
        self.child_image = wx.Bitmap(0, 0)
        self.update_animation_data()
        self.update_animation_previewimage()

    # Helper function to swap the previouw image
    def update_previewimage(self):
        image = self.base_image_file.frame_to_PIL(self.imageIndex)

        # Create a the full sized image
        fullimage = imgl.new("RGBA", (258, 194))

        # Paste it onto the full sized image
        fullimage.paste(image, (1, 1))
        edit = fullimage.load()
        for i in range(258):
            edit[i, 0] = (0, 0, 0, 255)
            edit[i, -1] = (0, 0, 0, 255)
        for i in range(1, 193):
            edit[0, i] = (0, 0, 0, 255)
            edit[-1, -i] = (0, 0, 0, 255)

        # Temporarely save it as a file to load it in wx
        fullimage.save("temp.bmp")
        wximage = wx.Image("temp.bmp")
        remove("temp.bmp")

        self.m_previewImage.SetBitmap(wximage.ConvertToBitmap())

    def OnButtonClickNextImage(self, event):
        if len(self.base_image_file.images) < 2:
            return
        self.imageIndex += 1
        if self.imageIndex >= len(self.base_image_file.images):
            self.imageIndex = 0
        self.m_staticText5.SetLabel(f"{self.imageIndex + 1}/{len(self.base_image_file.images)}")
        self.update_previewimage()

    def OnButtonClickPreviousImage(self, event):
        if len(self.base_image_file.images) < 2:
            return
        self.imageIndex -= 1
        if self.imageIndex < 0:
            self.imageIndex = len(self.base_image_file.images) - 1
        self.m_staticText5.SetLabel(f"{self.imageIndex + 1}/{len(self.base_image_file.images)}")
        self.update_previewimage()

    def OnButtonClickReplNoPal(self, event):
        with wx.FileDialog(self, "Choose Image", style=wx.FD_OPEN, wildcard="PNG files (*.png)\
                               |*.png;JPG files (*.jpg)|*.jpg;BMP files (*.bmp)|*.bmp;All FIles") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            img = imgl.open(pathname)
            self.base_image_file.frame_from_PIL_nopalswap(self.imageIndex, img)
            self.base_image_file.save()
        self.update_previewimage()

    def OnButtonClickReplAddPal(self, event):
        with wx.FileDialog(self, "Choose Image", style=wx.FD_OPEN, wildcard="PNG files (*.png)\
                               |*.png;JPG files (*.jpg)|*.jpg;BMP files (*.bmp)|*.bmp;All FIles") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            img = imgl.open(pathname)
            self.base_image_file.frame_from_PIL_addpal(self.imageIndex, img)
            self.base_image_file.save()
        self.update_previewimage()

    def OnButtonClickExport(self, event):
        with wx.FileDialog(self, "Save Image", style=wx.FD_SAVE, wildcard="PNG files (*.png)\
                        |*.png;JPG files (*.jpg)|*.jpg;BMP files (*.bmp)|*.bmp;All FIles") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            img = self.base_image_file.images[self.imageIndex - 1].to_PIL()
            img.save(pathname)

    def OnButtonClickSwapColorDepth(self, event):
        if self.base_image_file.colordepth == 4:
            # For four bit we don't have to change anything but the colordepth itself
            self.base_image_file.colordepth = 8
        else:
            # From 8 to 4 requires quantizing the image to 16 colors.
            # It uses a hacky selution of reimporting one of the images
            self.base_image_file.colordepth = 4
            self.base_image_file.frame_from_PIL_addpal(0, self.base_image_file.frame_to_PIL(0))
            self.base_image_file.save()
            self.update_previewimage()
        self.m_staticText7.SetLabel(f"Colordepth: {self.base_image_file.colordepth}bit")  # Colordepth

    def OnButtonClickAddImage(self, event):
        new_image = LaytonLib.images.ani.Image(self.base_image_file.palette)
        with wx.FileDialog(self, "Choose Image", style=wx.FD_OPEN, wildcard="PNG files (*.png)\
                               |*.png;JPG files (*.jpg)|*.jpg;BMP files (*.bmp)|*.bmp;All FIles") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
        new_image.from_PIL(imgl.open(pathname))
        self.base_image_file.images.insert(self.imageIndex + 1, new_image)
        self.imageIndex += 1
        self.m_staticText5.SetLabel(f"{self.imageIndex + 1}/{len(self.base_image_file.images)}")
        self.update_previewimage()

    def OnButtonClickRemoveImage(self, event):
        if len(self.base_image_file.images) == 1:
            return
        del self.base_image_file.images[self.imageIndex]
        self.imageIndex -= 1
        if self.imageIndex < 0:
            self.imageIndex = len(self.base_image_file.images) - 1

    def OnButtonClickAddImageAddPal(self, event):
        new_image = LaytonLib.images.ani.Image(self.base_image_file.palette)
        with wx.FileDialog(self, "Choose Image", style=wx.FD_OPEN, wildcard="PNG files (*.png)\
                                       |*.png;JPG files (*.jpg)|*.jpg;BMP files (*.bmp)|*.bmp;All FIles") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
        new_image.from_PIL(imgl.open(pathname))
        self.base_image_file.images.insert(self.imageIndex + 1, new_image)
        self.base_image_file.frame_from_PIL_addpal(self.imageIndex + 1, imgl.open(pathname))
        self.imageIndex += 1
        self.m_staticText5.SetLabel(f"{self.imageIndex + 1}/{len(self.base_image_file.images)}")
        self.update_previewimage()

    def OnButtonClickExportAll(self, event):
        with wx.DirDialog(self, "Choose Folder", style=wx.FD_OPEN) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
        for i in range(len(self.base_image_file.images)):
            image = self.base_image_file.images[i]
            pil_image: imgl.Image = image.to_PIL()
            filename = self.base_image_file.name.split('/')[-1]
            pil_image.save(join(pathname, f"{filename}_{i + 1}.png"))

    def OnButtonClickNextAnimation(self, event):
        self.animationIndex += 1
        if self.animationIndex >= len(self.base_image_file.animations):
            self.animationIndex = 0
        self.m_staticText51.SetLabel(f"{self.animationIndex + 1}/{len(self.base_image_file.animations)}")  # Frame Index
        self.m_textCtrl1.SetLabel(self.base_image_file.animations[self.animationIndex].name)
        self.m_spin_child_img_x.SetValue(f"{self.base_image_file.animations[self.animationIndex].child_spr_x}")
        self.m_spin_child_img_y.SetValue(f"{self.base_image_file.animations[self.animationIndex].child_spr_y}")
        self.m_spin_child_img_id.SetValue(f"{self.base_image_file.animations[self.animationIndex].child_spr_index}")

        self.animationFrameIndex = 0
        self.update_animation_data()
        self.update_animation_previewimage()

    def OnButtonClickPreviousAnimation(self, event):
        self.animationIndex -= 1
        if self.animationIndex < 0:
            self.animationIndex = len(self.base_image_file.animations) - 1
        self.m_staticText51.SetLabel(f"{self.animationIndex + 1}/{len(self.base_image_file.animations)}")  # Frame Index
        self.m_textCtrl1.SetLabel(self.base_image_file.animations[self.animationIndex].name)
        self.m_spin_child_img_x.SetValue(f"{self.base_image_file.animations[self.animationIndex].child_spr_x}")
        self.m_spin_child_img_y.SetValue(f"{self.base_image_file.animations[self.animationIndex].child_spr_y}")
        self.m_spin_child_img_id.SetValue(f"{self.base_image_file.animations[self.animationIndex].child_spr_index}")

        self.animationFrameIndex = 0
        self.update_animation_data()
        self.update_animation_previewimage()

    def m_textCtrl1OnTextEnter(self, event):
        animation = self.base_image_file.animations[self.animationIndex]
        animation: LaytonLib.images.ani.Animation
        animation.name = self.m_textCtrl1.GetValue()

    # Helper function to swap the previouw image of the animation editor
    def update_animation_previewimage(self):
        if len(self.base_image_file.animations[self.animationIndex].frameIDs) == 0:
            self.main_image = wx.Bitmap(0, 0)
            self.m_panel_animation_preview.Refresh()
            return
        main_index = self.base_image_file.animations[self.animationIndex].imageIndexes[self.animationFrameIndex]
        pil_image = self.base_image_file.frame_to_PIL(main_index)
        wx_image = wx.Image(*pil_image.size)
        wx_image.SetData(pil_image.convert("RGB").tobytes())
        self.main_image = wx.Bitmap(wx_image)
        if not self.child_image_file or len(self.child_image_file.animations[
                                                self.base_image_file.animations[
                                                    self.animationIndex].child_spr_index].frameIDs) == 0:
            self.child_image = wx.Bitmap(0, 0)
        else:
            child_index = self.child_image_file.animations[
                self.base_image_file.animations[self.animationIndex].child_spr_index].imageIndexes[0]
            pil_image = self.child_image_file.frame_to_PIL(child_index)
            wx_image = wx.Image(*pil_image.size)
            wx_image.SetData(pil_image.convert("RGB").tobytes())
            self.child_image = wx.Bitmap(wx_image)

        self.m_panel_animation_preview.Refresh()

    def m_panel_animation_previewOnPaint(self, event):
        dc = wx.PaintDC(self.m_panel_animation_preview)
        w, h = self.m_panel_animation_preview.GetSize()
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, w, h)
        dc.DrawBitmap(self.main_image, 1, 1)
        if self.m_checkBox_draw_child_img.GetValue():
            anim = self.base_image_file.animations[self.animationIndex]
            dc.DrawBitmap(self.child_image, anim.child_spr_x + 1, anim.child_spr_y + 1)

    def m_panel_animation_previewOnSize(self, event):
        self.m_panel_animation_preview.Refresh()

    def update_animation_data(self):
        if len(self.base_image_file.animations[self.animationIndex].frameIDs) == 0:
            self.m_staticText511.SetLabel("0/0")
            self.m_textCtrl11.SetLabel("")
            self.m_textCtrl13.SetLabel("")
            return
        animation: LaytonLib.images.ani.Animation = self.base_image_file.animations[self.animationIndex]
        self.m_staticText511.SetLabel(f"{self.animationFrameIndex + 1}/{len(animation.frameIDs)}")
        self.m_textCtrl11.SetLabel(str(animation.imageIndexes[self.animationFrameIndex]))
        self.m_textCtrl13.SetLabel(str(animation.frameDurations[self.animationFrameIndex]))
        self.m_textCtrl131.SetLabel(str(animation.frameIDs[self.animationFrameIndex]))

    def OnButtonClickNextAnimationFrame(self, event):
        if len(self.base_image_file.animations[self.animationIndex].frameIDs) == 0:
            return
        self.animationFrameIndex += 1
        if self.animationFrameIndex >= len(self.base_image_file.animations[self.animationIndex].frameIDs):
            self.animationFrameIndex = 0
        self.update_animation_data()
        self.update_animation_previewimage()

    def OnButtonClickPreviousAnimationFrame(self, event):
        animation = self.base_image_file.animations[self.animationIndex]
        if len(animation.frameIDs) == 0:
            return
        self.animationFrameIndex -= 1
        if self.animationFrameIndex < 0:
            self.animationFrameIndex = len(animation.frameIDs) - 1
        self.update_animation_data()
        self.update_animation_previewimage()

    def OnButtonClickAddAnimation(self, event):
        newanimation = LaytonLib.images.ani.Animation()
        newanimation.name = "New Animation"
        self.animationIndex += 1
        self.base_image_file.animations.insert(self.animationIndex, newanimation)
        self.update_animation_previewimage()
        self.update_animation_data()
        self.m_staticText51.SetLabel(f"{self.animationIndex + 1}/{len(self.base_image_file.animations)}")  # Frame Index
        self.m_textCtrl1.SetLabel(self.base_image_file.animations[self.animationIndex].name)
        self.m_spin_child_img_x.SetValue(f"{self.base_image_file.animations[self.animationIndex].child_spr_x}")
        self.m_spin_child_img_y.SetValue(f"{self.base_image_file.animations[self.animationIndex].child_spr_y}")
        self.m_spin_child_img_id.SetValue(f"{self.base_image_file.animations[self.animationIndex].child_spr_index}")
        self.base_image_file.save()

    def OnButtonClickRemoveAnimation(self, event):
        if self.animationIndex == 0:
            print("Can't remove this animation")
            return
        del self.base_image_file.animations[self.animationIndex]
        self.update_animation_previewimage()
        self.update_animation_data()
        self.m_staticText51.SetLabel(f"{self.animationIndex + 1}/{len(self.base_image_file.animations)}")  # Frame Index
        self.m_textCtrl1.SetLabel(self.base_image_file.animations[self.animationIndex].name)
        self.m_spin_child_img_x.SetValue(f"{self.base_image_file.animations[self.animationIndex].child_spr_x}")
        self.m_spin_child_img_y.SetValue(f"{self.base_image_file.animations[self.animationIndex].child_spr_y}")
        self.m_spin_child_img_id.SetValue(f"{self.base_image_file.animations[self.animationIndex].child_spr_index}")
        self.base_image_file.save()

    def OnButtonClickAddAFrame(self, event):
        animation: LaytonLib.images.ani.Animation = self.base_image_file.animations[self.animationIndex]
        self.animationFrameIndex += 1
        animation.imageIndexes.insert(self.animationFrameIndex, 0)
        animation.frameDurations.insert(self.animationFrameIndex, 60)
        animation.frameIDs.insert(self.animationFrameIndex, self.animationFrameIndex)
        self.update_animation_previewimage()
        self.update_animation_data()
        self.base_image_file.save()

    def OnButtonClickRemoveAFrame(self, event):
        animation: LaytonLib.images.ani.Animation = self.base_image_file.animations[self.animationIndex]
        animation.imageIndexes.pop(self.animationFrameIndex)
        animation.frameDurations.pop(self.animationFrameIndex)
        animation.frameIDs.pop(self.animationFrameIndex)
        self.update_animation_previewimage()
        self.update_animation_data()
        self.base_image_file.save()

    def OnTextEnterFrameDur(self, event):
        animation: LaytonLib.images.ani.Animation = self.base_image_file.animations[self.animationIndex]
        animation.frameDurations[self.animationFrameIndex] = int(self.m_textCtrl13.GetValue())

    def OnTextEnterFrameID(self, event):
        animation: LaytonLib.images.ani.Animation = self.base_image_file.animations[self.animationIndex]
        animation.frameIDs[self.animationFrameIndex] = int(self.m_textCtrl131.GetValue())

    def OnTextEnterImgID(self, event):
        animation: LaytonLib.images.ani.Animation = self.base_image_file.animations[self.animationIndex]
        animation.imageIndexes[self.animationFrameIndex] = int(self.m_textCtrl11.GetValue())
        self.update_animation_previewimage()

    def m_text_child_imageOnTextEnter(self, event):
        self.base_image_file.child_image = self.m_text_child_image.GetValue()
        self.base_image_file.save()
        if self.m_checkBox_draw_child_img.GetValue():
            self.update_animation_previewimage()

    def m_spin_child_img_xOnSpinCtrl(self, event):
        self.base_image_file.animations[self.animationIndex].child_spr_x = int(self.m_spin_child_img_x.GetValue())
        # self.base_image_file.save()
        if self.m_checkBox_draw_child_img.GetValue():
            self.m_panel_animation_preview.Refresh()

    def m_spin_child_img_yOnSpinCtrl(self, event):
        self.base_image_file.animations[self.animationIndex].child_spr_y = int(self.m_spin_child_img_y.GetValue())
        # self.base_image_file.save()
        if self.m_checkBox_draw_child_img.GetValue():
            self.m_panel_animation_preview.Refresh()

    def m_spin_child_img_idOnSpinCtrl(self, event):
        self.base_image_file.animations[self.animationIndex].child_spr_index = int(self.m_spin_child_img_id.GetValue())
        # self.base_image_file.save()
        if self.m_checkBox_draw_child_img.GetValue():
            self.update_animation_previewimage()

    def m_button_save_child_img_posOnButtonClick(self, event):
        self.base_image_file.save()

    def m_propertyGrid_varsOnPropertyGridChanged(self, event):
        for i in range(16):
            spaceless = self.m_propertyGrid_vars.GetPropertyByName(f"Var{i}").GetValue().replace(" ", "")
            for part, offset in enumerate(range(0, 32, 4)):
                self.base_image_file.variables[i].params[part] = hexdecoder(spaceless[offset:offset + 4])[0]

    def m_checkBox_draw_child_imgOnCheckBox(self, event):
        self.update_animation_previewimage()


class PuzzleBaseDataEditor(GUI.generated.PuzzleBaseDataEditor.PuzzleBaseDataEditor):
    def __init__(self, parent: MainFrame):
        super().__init__(parent)
        self.parent = parent
        self.puzzle_data = pzd.PuzzleData(rom=self.parent.rom)

    def OnButtonLoadPuzzle(self, event):
        puzzle_id = str(self.puzz_id_text.Value)
        if puzzle_id.startswith("0x"):
            puzzle_id = int(puzzle_id[2:], 16)
        else:
            puzzle_id = int(puzzle_id)

        self.puzzle_data.set_internal_id(puzzle_id)
        if not self.puzzle_data.load_from_rom():
            error_msg = "Error loading puzzle with id {} from rom".format(self.puzzle_data.internal_id)
            error_dialog = wx.MessageDialog(self, error_msg, style=wx.ICON_ERROR | wx.OK)
            error_dialog.ShowModal()
            return

        self.puzz_txt_input.Value = self.puzzle_data.text
        self.correct_input.Value = self.puzzle_data.correct_answer
        self.incorrect_input.Value = self.puzzle_data.incorrect_answer
        self.hint1_input.Value = self.puzzle_data.hint1
        self.hint2_input.Value = self.puzzle_data.hint2
        self.hint3_input.Value = self.puzzle_data.hint3
        self.puzz_title_input.Value = self.puzzle_data.title
        self.puzzle_type_choice.Selection = self.puzzle_data.type
        self.puzzle_num_display.LabelText = str(self.puzzle_data.number)

        self.puzzle_data.bg.img.save("temp2.bmp")
        wx_img = wx.Image("temp2.bmp")
        remove("temp2.bmp")
        self.puzz_display.SetBitmap(wx_img.ConvertToBitmap())

    def OnButtonSavePuzzle(self, event):
        puzzle_id = str(self.puzz_id_text.Value)
        if puzzle_id.startswith("0x"):
            puzzle_id = int(puzzle_id[2:], 16)
        else:
            puzzle_id = int(puzzle_id)

        self.puzzle_data.set_internal_id(puzzle_id)

        try:
            self.puzzle_data.text = auto_newline(str(self.puzz_txt_input.Value), 42).encode("ascii")
            self.puzzle_data.correct_answer = auto_newline(str(self.correct_input.Value), 38).encode("ascii")
            self.puzzle_data.incorrect_answer = auto_newline(str(self.incorrect_input.Value), 38).encode("ascii")
            self.puzzle_data.hint1 = auto_newline(str(self.hint1_input.Value), 38).encode("ascii")
            self.puzzle_data.hint2 = auto_newline(str(self.hint2_input.Value), 38).encode("ascii")
            self.puzzle_data.hint3 = auto_newline(str(self.hint3_input.Value), 38).encode("ascii")
            self.puzzle_data.title = auto_newline(str(self.puzz_title_input.Value), 38).encode("ascii")
            self.puzzle_data.type = self.puzzle_type_choice.Selection
        except UnicodeEncodeError:
            error_unicode = wx.MessageDialog(self, "There can't be unicode characters in the texts",
                                             style = wx.ICON_ERROR | wx.OK)
            error_unicode.ShowModal()
            return

        self.puzzle_data.save_to_rom()

        successful = wx.MessageDialog(self, "Saved successfully")
        successful.ShowModal()


class PuzzleMultipleChoice(GUI.generated.PuzzleMultipleChoice.PuzzleMultipleChoice):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.puzzle_bg_original = None
        self.puzzle_data = pzd.PuzzleData(rom=parent.rom)

        self.current_selection = -1

    def load_puzzle_bg(self):
        self.puzzle_bg_original = self.puzzle_data.bg.img.copy()

        self.update_puzzle_preview(0)

    def OnButtonGDSLoad(self, event):
        puzzle_id = int(self.gds_load_input.Value)
        self.puzzle_data.set_internal_id(puzzle_id)
        if not self.puzzle_data.load_from_rom():
            gds_error = wx.MessageDialog(self, "Can't load puzzle (not found)", style=wx.ICON_ERROR|wx.OK)
            gds_error.ShowModal()
            return
        if not self.puzzle_data.load_gds():
            gds_error = wx.MessageDialog(self, "Can't load gds (not found)", style=wx.ICON_ERROR|wx.OK)
            gds_error.ShowModal()
            return
        if self.puzzle_data.type != pzd.PuzzleData.MULTIPLE_CHOICE:
            gds_warning = wx.MessageDialog(self, "Warning: loading puzzle which is not of type multiple choice",
                                           style=wx.ICON_WARNING | wx.OK)
            gds_warning.ShowModal()

        self.current_selection = -1

        self.load_puzzle_bg()
        self.update_tree()
        self.update_puzzle_preview(0)

    def OnButtonGDSSave(self, event):
        self.save_current_editing_data()
        self.puzzle_data.set_internal_id(int(self.gds_save_input.Value))
        if not self.puzzle_data.save_gds():
            gds_error = wx.MessageDialog(self, "Can't save gds (not found)", style=wx.ICON_ERROR|wx.OK)
            gds_error.ShowModal()
            return

        successful = wx.MessageDialog(self, "Saved successfully")
        successful.ShowModal()

    def OnButtonUpdatePuzzlePreview(self, event):
        self.update_puzzle_preview(0)

    def update_puzzle_preview(self, anim_num):
        self.save_current_editing_data()
        if self.puzzle_bg_original is None:
            return
        puzzle_bg = self.puzzle_bg_original.copy()  # type: imgl.Image

        for element in self.puzzle_data.gds.commands:
            if element.command != 0x14:
                continue
            freebutton_txt = str(element.params[2])
            freebutton_txt = freebutton_txt.replace(".spr", ".arc")
            freebutton_id = self.parent.rom.filenames.idOf("data_lt2/ani/nazo/freebutton/{}".format(freebutton_txt))
            if not freebutton_id:
                continue
            freebutton = LaytonLib.images.ani.AniFile(self.parent.rom, freebutton_id)
            freebutton_pil = freebutton.frame_to_PIL(anim_num)  # type: imgl.Image
            freebutton_pil.putalpha(255)

            for i in range(freebutton_pil.width):
                for j in range(freebutton_pil.height):
                    color = freebutton_pil.getpixel((i, j))
                    if color[1] == 248:
                        freebutton_pil.putpixel((i, j), (0, 0, 0, 0))

            freebutton_pil.load()

            puzzle_bg.paste(freebutton_pil, box=(element.params[0], element.params[1]),
                            mask=freebutton_pil.split()[3])

        self.puzzle_preview.SetBitmap(self.PIL2wx(puzzle_bg))

    def update_tree(self):
        self.buttons_tree.DeleteAllItems()
        root = self.buttons_tree.AddRoot("gds_buttons")
        element_count = 0

        for element in self.puzzle_data.gds.commands:
            if element.command != 0x14:
                continue
            new_item = self.buttons_tree.AppendItem(root, "button{}".format(element_count))
            self.buttons_tree.SetItemData(new_item, self.puzzle_data.gds.commands.index(element))
            element_count += 1

    def ObjTreeSelChanged(self, event):
        self.save_current_editing_data()
        selected_object = self.buttons_tree.GetItemData(self.buttons_tree.GetSelection())
        self.current_selection = selected_object

        self.edit_gds_pannel.Show(True)
        if self.current_selection >= len(self.puzzle_data.gds.commands):
            self.current_selection = -1
            return
        selected_object_gds = self.puzzle_data.gds.commands[selected_object]

        self.x_input.Value = str(selected_object_gds.params[0])
        self.y_input.Value = str(selected_object_gds.params[1])
        self.freebutton_input.Value = str(selected_object_gds.params[2])
        self.is_correct_checkbox.Value = selected_object_gds.params[3] > 0
        self.sfx_input.Value = str(selected_object_gds.params[4])

    def save_current_editing_data(self):
        if self.current_selection == -1:
            return
        selected_object_gds = self.puzzle_data.gds.commands[self.current_selection]
        selected_object_gds.params[0] = int(self.x_input.Value)
        selected_object_gds.params[1] = int(self.y_input.Value)
        selected_object_gds.params[2] = str(self.freebutton_input.Value)
        selected_object_gds.params[3] = int(self.is_correct_checkbox.Value)
        selected_object_gds.params[4] = int(self.sfx_input.Value)

    def OnButtonNew(self, event):
        add_index = len(self.puzzle_data.gds.commands)
        self.puzzle_data.gds.commands.insert(add_index,
                                             LaytonLib.gds.GDSCommand(0x14, [0, 0, "freebutton_m.spr", 0, 0]))
        self.current_selection = -1
        self.update_tree()

    def OnButtonDelete(self, event):
        add_index = self.current_selection
        if add_index == -1:
            return
        self.puzzle_data.gds.commands = self.puzzle_data.gds.commands[:add_index] +\
                                        self.puzzle_data.gds.commands[add_index + 1:]
        self.current_selection = -1
        self.update_tree()

    def PIL2wx(self, image):
        width, height = image.size
        return wx.Bitmap.FromBuffer(width, height, image.tobytes())


class PuzzleInputEditor(GUI.generated.PuzzleInputEditor.PuzzleInputEditor):
    def __init__(self, parent):
        super().__init__(parent)
        self.puzzle_data = pzd.PuzzleData(rom=parent.rom)

    def update_puzzle_preview(self):
        self.puzzle_preview.SetBitmap(self.PIL2wx(self.puzzle_data.bg.img))
        input_bg_path: str = self.input_bg_inp.Value
        input_bg_path = input_bg_path.replace("?", "en")
        input_bg_path = input_bg_path.replace("bgx", "arc")
        bg_id = self.puzzle_data.rom.filenames.idOf("data_lt2/bg/nazo/drawinput/{}".format(input_bg_path))
        if bg_id is None:
            input_bg = LaytonLib.images.bg.Bg()
            print(f"Warning: input bg {input_bg_path} not found")
        else:
            input_bg = LaytonLib.images.bg.BgFile(self.puzzle_data.rom, bg_id)
        self.input_bg_preview.SetBitmap(self.PIL2wx(input_bg.img))

    def load_values(self):
        for cmd in self.puzzle_data.gds.commands:  # type: LaytonLib.gds.GDSCommand
            if cmd.command == 0x43:
                self.input_bg_inp.Value = cmd.params[0]
            elif cmd.command == 0x42:
                self.answer_inp.Value = cmd.params[1]
            elif cmd.command == 0x41:
                self.type_of_input_inp.Value = str(cmd.params[3])

    def save_values(self):
        # TODO: Add and reverse engineer the other parameters
        self.puzzle_data.gds = LaytonLib.gds.GDSScript()
        self.puzzle_data.gds.commands.append(LaytonLib.gds.GDSCommand(0x43, [str(self.input_bg_inp.Value)]))
        self.puzzle_data.gds.commands.append(LaytonLib.gds.GDSCommand(0x41, [0, 0, 0,
                                                                             int(self.type_of_input_inp.Value)]))
        self.puzzle_data.gds.commands.append(LaytonLib.gds.GDSCommand(0x42, [0, str(self.answer_inp.Value)]))

    def OnButtonGDSLoad(self, event):
        puzzle_id = int(self.gds_load_input.Value)
        self.puzzle_data.set_internal_id(puzzle_id)
        if not self.puzzle_data.load_from_rom():
            gds_error = wx.MessageDialog(self, "Can't load puzzle (not found)", style=wx.ICON_ERROR | wx.OK)
            gds_error.ShowModal()
            return
        if not self.puzzle_data.load_gds():
            gds_error = wx.MessageDialog(self, "Can't load gds (not found)", style=wx.ICON_ERROR | wx.OK)
            gds_error.ShowModal()
            return
        if self.puzzle_data.type not in pzd.PuzzleData.INPUTS:
            gds_warning = wx.MessageDialog(self, "Warning: loading puzzle which is not of type input",
                                           style=wx.ICON_WARNING | wx.OK)
            gds_warning.ShowModal()

        self.input_bg_inp.Value = ""
        self.answer_inp.Value = ""
        self.type_of_input_inp.Value = ""
        self.load_values()
        self.update_puzzle_preview()

    def OnButtonGDSSave(self, event):
        self.save_values()
        self.puzzle_data.set_internal_id(int(self.gds_save_input.Value))
        if not self.puzzle_data.save_gds():
            gds_error = wx.MessageDialog(self, "Can't save gds (not found)", style=wx.ICON_ERROR | wx.OK)
            gds_error.ShowModal()
            return

        successful = wx.MessageDialog(self, "Saved successfully")
        successful.ShowModal()

    def OnButtonUpdatePuzzlePreview(self, event):
        self.update_puzzle_preview()

    def PIL2wx(self, image):
        width, height = image.size
        return wx.Bitmap.FromBuffer(width, height, image.tobytes())


class LaytonEditor(wx.App):
    def __init__(self):
        super().__init__()
        self.mainFrame: MainFrame

    def OnInit(self):
        self.mainFrame = MainFrame(None)
        self.mainFrame.Show(True)
        return True
