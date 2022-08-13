from typing import Optional

import pygame as pg


class StreamPlayerAbstract:
    def __init__(self, loops=False):
        self.sound_obj: Optional[pg.mixer.Sound] = None
        self.channel: Optional[pg.mixer.Channel] = None
        self.sound_buffer = None
        self.loading = False
        self.loading_finished = False
        self.buffer_offset = 0
        self.volume = 0.0

        self.fading = False
        self.is_fade_in = False
        self.current_fade_time = 0.0
        self.fade_time = 0.0

        self.expected_buffer_position = 0
        self.sample_rate = 0
        self.playing = False
        self.paused = False
        self.channels = 0

        self.loops = loops

    def update(self, delta_time):
        if self.playing and not self.paused:
            self.expected_buffer_position += self.sample_rate * delta_time
            if self.channel is not None:
                if not self.channel.get_busy():
                    self.playing = False
        if self.loading:
            self.add_samples()
        if self.fading and not self.paused:
            self.do_fade(delta_time)

    def pause(self):
        if not self.playing:
            return
        if self.channel.get_sound() != self.sound_obj:
            return
        self.channel.pause()
        self.paused = True

    def unpause(self):
        if not self.playing:
            self.play()
            return
        if self.channel.get_sound() != self.sound_obj:
            return
        self.channel.unpause()
        self.paused = False

    def do_fade(self, delta_time):
        if not self.playing:
            return
        if self.current_fade_time >= self.fade_time:
            self.current_fade_time = self.fade_time
            self.fading = False
        percentage = (self.current_fade_time / self.fade_time)
        if not self.is_fade_in:
            percentage = 1 - percentage
        new_volume = self.volume * percentage
        if self.channel is not None and self.channel.get_sound() == self.sound_obj:
            self.channel.set_volume(new_volume)
        self.current_fade_time += delta_time

    def stop(self):
        if not self.playing:
            return
        self.loading_finished = False
        self.loading = False
        self.playing = False
        self.fading = False
        if self.channel is not None and self.channel.get_sound() == self.sound_obj:
            self.channel.stop()
            self.channel = None

    def fade(self, time, fade_in):
        self.fading = True
        self.fade_time = time
        self.current_fade_time = 0.0
        self.is_fade_in = fade_in

    def set_volume(self, volume):
        if volume != self.volume:
            self.volume = volume
            if not self.fading:
                if self.channel is not None:
                    self.channel.set_volume(volume)
            else:
                self.do_fade(0)

    def add_samples(self, first_init=False):
        pass

    def load_sound(self, snd_obj):
        self.stop()
        self.sample_rate = pg.mixer.get_init()[0]
        self.channels = pg.mixer.get_init()[2]
        if not self._load_sound(snd_obj):
            # sound not loaded correctly
            return
        self.loading = True
        self.loading_finished = False
        self.buffer_offset = 0
        self.add_samples(first_init=True)
        self.playing = False
        self.paused = False

    def _load_sound(self, snd_obj):
        return False

    def play(self):
        self.expected_buffer_position = 0
        self.channel = self.sound_obj.play(loops=-1 if self.loops else 0)
        self.channel.set_volume(self.volume)
        self.playing = True
        self.paused = False

    @staticmethod
    def get_playable():
        return True
