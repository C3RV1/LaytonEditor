

class MenuItem:
    def __init__(self, *args, **kwargs):
        super(MenuItem, self).__init__(*args, **kwargs)
        self.right = None
        self.up = None
        self.left = None
        self.down = None
        self.hovering = False
        self.pressed = False

    def set_hover(self, hover):
        self.hovering = hover

    def set_press(self, press):
        self.pressed = press
