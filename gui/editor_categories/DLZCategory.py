from ..EditorTypes import EditorCategory, EditorObject

from PySide6 import QtCore, QtWidgets, QtGui
from formats.dlz_types.TimeDefinitions import TimeDefinitionsDlz
from formats.dlz_types.SoundFix import SoundFixDlz


class SoundFixCategory(EditorCategory):
    def __init__(self):
        super(SoundFixCategory, self).__init__()
        self.name = "Sound Fix"
        self.sound_fix_dlz: SoundFixDlz = None

    def reset_file_system(self):
        self.sound_fix_dlz = SoundFixDlz(rom=self.rom, filename="/data_lt2/rc/snd_fix.dlz")

    def get_sound_profile_dlz(self) -> SoundFixDlz:
        return self.sound_fix_dlz


class TimeDefinitionsNode(EditorCategory):
    def __init__(self):
        super().__init__()
        self.name = "Time Definitions"
        self.time_def_dlz: TimeDefinitionsDlz = None

    def reset_file_system(self):
        self.time_def_dlz = TimeDefinitionsDlz(rom=self.rom, filename="/data_lt2/rc/tm_def.dlz")

    def get_time_definitions_dlz(self):
        return self.time_def_dlz
