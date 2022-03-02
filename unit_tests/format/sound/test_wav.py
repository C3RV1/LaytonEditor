import unittest
from formats import binary
from formats.sound.wav import WAV
import os
import io


# class TestWAV(unittest.TestCase):
# TODO: Find alternative to a baked file
class TestWAV_not_working:
    @classmethod
    def setUpClass(cls) -> None:
        wav_file = cls.open_file("test_wav.wav", "rb")
        cls.wav_data = wav_file.read()
        wav_file.close()

    @staticmethod
    def open_file(name, method):
        p = os.path.join(os.path.dirname(__file__), name)
        f = open(p, method)
        return f

    def not_working_test_loadAndSave(self) -> None:
        wav_obj = WAV()
        wav_obj.read_stream(self.wav_data)

        expected_file = self.open_file("expected.wav", "rb")
        expected_data = expected_file.read()
        expected_file.close()

        wav_obj.change_sample_rate(32768)

        exported_file = io.BytesIO()
        exported_file = binary.BinaryWriter(exported_file)
        wav_obj.write_stream(exported_file)

        exported_data = exported_file.readall()
        assert exported_data == expected_data
