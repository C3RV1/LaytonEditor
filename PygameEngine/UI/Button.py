from .UIElement import UIElement
from ..Input import Input
from ..Animation import Animation
from ..GameManager import GameManager


class Button(UIElement, Animation):
    def __init__(self, groups):
        super(Button, self).__init__()
        Animation.__init__(self, groups)
        self.gm = GameManager()

        self.check_interacting = self._check_interacting
        self.mouse_button = 1
        self.current_time = 0
        self.time_interact_command = 0

    def _check_interacting(self):
        if self.interacting:
            self.current_time += self.gm.delta_time
            if self.current_time > self.time_interact_command:
                self.interacting = False
        else:
            mouse_pos = Input().get_screen_mouse_pos()
            if Input().get_mouse_down(self.mouse_button):
                if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    self.interacting = True
                    self.current_time = 0

