

class EventSoundAbstract:
    def __init__(self):
        pass

    def play_sadl(self, path, volume=1):
        pass

    def stop_sadl(self):
        pass

    def play_smdl(self, path, volume=1):
        pass

    def stop_smdl(self):
        pass

    def fade(self, is_fade_in, frames):
        pass
