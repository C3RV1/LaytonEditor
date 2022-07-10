from ..input.Controls import Controls
from .MenuItem import MenuItem


class MenuController:
    def __init__(self, active, controls):
        self.controls: Controls = controls
        self.active_menu_item: MenuItem = active
        self.set_hover(True)

    def set_hover(self, hover):
        if self.active_menu_item:
            self.active_menu_item.set_hover(hover)

    def set_press(self, press):
        if self.active_menu_item:
            self.active_menu_item.set_press(press)

    def change_menu_item(self, active):
        if not active:
            return
        self.set_hover(False)
        self.active_menu_item = active
        self.set_hover(True)

    def update(self):
        if self.controls.up():
            self.change_menu_item(self.active_menu_item.up)
        elif self.controls.right():
            self.change_menu_item(self.active_menu_item.right)
        elif self.controls.down():
            self.change_menu_item(self.active_menu_item.down)
        elif self.controls.left():
            self.change_menu_item(self.active_menu_item.left)
        if self.controls.confirm():
            self.active_menu_item.set_press(True)
