class Color():
    def __init__(self, rgb=None, bgr555sum=None):
        self.r, self.g, self.b = 0, 0, 0
        if rgb:
            self.rgb = rgb
        elif bgr555sum:
            self.bgr555int = bgr555sum

    @property
    def rgb(self):
        return self.r, self.g, self.b

    @rgb.setter
    def rgb(self, value):
        self.r, self.g, self.b = [(x >> 3) << 3 for x in value]

    @property
    def bgr555int(self):
        return ((self.b >> 3) << 10) + ((self.g >> 3) << 5) + (self.r >> 3)

    @bgr555int.setter
    def bgr555int(self, bgr555_sum):
        self.r = (bgr555_sum & (2 ** 5 - 1)) << 3
        self.g = ((bgr555_sum >> 5) & (2 ** 5 - 1)) << 3
        self.b = ((bgr555_sum >> 10) & (2 ** 5 - 1)) << 3
