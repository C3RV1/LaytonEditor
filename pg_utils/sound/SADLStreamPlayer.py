import SADLpy.SADL
import pygame as pg
import numpy as np
from pg_utils.sound.StreamPlayerAbstract import StreamPlayerAbstract


class SADLStreamPlayer(StreamPlayerAbstract):
    def __init__(self):
        super(SADLStreamPlayer, self).__init__()
        self.sadl: SADLpy.SADL.SADL = None
        self.sound_obj: pg.mixer.Sound = None
        self.sound_buffer = None
        self.loading = False
        self.loading_finished = False
        self.buffer_offset = 0
        self.volume = 0.0

        self.fading = False
        self.is_fade_in = False
        self.current_fade_time = 0.0
        self.fade_time = 0.0

    def update_(self, delta_time):
        if self.loading:
            self.add_samples()
        if self.fading:
            self.do_fade(delta_time)

    def do_fade(self, delta_time):
        if self.current_fade_time >= self.fade_time:
            self.current_fade_time = self.fade_time
            self.fading = False
        percentage = (self.current_fade_time / self.fade_time)
        if not self.is_fade_in:
            percentage = 1 - percentage
        new_volume = self.volume * percentage
        self.sound_obj.set_volume(new_volume)
        self.current_fade_time += delta_time

    def add_samples(self, first_init=False):
        sample_steps = 17
        if first_init:
            sample_steps *= 3  # If the sound gets cut increase this number (slower load, better playback)
        new_samples = np.array(self.sadl.decode(sample_steps))
        if new_samples.shape[0] == 0:
            self.loading = False
            self.loading_finished = True
            return
        self.sound_buffer[self.buffer_offset:self.buffer_offset + new_samples.shape[0]] = new_samples
        self.buffer_offset += new_samples.shape[0]

    def start_sound(self, snd_obj: SADLpy.SADL.SADL, loops=0, volume=0.5):
        if self.sound_obj is not None:
            self.sound_obj.stop()
        if self.sadl is not snd_obj:
            self.sadl = snd_obj
            self.sadl.sample_rate = pg.mixer.get_init()[0]  # Set sadl sample rate
            snd_obj.channels = 2
            self.sound_obj = pg.sndarray.make_sound(np.zeros((snd_obj.alloc_size, snd_obj.channels), dtype=np.int16))
            self.sound_buffer = pg.sndarray.samples(self.sound_obj)
            self.loading_finished = False
            self.buffer_offset = 0
            self.add_samples(first_init=True)
        if not self.loading_finished:
            self.loading = True
        self.sound_obj.set_volume(volume)
        self.sound_obj.play(loops=loops)
        self.volume = volume

    def stop(self):
        self.loading_finished = False
        self.loading = False
        if self.sound_obj is not None:
            self.sound_obj.stop()

    def fade(self, time, fade_in):
        self.fading = True
        self.fade_time = time
        self.current_fade_time = 0.0
        self.is_fade_in = fade_in
