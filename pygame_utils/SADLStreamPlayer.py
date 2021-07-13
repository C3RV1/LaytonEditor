import SADLpy.SADL
import pygame as pg
import numpy as np


class SoundPlayer:
    def __init__(self):
        self.sadl: SADLpy.SADL.SADL = None
        self.sound_obj: pg.mixer.Sound = None
        self.sound_buffer = None
        self.loading = False
        self.loading_finished = False
        self.buffer_offset = 0

    def update_(self):
        if self.loading:
            self.add_samples()

    def add_samples(self, first_init=False):
        sample_steps = 19
        if first_init:
            sample_steps *= 4  # If the sound gets cut increase this number (slower load, better playback)
        new_samples = np.array(self.sadl.decode_procyon(sample_steps))
        if new_samples.shape[0] == 0:
            self.loading = False
            self.loading_finished = True
            return
        self.sound_buffer[self.buffer_offset:self.buffer_offset + new_samples.shape[0]] = new_samples
        self.buffer_offset += new_samples.shape[0]

    def start_sound(self, sadl: SADLpy.SADL.SADL, loops=0, volume=0.5):
        if self.sound_obj is not None:
            self.sound_obj.stop()
        if self.sadl is not sadl:
            self.sadl = sadl
            self.sadl.sample_rate = pg.mixer.get_init()[0]  # Set sadl sample rate
            sadl.channels = 2
            self.sound_obj = pg.sndarray.make_sound(np.zeros((sadl.alloc_size, sadl.channels), dtype=np.int16))
            self.sound_buffer = pg.sndarray.samples(self.sound_obj)
            self.loading_finished = False
            self.buffer_offset = 0
            self.add_samples(first_init=True)
        if not self.loading_finished:
            self.loading = True
        self.sound_obj.set_volume(volume)
        self.sound_obj.play(loops=loops)

    def stop(self):
        self.loading_finished = False
        self.loading = False
        if self.sound_obj is not None:
            self.sound_obj.stop()
