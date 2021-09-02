import formats.puzzle as pzd
from formats.binary import BinaryWriter
from formats.filesystem import NintendoDSRom
import unittest
import os


class TestPuzzleData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        rom_path = os.path.dirname(__file__)
        cls.rom = NintendoDSRom.fromFile(rom_path + "/../../test_rom.nds")

    def get_pzd(self):
        pz_data = pzd.Puzzle(rom=self.rom, id_=1)
        pz_data.load_from_rom()
        return pz_data

    def test_loading_saving(self):
        pz_data = self.get_pzd()
        wtr = BinaryWriter()
        pz_data.export_data(wtr)
        assert wtr.data == pz_data.original

    def test_values(self):
        pz_data = self.get_pzd()
        assert pz_data.title == "Dr Schrader's Map"
        assert pz_data.type == 26
        assert pz_data.number == 1
        assert pz_data.location_id == 91
        assert pz_data.tutorial_id == 2
        assert pz_data.reward_id == 255
        assert pz_data.bg_btm_id == 1
        assert pz_data.bg_top_id == 1
        assert pz_data.judge_char == 0
        assert pz_data.flag_bit2 is True
        assert pz_data.flag_bit5 is True
        assert pz_data.bg_lang is False
        assert pz_data.ans_bg_lang is False
        assert len(pz_data.correct_answer) == 55  # Not checking full answer, but the length
        assert pz_data.correct_answer == "Excellent work!\n\nNow, let's hurry to the doctor's flat!"
        assert pz_data.picarat_decay == [10, 9, 8]

    def test_readable(self):
        pz_data = self.get_pzd()
        readable = pz_data.to_readable()
        pz_data.from_readable(readable)
        wtr = BinaryWriter()
        pz_data.export_data(wtr)
        assert wtr.data == pz_data.original
