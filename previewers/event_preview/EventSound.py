from .abstracts.EventSoundAbstract import EventSoundAbstract
import pygame_utils.SADLStreamPlayer
from pygame_utils.rom.rom_extract import load_sadl


class EventSound(EventSoundAbstract):
    def __init__(self):
        super().__init__()
        self.player = pygame_utils.SADLStreamPlayer.SoundPlayer()
        self.loops = False

    def play(self, path):
        sadl = load_sadl(path)
        self.player.start_sound(sadl, self.loops)

    def stop(self):
        self.player.stop()

    def update_(self):
        self.player.update_()
