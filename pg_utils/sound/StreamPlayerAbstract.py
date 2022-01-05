import pygame as pg


class StreamPlayerAbstract:
    def __init__(self):
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

        self.expected_buffer_position = 0
        self.sample_rate = 0
        self.playing = False

    def update_(self, delta_time):
        if self.playing:
            self.expected_buffer_position += self.sample_rate * delta_time
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
        if self.sound_obj:
            self.sound_obj.set_volume(new_volume)
        self.current_fade_time += delta_time

    def stop(self):
        self.loading_finished = False
        self.loading = False
        self.playing = False
        if self.sound_obj is not None:
            self.sound_obj.stop()

    def fade(self, time, fade_in):
        self.fading = True
        self.fade_time = time
        self.current_fade_time = 0.0
        self.is_fade_in = fade_in

    def set_volume(self, volume):
        if volume != self.volume:
            self.volume = volume
            if not self.fading:
                if self.sound_obj is not None:
                    self.sound_obj.set_volume(volume)
            else:
                self.do_fade(0)

    def add_samples(self, first_init=False):
        pass

    def start_sound(self, snd_obj, loops=False):
        pass

    @staticmethod
    def get_playable():
        return True
