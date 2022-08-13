import pg_utils.sound.SADLStreamPlayer
import pg_utils.sound.SMDLStreamPlayer
from pg_utils.rom.rom_extract import load_sadl, load_smd


class EventSound:
    def __init__(self):
        self.sadl_player = pg_utils.sound.SADLStreamPlayer.SADLStreamPlayer(loops=False)
        self.sadl_player.set_volume(0.5)
        self.bg_player = pg_utils.sound.SMDLStreamPlayer.SMDLStreamPlayer(loops=True)
        self.bg_player.set_volume(0.3)

    def play_smdl(self, path):
        smd_obj, swd_file, sample_bank = load_smd(path)
        self.bg_player.create_temporal_sf2(swd_file, sample_bank)
        self.bg_player.load_sound(smd_obj)
        self.bg_player.play()

    def stop_smdl(self):
        self.bg_player.stop()

    def play_sadl(self, path):
        sadl = load_sadl(path)
        self.sadl_player.load_sound(sadl)
        self.sadl_player.play()

    def stop_sadl(self):
        self.sadl_player.stop()

    def update_(self, dt: float):
        self.sadl_player.update(dt)
        self.bg_player.update(dt)

    def fade(self, is_fade_in, frames):
        time = frames / 1000.0
        self.bg_player.fade(time, is_fade_in)
