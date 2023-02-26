from ..ui.ButtonSprite import ButtonSprite
from .MenuItem import MenuItem


class MenuButtonSprite(ButtonSprite, MenuItem):
    def __init__(self, *args, **kwargs):
        super(MenuButtonSprite, self).__init__(*args, **kwargs)

    def get_hover(self, cam):
        return self.hovering

    def get_press(self):
        pressed = self.pressed
        self.pressed = False
        return pressed