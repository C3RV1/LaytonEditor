

class StreamPlayerAbstract:
    def __init__(self):
        pass

    def update_(self, delta_time):
        pass

    def add_samples(self, first_init=False):
        pass

    def start_sound(self, snd_obj, loops=0, volume=0.5):
        pass

    def stop(self):
        pass

    def fade(self, time, fade_in):
        pass

    @staticmethod
    def get_playable():
        return True
