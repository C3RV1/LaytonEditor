from PySide6 import QtCore, QtWidgets, QtGui
from gui.ui.SoundProfileWidget import SoundProfileUI
from formats.dlz import SoundProfile


class SoundProfileEditor(SoundProfileUI):
    def __init__(self):
        super(SoundProfileEditor, self).__init__()
        self.sound_profile: SoundProfile = None
        self.save_func = lambda: None

    def set_snd_profile(self, snd_profile: SoundProfile, save_func):
        self.sound_profile = snd_profile
        self.bg_music_id_spin.setValue(self.sound_profile.bg_music_id)
        self.unk0_spin.setValue(self.sound_profile.unk0)
        self.unk1_spin.setValue(self.sound_profile.unk1)
        self.save_btn = save_func

    def bg_music_id_spin_edit(self, value: int):
        self.sound_profile.bg_music_id = value

    def unk0_spin_edit(self, value: int):
        self.sound_profile.unk0 = value

    def unk1_spin_edit(self, value: int):
        self.sound_profile.unk1 = value

    def save_btn_click(self):
        self.save_btn()
