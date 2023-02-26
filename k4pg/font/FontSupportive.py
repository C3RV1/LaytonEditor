from .Font import Font


class FontSupportive:
    def __init__(self, *args, **kwargs):
        super(FontSupportive, self).__init__(*args, **kwargs)
        self._font = None

    def set_font(self, f: Font):
        self._font = f

    def get_font(self) -> Font:
        return self._font
