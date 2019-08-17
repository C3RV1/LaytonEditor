import wx

import generated
from laytonlib import NDS, Folder
from sys import exit
import laytonlib.images.ani as ani
from os import remove
import PIL.Image as IMG


class MainFrame(generated.MainFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.nds = None
        self.selected_image = 1
        self.selected_imagefile = None
        self.openFile()
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
                    self.nds = NDS(file.read())

            except IOError:
                exit(1)
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
            file.write(self.nds.save())

    def updateAniImageList(self):
        folder: Folder = self.nds.filenames["data_lt2/ani"]
        self.tree_imagefiles.DeleteAllItems()
        root = self.tree_imagefiles.AddRoot("ani")
        for img in folder.files:
            i = self.tree_imagefiles.AppendItem(root, img)
            self.tree_imagefiles.SetItemData(i, folder.idOf(img))
        for f in folder.folders:
            self.addFolder(root, f)

    def addFolder(self, root, folder):
        nroot = self.tree_imagefiles.AppendItem(root, folder[0])
        fol = folder[1]
        for i in fol.files:
            j = self.tree_imagefiles.AppendItem(nroot, i)
            self.tree_imagefiles.SetItemData(j, fol.idOf(i))
        for f in fol.folders:
            self.addFolder(nroot, f)

    def tree_imagefilesOnTreeSelChanged(self, event):
        id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not id:
            return

        file = self.nds.files[id]
        animage = ani.Arc()
        animage.import_arc(file)
        self.selected_imagefile = animage
        fullimage = IMG.new("RGBA", (256, 192))
        image = animage.export_frame_to_image(0)
        fullimage.paste(image)
        fullimage.save("temp.bmp")
        wximage = wx.Image("temp.bmp")
        remove("temp.bmp")
        self.previewImage.SetBitmap(wximage.ConvertToBitmap())
        self.m_staticText_Colordepth.SetLabel(f"Colordepth: {animage.colordepth}bit")
        self.m_staticText_imagename.SetLabel(self.nds.filenames[id])
        self.m_staticText_imageID.SetLabel(f"ID: {id}")

        self.selected_image = 1
        self.m_staticText_currentimage.SetLabel(f"{self.selected_image}/{len(animage.images)}")

    def OnButtonClickPreviousImage(self, event):
        if len(self.selected_imagefile.images) < 2:
            return
        self.selected_image -= 1
        if self.selected_image < 1:
            self.selected_image = len(self.selected_imagefile.images)
        self.m_staticText_currentimage.SetLabel(f"{self.selected_image}/{len(self.selected_imagefile.images)}")
        fullimage = IMG.new("RGBA", (256, 192))
        image = self.selected_imagefile.export_frame_to_image(self.selected_image - 1)
        fullimage.paste(image)
        fullimage.save("temp.bmp")
        wximage = wx.Image("temp.bmp")
        remove("temp.bmp")
        self.previewImage.SetBitmap(wximage.ConvertToBitmap())

    def OnButtonClickNextImage(self, event):
        if len(self.selected_imagefile.images) < 2:
            return
        self.selected_image += 1
        if self.selected_image > len(self.selected_imagefile.images):
            self.selected_image = 1
        self.m_staticText_currentimage.SetLabel(f"{self.selected_image}/{len(self.selected_imagefile.images)}")
        fullimage = IMG.new("RGBA", (256, 192))
        image = self.selected_imagefile.export_frame_to_image(self.selected_image - 1)
        fullimage.paste(image)
        fullimage.save("temp.bmp")
        wximage = wx.Image("temp.bmp")
        remove("temp.bmp")
        self.previewImage.SetBitmap(wximage.ConvertToBitmap())

    def OnButtonClickExtract(self, event):
        id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not id:
            return

        with wx.FileDialog(self, "Extract File", style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'wb+') as file:
                    file.write(self.nds.files[id])
            except IOError:
                return

    def OnButtonClickExtractDecom(self, event):
        id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not id:
            return
        with wx.FileDialog(self, "Extract Decompressed File", style=wx.FD_SAVE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'wb+') as file:
                    file.write(self.selected_imagefile.export_data())
            except IOError:
                return

    def updateAfterReplace(self):
        id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not id:
            return
        self.selected_imagefile.import_arc(self.nds.files[id])
        fullimage = IMG.new("RGBA", (256, 192))
        image = self.selected_imagefile.export_frame_to_image(self.selected_image - 1)
        fullimage.paste(image)
        fullimage.save("temp.bmp")
        wximage = wx.Image("temp.bmp")
        remove("temp.bmp")
        self.previewImage.SetBitmap(wximage.ConvertToBitmap())

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
                    self.nds.files[id] = file.read()
            except IOError:
                return
        self.updateAfterReplace()

    def OnButtonClickReplaceDecom(self, event):
        id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not id:
            return
        with wx.FileDialog(self, "Replace File", style=wx.FD_OPEN) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'rb') as file:
                    self.selected_imagefile.import_data(file.read())
                    self.nds.files[id] = self.selected_imagefile.export_arc()

            except IOError:
                return
        self.updateAfterReplace()

    def OnButtonClickSaveImage(self, event):
        id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not id:
            return
        with wx.FileDialog(self, "Save Image", style=wx.FD_SAVE, wildcard="PNG files (*.png)\
        |*.png;JPG files (*.jpg)|*.jpg;BMP files (*.bmp)|*.bmp;All FIles") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            img = self.selected_imagefile.export_frame_to_image(self.selected_image-1)
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
            img = IMG.open(pathname)
            self.selected_imagefile.import_frame_to_image_nopal(self.selected_image-1, img)
            self.nds.files[id] = self.selected_imagefile.export_arc()
        self.updateAfterReplace()

    def OnButtonClickReplaceImageAddPall( self, event ):
        id = self.tree_imagefiles.GetItemData(self.tree_imagefiles.GetSelection())
        if not id:
            return
        with wx.FileDialog(self, "Choose Image", style=wx.FD_OPEN, wildcard="PNG files (*.png)\
                        |*.png;JPG files (*.jpg)|*.jpg;BMP files (*.bmp)|*.bmp;All FIles") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            img = IMG.open(pathname)
            self.selected_imagefile.import_frame_to_image(self.selected_image-1, img)
            self.nds.files[id] = self.selected_imagefile.export_arc()
        self.updateAfterReplace()

class ImageEditor(generated.ImageEdit):
    pass


class LaytonEditor(wx.App):
    def OnInit(self):
        self.mainFrame = MainFrame(None)
        self.mainFrame.Show(True)
        return True
