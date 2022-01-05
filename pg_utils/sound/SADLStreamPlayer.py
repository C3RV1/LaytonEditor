import math

from formats.sound import sadl
from formats.sound import sample_transform
import pygame as pg
import numpy as np
from pg_utils.sound.StreamPlayerAbstract import StreamPlayerAbstract


class SADLStreamPlayer(StreamPlayerAbstract):
    def __init__(self):
        super(SADLStreamPlayer, self).__init__()
        self.sadl: sadl.SADL = None

        self.target_rate = pg.mixer.get_init()[0]
        self.target_channels = pg.mixer.get_init()[2]

    def add_samples(self, first_init=False):
        sample_steps = 20
        if first_init:
            sample_steps *= 3  # If the sound gets cut increase this number (slower load, better playback)
        new_samples = np.array(self.sadl.decode(sample_steps))
        new_samples = sample_transform.change_channels(new_samples, self.target_channels)
        new_samples = sample_transform.change_sample_rate(new_samples, self.sadl.sample_rate, self.target_rate)
        new_samples = new_samples.swapaxes(0, 1)
        if new_samples.shape[0] == 0:
            self.loading = False
            self.loading_finished = True
            return
        copy_size = min(new_samples.shape[0], self.sound_buffer.shape[0] - self.buffer_offset)
        self.sound_buffer[self.buffer_offset:self.buffer_offset + copy_size] = new_samples[:copy_size]
        self.buffer_offset += copy_size

    def start_sound(self, snd_obj: sadl.SADL, loops=False):
        if self.sound_obj is not None:
            self.sound_obj.stop()
        if self.sadl is not snd_obj:
            self.sadl = snd_obj
            alloc_size = int(math.ceil(snd_obj.num_samples * self.target_rate / snd_obj.sample_rate))
            self.sound_obj = pg.sndarray.make_sound(np.zeros((alloc_size, self.target_channels), dtype=np.int16))
            self.sound_buffer = pg.sndarray.samples(self.sound_obj)
            self.loading_finished = False
            self.buffer_offset = 0
            self.add_samples(first_init=True)
        if not self.loading_finished:
            self.loading = True
        self.sound_obj.set_volume(self.volume)
        self.sound_obj.play(loops=-1 if loops else 0)
