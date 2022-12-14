import os

from .Filesystem import FolderNode, AssetNodeBasename, FilesystemCategory
from formats.graphics.bg import BGImage
from PySide6 import QtCore, QtWidgets
from typing import Callable, List, Tuple, Union
from PIL import Image


class BackgroundAsset(AssetNodeBasename):
    def get_bg(self) -> BGImage:
        return BGImage(self.path, rom=self.rom)


class BackgroundsCategory(FilesystemCategory):
    def __init__(self):
        super(BackgroundsCategory, self).__init__()
        self.name = "Backgrounds"

    def reset_file_system(self):
        self._root = FolderNode(self, "/data_lt2/bg", self.rom.filenames["/data_lt2/bg"], None,
                                asset_class=BackgroundAsset)

    def get_context_menu(self, index: QtCore.QModelIndex,
                         refresh_function: Callable) -> List[Union[Tuple[str, Callable], None]]:
        default_context_menu = super(BackgroundsCategory, self).get_context_menu(index, refresh_function)
        if isinstance(index.internalPointer(), BackgroundAsset):
            bg_context_actions = [
                None,
                ("Import PNG", lambda: self.import_png(index, refresh_function)),
                ("Export PNG", lambda: self.export_png(index))
            ]
            default_context_menu.extend(bg_context_actions)
        return default_context_menu

    def import_png(self, index: QtCore.QModelIndex, refresh_callback: Callable):
        node: BackgroundAsset = index.internalPointer()
        import_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Import PNG...", filter="PNG Files (*.png)")
        if import_path == "":
            return

        image: Image.Image = Image.open(import_path)
        bg_image = node.get_bg()
        bg_image.import_image_pil(image)
        bg_image.save()
        image.close()
        refresh_callback(index, index)

    def export_png(self, index: QtCore.QModelIndex):
        node: BackgroundAsset = index.internalPointer()
        filename, _ = os.path.splitext(os.path.basename(node.path))
        filename += ".png"
        export_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Export PNG...", filename,
                                                               filter="PNG Files (*.png)")
        if export_path == "":
            return

        image: Image.Image = node.get_bg().extract_image_pil()
        image.save(export_path)
