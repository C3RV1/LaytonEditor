import PygameEngine.UI.UIElement
import PygameEngine.GameManager
import PygameEngine.Input
import PygameEngine.Sprite


class DragObject(PygameEngine.UI.UIElement.UIElement, PygameEngine.Sprite.Sprite):
    def __init__(self, groups):
        PygameEngine.UI.UIElement.UIElement.__init__(self)
        PygameEngine.Sprite.Sprite.__init__(self, groups)
        self.gm = PygameEngine.GameManager.GameManager()
        self.rel_position = [0, 0]

        self.check_interacting = self._check_interacting
        self.interact = self._interact

    def _check_interacting(self):
        if self.interacting:
            if PygameEngine.Input.Input().get_mouse_up(1):
                self.interacting = False
        else:
            mouse_pos = PygameEngine.Input.Input().get_screen_mouse_pos()
            if PygameEngine.Input.Input().get_mouse_down(1):
                if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    self.rel_position[0] = self.rect[0] - mouse_pos[0]
                    self.rel_position[1] = self.rect[1] - mouse_pos[1]
                    self.interacting = True

    def _interact(self):
        mouse_pos = PygameEngine.Input.Input().get_screen_mouse_pos()
        self.rect.x = mouse_pos[0] + self.rel_position[0]
        self.rect.y = mouse_pos[1] + self.rel_position[1]
        self.world_rect.x, self.world_rect.y = self.current_camera.screen_to_world(self.rect.x, self.rect.y)
        self.world_rect.x += self.world_rect.w // 2
        self.world_rect.y += self.world_rect.h // 2
        self.dirty = 1
