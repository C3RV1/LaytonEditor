import GUI.generated as gen
import LaytonLib
from ndspy.rom import NintendoDSRom
from ndspy.fnt import Folder
import wx
from os import remove
import PIL.Image as imgl


class MainFrame(gen.MainFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.rom = None
        self.selected_image = 1
        self.selected_imagefile = None
        self.location = ""

    def OnMenuSelectionOpen(self, event):
        self.openFile()

    def openFile(self):
        with wx.FileDialog(self, "Open NDS ROM", wildcard="NDS files (*.nds)|*.nds",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.location = pathname
            try:
                with open(pathname, 'rb') as file:
                    self.rom = NintendoDSRom(file.read())

            except IOError:
                raise IOError("Unable to load rom.")
        self.updateAniImageList()

    def OnMenuSelectionSave(self, event):
        self.saveFile()

    def OnMenuSelectionSaveAs(self, event):
        with wx.FileDialog(self, "Save NDS ROM", wildcard="NDS files (*.nds)|*.nds",
                           style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

                # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.location = pathname
        self.saveFile()

    def saveFile(self):
        if not self.location:
            return
        with open(self.location, "wb+") as file:
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

    def OnButtonClickNextImage( self, event ):
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
        id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not id:
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

    def OnButtonClickExtractDecom( self, event ):
        id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not id:
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

    def OnButtonClickReplaceDecom( self, event ):
        id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not id:
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

    def OnButtonClickSaveImage( self, event ):
        id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not id:
            return
        with wx.FileDialog(self, "Save Image", style=wx.FD_SAVE, wildcard="PNG files (*.png)\
                |*.png;JPG files (*.jpg)|*.jpg;BMP files (*.bmp)|*.bmp;All FIles") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            img = self.selected_imagefile.images[self.selected_image-1].to_PIL()
            img.save(pathname)

    def OnButtonClickReplaceImage( self, event ):
        id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not id:
            return
        with wx.FileDialog(self, "Choose Image", style=wx.FD_OPEN, wildcard="PNG files (*.png)\
                        |*.png;JPG files (*.jpg)|*.jpg;BMP files (*.bmp)|*.bmp;All FIles") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            img = imgl.open(pathname)
            self.selected_imagefile.frame_from_PIL_nopalswap(self.selected_image - 1, img)
            self.selected_imagefile.save()
        self.swap_preview_image(self.selected_imagefile.frame_to_PIL(self.selected_image-1))

    def OnButtonClickReplaceImageAddPall( self, event ):
        id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not id:
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


class LaytonEditor(wx.App):
    def __init__(self):
        super().__init__()
        self.mainFrame = None

    def OnInit(self):
        self.mainFrame = MainFrame(None)
        self.mainFrame.Show(True)
        return True
