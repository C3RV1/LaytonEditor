import PygameEngine.UI.UIElement
import PygameEngine.Input
import PygameEngine.Sprite


class Button(PygameEngine.UI.UIElement.UIElement, PygameEngine.Sprite.Sprite):
    def __init__(self, groups):
        super(Button, self).__init__()
        PygameEngine.Sprite.Sprite.__init__(self, groups)
        self.command = None

        self.check_interacting = self._check_interacting
        self.interact = self._interact

    def _check_interacting(self):
        mouse_pos = PygameEngine.Input.Input().get_screen_mouse_pos()
        if PygameEngine.Input.Input().get_mouse_down(1):
            if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.interacting = True
                return
        self.interacting = False

    def _interact(self):
        if callable(self.command):
            self.command()
