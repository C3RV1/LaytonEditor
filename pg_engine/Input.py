import pygame


class Input(object):
    __instance = None
    __inited = False

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not isinstance(Input.__instance, Input):
            Input.__instance = super(Input, cls).__new__(cls, *args, **kwargs)
        return Input.__instance

    def __init__(self):
        if not Input.__inited:
            Input.__inited = True
            self._key_down = {}
            self._key_updated = []
            self._key_grab_id = None

            self._mouse_down = {}
            self._mouse_updated = []
            self._mouse_position = [0, 0]
            self._mouse_position_pre_grab = [0, 0]
            self._mouse_motion = [0, 0]
            self._mouse_grab_id = None

            self.quit = False
            self.last_events = None

    def update_events(self, events: list) -> None:
        self._key_grab_id = None
        self._mouse_grab_id = None
        self.last_events = events
        self._key_updated = []
        self._mouse_updated = []
        self._mouse_motion = [0, 0]
        self.quit = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                key = event.key
                self._key_down[key] = True
                self._key_updated.append(key)
            elif event.type == pygame.KEYUP:
                key = event.key
                self._key_down[key] = False
                self._key_updated.append(key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button = event.button
                self._mouse_down[button] = True
                self._mouse_updated.append(button)
            elif event.type == pygame.MOUSEBUTTONUP:
                button = event.button
                self._mouse_down[button] = False
                self._mouse_updated.append(button)
            elif event.type == pygame.MOUSEMOTION:
                self._mouse_position = event.pos
                self._mouse_motion = event.rel
            elif event.type == pygame.QUIT:
                self.quit = True

    def get_key_down(self, key: int, grab_id=None) -> bool:
        if self._key_grab_id is not None and self._key_grab_id != grab_id:
            return False
        if key not in self._key_updated or key not in self._key_down.keys():
            return False
        return self._key_down.get(key, False)

    def get_key_up(self, key: int, grab_id=None) -> bool:
        if self._key_grab_id is not None and self._key_grab_id != grab_id:
            return False
        if key not in self._key_updated or key not in self._key_down.keys():
            return False
        return not self._key_down.get(key, False)

    def get_key(self, key: int, grab_id=None) -> bool:
        if self._key_grab_id is not None and self._key_grab_id != grab_id:
            return False
        return self._key_down.get(key, False)

    def get_mouse_down(self, button: int, grab_id=None) -> bool:
        if self._mouse_grab_id is not None and self._mouse_grab_id != grab_id:
            return False
        if button not in self._mouse_updated or button not in self._mouse_down.keys():
            return False
        return self._mouse_down.get(button, False)

    def get_mouse_up(self, button: int, grab_id=None) -> bool:
        if self._mouse_grab_id is not None and self._mouse_grab_id != grab_id:
            return False
        if button not in self._mouse_updated or button not in self._mouse_down.keys():
            return False
        return not self._mouse_down.get(button, False)

    def get_mouse(self, button: int, grab_id=None) -> bool:
        if self._mouse_grab_id is not None and self._mouse_grab_id != grab_id:
            return False
        return self._mouse_down.get(button, False)

    def get_mouse_pos(self, grab_id=None) -> tuple:
        if self._mouse_grab_id is not None and self._mouse_grab_id != grab_id:
            return tuple(self._mouse_position_pre_grab)
        return tuple(self._mouse_position)

    def get_mouse_motion(self, grab_id=None) -> tuple:
        if self._mouse_grab_id is not None and self._mouse_grab_id != grab_id:
            return 0, 0
        return tuple(self._mouse_motion)

    def grab_keyboard(self, grab_id) -> None:
        if self._key_grab_id is None:
            self._key_grab_id = grab_id

    def release_keyboard(self):
        self._key_grab_id = None

    def grab_mouse(self, grab_id) -> None:
        if self._mouse_grab_id is None:
            self._mouse_position_pre_grab = self._mouse_position.copy()
            self._mouse_grab_id = grab_id

    def release_mouse(self):
        self._mouse_grab_id = None
