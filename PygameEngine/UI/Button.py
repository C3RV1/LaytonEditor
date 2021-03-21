from .UIElement import UIElement
from ..Input import Input
from ..Sprite import Sprite


class Button(UIElement, Sprite):
    def __init__(self, groups):
        super(Button, self).__init__()
        Sprite.__init__(self, groups)
        self.command = None

        self.check_interacting = self._check_interacting
        self.interact = self._interact

    def _check_interacting(self):
        mouse_pos = Input().get_screen_mouse_pos()
        if Input().get_mouse_down(1):
            if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.interacting = True
                return
        self.interacting = False

    def _interact(self):
        if callable(self.command):
            self.command()
