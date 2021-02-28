import PygameEngine.Camera
import PygameEngine.UI.UIElement
import PygameEngine.Input


class DraggableCamera(PygameEngine.Camera.Camera, PygameEngine.UI.UIElement.UIElement):
    def __init__(self):
        self.inp = PygameEngine.Input.Input()
        PygameEngine.Camera.Camera.__init__(self)
        PygameEngine.UI.UIElement.UIElement.__init__(self)
        self.rel_position = [0, 0]

        self.check_interacting = self.check_interact_
        self.interact = self.interact_

    def check_interact_(self):
        if not self.interacting:
            mouse_pos = self.inp.get_screen_mouse_pos()
            if self.inp.get_mouse_down(1) and self.display_port.collidepoint(mouse_pos):
                self.rel_position[0] = self.position[0] - mouse_pos[0]
                self.rel_position[1] = self.position[1] - mouse_pos[1]
                self.interacting = True
                self.interacting = True
        else:
            if self.inp.get_mouse_up(1):
                self.interacting = False

    def interact_(self):
        mouse_pos = PygameEngine.Input.Input().get_screen_mouse_pos()
        self.position[0] = mouse_pos[0] + self.rel_position[0]
        self.position[1] = mouse_pos[1] + self.rel_position[1]