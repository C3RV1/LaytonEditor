

class EventBGAbstract:
    FADE_IN = 1
    FADE_OUT = 2

    def __init__(self):
        pass

    def set_bg(self, path):
        pass

    def set_opacity(self, opacity):
        pass

    def shake(self):
        pass

    def set_fade_max_opacity(self, opacity):
        pass

    def fade(self, fade_type, fade_time, instant):
        pass
