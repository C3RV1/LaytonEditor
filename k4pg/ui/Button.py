from ..Camera import Camera
from ..GameManager import GameManager


class Button:
    def __init__(self, *args, pressed_counter=0.1, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self._pressed = False
        self._hovering = False
        self.pressed_counter = pressed_counter
        self._current_pressed_counter = 0
        self.gm = GameManager()

    def on_not_pressed(self):
        pass

    def on_pressed(self):
        pass

    def on_hover(self):
        pass

    def get_hover(self, cam: Camera):
        return False

    def get_press(self):
        return False

    def get_pressed(self, cam: Camera):
        self._hovering = False
        if not self._pressed:
            if self.get_hover(cam):
                if self.get_press():
                    self._pressed = True
                    self.on_pressed()
                    self._current_pressed_counter = self.pressed_counter
                else:
                    self.on_hover()
                    self._hovering = True
            else:
                self.on_not_pressed()
        else:
            if self._current_pressed_counter <= 0:
                self.on_not_pressed()
                self._current_pressed_counter = 0
                self._pressed = False
                return True
            self._current_pressed_counter -= self.gm.delta_time
        return False
