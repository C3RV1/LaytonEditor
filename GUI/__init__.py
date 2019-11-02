import GUI.generated as gen
import LaytonLib
from ndspy.rom import NintendoDSRom
from ndspy.fnt import Folder
import wx
from os import remove
import PIL.Image as imgl
from os.path import join
import LaytonLib.asm_patching


class MainFrame(gen.MainFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.rom = None
        self.selected_image = 1
        self.selected_imagefile = None
        self.save_location = ""

        self.arm9backup = None

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
        self.rom.arm9 = self.rom.loadArm9().save(compress=False)
        self.arm9backup = self.rom.arm9
        self.updateAniImageList()
        self.tree_imagefiles.Expand(self.tree_imagefiles.GetRootItem())

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

    # Helper function to update the list of image files
    def updateAniImageList(self):
        self.tree_imagefiles.DeleteAllItems()
        folder: Folder = self.rom.filenames["data_lt2/ani"]
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

    def OnButtonClickPatchRom( self, event ):
        print(self.arm9backup)
        setupcode_folder = self.m_textCtrl2.GetLabelText()
        gamecode_folder = self.m_textCtrl3.GetLabelText()
        arenalooffsptr = int(self.m_textCtrl31.GetLabelText(), 16)
        self.rom.arm9 = self.arm9backup
        LaytonLib.asm_patching.PatchRom(self.rom, setupcode_folder, gamecode_folder, arenalooffsptr)

class ImageEdit(generated.ImageEdit):
    def __init__(self, parent, base_image_file):
        super().__init__(parent)
        self.base_image_file: LaytonLib.images.ani.AniFile = base_image_file
        self.imageIndex = 0
        self.update_previewimage()
        self.m_staticText5.SetLabel(f"1/{len(self.base_image_file.images)}")  # Frame Index
        self.m_staticText9.SetLabel(f"ID: {self.base_image_file._id} | {hex(self.base_image_file.id)}")  # File ID
        self.m_staticText11.SetLabel(self.base_image_file.name)  # File Name
        self.m_staticText7.SetLabel(f"Colordepth: {self.base_image_file.colordepth}bit")  # Colordepth

        # The Animations Part
        self.animationIndex = 0
        self.m_staticText51.SetLabel(f"1/{len(self.base_image_file.animations)}")  # Frame Index
        self.m_textCtrl1.SetLabel(self.base_image_file.animations[0].name)

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
        anim: LaytonLib.images.ani.Animation = self.base_image_file.animations[self.animationIndex]

    def OnButtonClickPreviousAnimation(self, event):
        self.animationIndex -= 1
        if self.animationIndex < 0:
            self.animationIndex = len(self.base_image_file.animations)-1
        self.m_staticText51.SetLabel(f"{self.animationIndex + 1}/{len(self.base_image_file.animations)}")  # Frame Index
        self.m_textCtrl1.SetLabel(self.base_image_file.animations[self.animationIndex].name)

    def OnButtonClickSaveAnimationName( self, event ):
        animation = self.base_image_file.animations[self.animationIndex]
        animation: LaytonLib.images.ani.Animation
        animation.name = self.m_textCtrl1.GetValue()
        print(self.m_textCtrl1.GetValue())

class LaytonEditor(wx.App):
    def __init__(self):
        super().__init__()
        self.mainFrame: MainFrame

    def OnInit(self):
        self.mainFrame = MainFrame(None)
        self.mainFrame.Show(True)
        return True
