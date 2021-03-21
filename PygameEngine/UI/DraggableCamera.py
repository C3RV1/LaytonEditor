from ..Camera import Camera
from .UIElement import UIElement
from ..Input import Input


class DraggableCamera(Camera, UIElement):
    def __init__(self):
        self.inp = Input()
        Camera.__init__(self)
        UIElement.__init__(self)
        self.__rel_position = [0, 0]

        self.check_interacting = self.check_interact_
        self.interact = self.interact_

    def check_interact_(self):
        if not self.interacting:
            mouse_pos = self.inp.get_screen_mouse_pos()
            if self.inp.get_mouse_down(1) and self.display_port.collidepoint(mouse_pos):
                self.__rel_position[0] = self.position[0] - mouse_pos[0]
                self.__rel_position[1] = self.position[1] - mouse_pos[1]
                self.interacting = True
                self.interacting = True
        else:
            if self.inp.get_mouse_up(1):
                self.interacting = False

    def interact_(self):
        mouse_pos = self.inp.get_screen_mouse_pos()
        self.position[0] = mouse_pos[0] + self.__rel_position[0]
        self.position[1] = mouse_pos[1] + self.__rel_position[1]
