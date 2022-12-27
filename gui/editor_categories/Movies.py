import os
import re

from .Filesystem import FilesystemCategory, FolderNodeOneLevel, AssetNodeBasename
from PySide6 import QtCore, QtWidgets
from typing import Callable, List, Union, Tuple

import threading
import subprocess

from formats import conf
from formats.sound.sadl import SADL
from formats_parsed.sound.wav import WAV
from previewers.sound.SoundPreview import SoundPreview
from pg_utils.sound.SADLStreamPlayer import SADLStreamPlayer
from ..SettingsManager import SettingsManager
from ..PygamePreviewer import PygamePreviewer


def get_movie_num(path):
    if match := re.match(r"m([0-9]+)\.mods", os.path.basename(path)):
        return int(match.group(1))
    return -1


class MovieFolder(FolderNodeOneLevel):
    def __init__(self, *args, **kwargs):
        super(MovieFolder, self).__init__(*args, **kwargs)
        self.files.sort(key=lambda x: get_movie_num(x))


class MovieAsset(AssetNodeBasename):
    def get_num(self):
        if (num := get_movie_num(self.path)) >= 0:
            return num
        return None

    def get_sad(self):
        if not self.rom.name == b"LAYTON2":
            return None
        num = self.get_num()
        if num is None:
            return None
        return SADL(f"/data_lt2/stream/movie/{conf.LANG}/M{num}.SAD", rom=self.rom)

    def has_audio(self):
        return self.rom.name == b"LAYTON2" and self.get_num() is not None


class MoviesCategory(FilesystemCategory):
    def __init__(self):
        super(MoviesCategory, self).__init__()
        self.name = "Movies"

    def reset_file_system(self):
        self._root = MovieFolder(self, "/data_lt2/movie", self.rom.filenames["/data_lt2/movie"], None,
                                 asset_class=MovieAsset)

    def get_context_menu(self, index: QtCore.QModelIndex,
                         refresh_function: Callable) -> List[Union[Tuple[str, Callable], None]]:
        default_options = super(MoviesCategory, self).get_context_menu(index, refresh_function)
        if isinstance(index.internalPointer(), MovieAsset):
            asset: MovieAsset = index.internalPointer()
            default_options.extend([
                None,
                ("View", lambda: self.view_mods(index))
            ])
            if asset.has_audio():
                default_options.extend([
                    None,
                    ("Export audio WAV", lambda: self.import_wav(index, refresh_function)),
                    ("Import audio WAV", lambda: self.export_wav(index))
                ])
        return default_options

    def view_mods(self, index: QtCore.QModelIndex):
        if not os.path.isdir(os.getcwd() + "\\temporary"):
            os.mkdir(os.getcwd() + "\\temporary")

        asset: MovieAsset = index.internalPointer()

        def open_mobi_view():
            mobi_location = os.getcwd() + "\\data_permanent\\mobiclip\\MobiclipDecoder.exe"
            temp_file_location = os.getcwd() + "\\temporary\\temp.mods"
            # Use subprocess instead of os.system in case the path contains spaces
            subprocess.run([mobi_location, temp_file_location])

        output_location = os.getcwd() + "\\temporary\\temp.mods"
        path, archive = asset.path, asset.rom
        with open(output_location, "wb+") as out_file:
            with archive.open(path, "rb") as game_file:
                out_file.write(game_file.read())
        t1 = threading.Thread(target=open_mobi_view)
        t1.start()

        if asset.has_audio():
            sound_previewer = SoundPreview(SADLStreamPlayer(), asset.get_sad(),
                                           f"Movie {asset.get_num()}")
            PygamePreviewer.INSTANCE.start_renderer(sound_previewer)
            sound_previewer.start_sound()

    def import_wav(self, index: QtCore.QModelIndex, refresh_callback: Callable):
        node: MovieAsset = index.internalPointer()
        import_path = SettingsManager().import_file(None, "Import WAV...", "WAV Files (*.wav)")
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
        sadl = node.get_sad()
        if wav_file.to_sadl(sadl, progress_callback=update_progress):
            sadl.save()

        refresh_callback(index, index)

    def export_wav(self, index: QtCore.QModelIndex):
        node: MovieAsset = index.internalPointer()
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

        wav_file, successful = WAV.from_sadl(node.get_sad(), progress_callback=update_progress)
        if not successful:
            return
        with open(export_path, "wb") as export_file:
            wav_file.write_stream(export_file)
