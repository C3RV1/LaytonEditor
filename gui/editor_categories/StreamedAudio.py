import os.path

from .Filesystem import FolderNode, AssetNodeBasename, FilesystemCategory, FolderNodeFilterExtension
from PySide6 import QtCore, QtWidgets, QtGui
from typing import List, Tuple, Callable, Union
from formats.sound.sadl import SADL
from formats_parsed.sound.wav import WAV
from ..SettingsManager import SettingsManager


class SADLNode(AssetNodeBasename):
    def get_sadl(self):
        return SADL(self.path, rom=self.rom)


class StreamedAudioCategory(FilesystemCategory):
    def __init__(self):
        super(StreamedAudioCategory, self).__init__()
        self.name = "Streamed Audio"

    def reset_file_system(self):
        if self.rom.name == b"LAYTON2":
            self._root = FolderNode(self, "/data_lt2/stream", self.rom.filenames["/data_lt2/stream"], None,
                                    asset_class=SADLNode)
        else:
            self._root = FolderNodeFilterExtension(self, "", self.rom.filenames, None, extensions=[".SAD"],
                                                   asset_class=SADLNode)

    def get_context_menu(self, index: QtCore.QModelIndex,
                         refresh_function: Callable) -> List[Union[Tuple[str, Callable], None]]:
        default_context_menu = super(StreamedAudioCategory, self).get_context_menu(index, refresh_function)
        if isinstance(index.internalPointer(), SADLNode):
            wav_context_actions = [
                None,
                ("Import WAV", lambda: self.import_wav(index, refresh_function)),
                ("Export WAV", lambda: self.export_wav(index))
            ]
            default_context_menu.extend(wav_context_actions)
        return default_context_menu

    def import_wav(self, index: QtCore.QModelIndex, refresh_callback: Callable):
        node: SADLNode = index.internalPointer()
        import_path, _ = SettingsManager().import_file(None, "Import WAV...", "WAV Files (*.wav)")
        if import_path == "":
            return

        wav_file = WAV()
        with open(import_path, "rb") as import_file:
            wav_file.read_stream(import_file)

        progress_dialog = QtWidgets.QProgressDialog("Encoding WAV...", "Abort", 0, 100, None)
        progress_dialog.setWindowModality(QtCore.Qt.WindowModality.WindowModal)

        def update_progress(value, maximum):
            progress_dialog.setMaximum(maximum)
            progress_dialog.setValue(value)
            return progress_dialog.wasCanceled()

        progress_dialog.setValue(0)
        sadl = node.get_sadl()
        if wav_file.to_sadl(sadl, progress_callback=update_progress):
            sadl.save()

        refresh_callback(index, index)

    def export_wav(self, index: QtCore.QModelIndex):
        node: SADLNode = index.internalPointer()
        filename, _ = os.path.splitext(os.path.basename(node.path))
        filename += ".wav"
        export_path = SettingsManager().export_file(None, "Export WAV...", filename, "WAV Files (*.wav)")
        if export_path == "":
            return

        progress_dialog = QtWidgets.QProgressDialog("Decoding SADL...", "Abort", 0, 100, None)
        progress_dialog.setWindowModality(QtCore.Qt.WindowModality.WindowModal)

        def update_progress(value, maximum):
            progress_dialog.setMaximum(maximum)
            progress_dialog.setValue(value)
            return progress_dialog.wasCanceled()

        wav_file, successful = WAV.from_sadl(node.get_sadl(), progress_callback=update_progress)
        if not successful:
            return
        with open(export_path, "wb") as export_file:
            wav_file.write_stream(export_file)

