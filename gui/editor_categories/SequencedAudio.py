import os.path
from PySide6 import QtCore, QtWidgets
from typing import Callable, List, Tuple, Union

from formats_parsed.sound import sf2
from .Filesystem import FilesystemCategory, FolderNodeOneLevelFilterExtension, AssetNodeBasename
from formats.sound.smdl.smdl import SMDL
from formats.sound.swdl import SWDL
from formats_parsed.sound.SMDLMidiSequencer import SMDLMidiSequencer
from formats_parsed.sound.SMDLBuilder import SMDLBuilderMidi
import mido
from ..SettingsManager import SettingsManager


class SMDLNode(AssetNodeBasename):
    def sample_bank(self):
        path = os.path.join(os.path.dirname(self.path), "BG_999.SWD")
        path = path.replace("\\", "/")
        return SWDL(path, rom=self.rom)

    def get_swdl(self):
        return SWDL(os.path.splitext(self.path)[0] + ".SWD", rom=self.rom)

    def get_smdl(self):
        return SMDL(self.path, rom=self.rom)


class SequencedAudioCategory(FilesystemCategory):
    def __init__(self):
        super(SequencedAudioCategory, self).__init__()
        self.name = "Sequenced Audio"

    def reset_file_system(self):
        self._root = FolderNodeOneLevelFilterExtension(self, "/data_lt2/sound", self.rom.filenames["/data_lt2/sound"],
                                                       None, extensions=[".SMD"], asset_class=SMDLNode)

    def get_context_menu(self, index: QtCore.QModelIndex,
                         refresh_function: Callable) -> List[Union[Tuple[str, Callable], None]]:
        default_context_menu = super(SequencedAudioCategory, self).get_context_menu(index, refresh_function)
        if isinstance(index.internalPointer(), SMDLNode):
            default_context_menu.extend([
                None,
                ("Import MID", lambda: self.import_mid(index, refresh_function)),
                ("Export MID", lambda: self.export_mid(index)),
                ("Export Instruments to SF2", lambda: self.export_sf2(index))
            ])
        return default_context_menu

    def import_mid(self, index, refresh_callback):
        node: SMDLNode = index.internalPointer()
        import_path = SettingsManager().import_file(None, "Import MID...", "MIDI Files (*.mid)")
        if import_path == "":
            return

        with open(import_path, "rb") as import_file:
            midi_file = mido.MidiFile(file=import_file)

        smd = node.get_smdl()
        smd_builder = SMDLBuilderMidi(smd)
        smd_builder.build_midi(midi_file)
        smd.save()

        refresh_callback(index, index)

    def export_mid(self, index):
        node: SMDLNode = index.internalPointer()

        filename, _ = os.path.splitext(os.path.basename(node.path))
        filename += ".mid"
        export_path = SettingsManager().export_file(None, "Export MID...", filename, "MIDI Files (*.mid)")
        if export_path == "":
            return

        smd_midi_seq = SMDLMidiSequencer(node.get_smdl())
        mid = smd_midi_seq.generate_mid()
        with open(export_path, "wb") as export_file:
            mid.save(file=export_file)

    def export_sf2(self, index):
        node: SMDLNode = index.internalPointer()

        swd = node.get_swdl()
        sample_bank = node.sample_bank()

        sf = sf2.SoundFont()
        sf.samples = swd.samples
        sf.programs = swd.programs
        sf.info_chunk.isft_chunk = sf2.ISFTChunk(sound_font_tool="Layton Editor")
        sf.set_sample_data(sample_bank.samples)

        filename, _ = os.path.splitext(os.path.basename(node.path))
        filename += ".sf2"
        export_path = SettingsManager().export_file(None, "Export SF2...", filename, "SoundFont Files (*.sf2)")
        if export_path == "":
            return

        with open(export_path, "wb") as export_file:
            sf.write_stream(export_file)
