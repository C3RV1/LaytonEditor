import hashlib
from typing import Dict

from formats.binary import BinaryWriter
from formats.sound.smdl import smdl, SMDLMidiSequencer, SMDLBuilder
from formats.sound import swdl
from formats.sound import sound_types
from formats import binary
from formats.filesystem import NintendoDSRom
import unittest
import os
import io


class TestSMD(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rom_path = os.path.dirname(__file__)
        cls.rom = NintendoDSRom.fromFile(rom_path + "/../../../test_rom.nds")

    def get_smd(self):
        return self.rom.open("data_lt2/sound/BG_004.SMD", "rb")

    def test_SMDReadAndSave(self):
        smd_file = self.get_smd()
        smd_data = smd_file.read()
        smd_file.close()

        smd_obj = smdl.SMDL(filename="data_lt2/sound/BG_004.SMD", rom=self.rom)

        exported_file = binary.BinaryWriter()
        smd_obj.write_stream(exported_file)

        exported_data = exported_file.readall()
        assert smd_data == exported_data

    def test_SMD_Mid(self):
        smd_obj = smdl.SMDL(filename="data_lt2/sound/BG_004.SMD", rom=self.rom)

        binary_writer = BinaryWriter()
        smd_obj.write_stream(binary_writer)
        assert hashlib.sha256(binary_writer.getvalue()).hexdigest() == "a876cb3acd2940219eeeb247ed6b078bbdde5ab7602ac72a8b77119f1f58a923"

        smd_midi_seq = SMDLMidiSequencer.SMDLMidiSequencer(smd_obj)
        mid = smd_midi_seq.generate_mid()

        exported_file = io.BytesIO()
        mid.save(file=exported_file)
        assert hashlib.sha256(exported_file.getvalue()).hexdigest() == "89b9b44e21dcdb82b0ded4cef625e3680615d96da465836b8ab59cb5d8fa9d94"

        smd_midi_builder = SMDLBuilder.SMDLBuilderMidi(smd_obj)
        smd_midi_builder.build_midi(mid)

        binary_writer = BinaryWriter()
        smd_obj.write_stream(binary_writer)
        assert hashlib.sha256(binary_writer.getvalue()).hexdigest() == "ec5e8053c8cf93ed554e07d26869c878ff6e89ed85ee0b90de92cca6dfaa782f"

