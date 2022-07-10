import pygame


class JOYSTICK_BUTTONS:
    A = 0
    B = 1
    X = 2
    Y = 3
    R = 7
    L = -1
    ZR = 9
    ZL = -1
    PLUS = 11
    MINUS = 10
    DOWN = 12
    LEFT = 13
    UP = 11
    RIGHT = 14


class JOYSTICK_HATS:
    HAT = 0


class JOYSTICK_AXIS:
    HORIZONTAL = 0
    VERTICAL = 1


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
            self._mouse_position_updated = False
            self._mouse_position_pre_grab = [0, 0]
            self._mouse_motion = [0, 0]
            self._mouse_grab_id = None

            self._joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
            for joystick in self._joysticks:
                joystick.init()
            self._joystick_buttons_down = [{} for _ in range(pygame.joystick.get_count())]
            self._joystick_buttons_updated = [[] for _ in range(pygame.joystick.get_count())]
            self._joystick_axes = [{} for _ in range(pygame.joystick.get_count())]
            self._joystick_hat = [[0, 0] for _ in range(pygame.joystick.get_count())]
            self._joystick_hat_or_axis = [0 for _ in range(pygame.joystick.get_count())]

            self.quit = False
            self.last_events = None

    @property
    def joystick_count(self):
        return len(self._joysticks)

    def update_events(self, events: list) -> None:
        self._key_grab_id = None
        self._mouse_grab_id = None
        self._mouse_position_updated = False
        self.last_events = events
        self._key_updated = []
        self._mouse_updated = []
        self._mouse_motion = [0, 0]
        self._joystick_buttons_updated = [[] for _ in range(len(self._joysticks))]
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
                self._mouse_position_updated = True
            elif event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.JOYAXISMOTION:
                self._joystick_axes[event.joy][event.axis] = event.value
                self._joystick_hat_or_axis[event.joy] = 0
            elif event.type == pygame.JOYHATMOTION:
                self._joystick_hat[event.joy] = event.value
                self._joystick_hat_or_axis[event.joy] = 1
            elif event.type == pygame.JOYBUTTONDOWN:
                print(event.button)
                self._joystick_buttons_down[event.joy][event.button] = True
                self._joystick_buttons_updated[event.joy].append(event.button)
            elif event.type == pygame.JOYBUTTONUP:
                self._joystick_buttons_down[event.joy][event.button] = False
                self._joystick_buttons_updated[event.joy].append(event.button)
            elif event.type == pygame.JOYDEVICEADDED:
                print("DEVICE ADDED", event)

    def get_key_down(self, key: int, grab_id=None) -> bool:
        if self._key_grab_id is not None and self._key_grab_id != grab_id:
            return False
        if key not in self._key_updated:
            return False
        return self._key_down.get(key, False)

    def get_key_up(self, key: int, grab_id=None) -> bool:
        if self._key_grab_id is not None and self._key_grab_id != grab_id:
            return False
        if key not in self._key_updated:
            return False
        return not self._key_down.get(key, True)

    def get_key(self, key: int, grab_id=None) -> bool:
        if self._key_grab_id is not None and self._key_grab_id != grab_id:
            return False
        return self._key_down.get(key, False)

    def get_mouse_down(self, button: int, grab_id=None) -> bool:
        if self._mouse_grab_id is not None and self._mouse_grab_id != grab_id:
            return False
        if button not in self._mouse_updated:
            return False
        return self._mouse_down.get(button, False)

    def get_mouse_up(self, button: int, grab_id=None) -> bool:
        if self._mouse_grab_id is not None and self._mouse_grab_id != grab_id:
            return False
        if button not in self._mouse_updated:
            return False
        return not self._mouse_down.get(button, True)

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

    def get_joystick_button_down(self, joy_id: int, button: int):
        if button not in self._joystick_buttons_updated[joy_id]:
            return False
        return self._joystick_buttons_down[joy_id].get(button, False)

    def get_joystick_button_up(self, joy_id: int, button: int):
        if button not in self._joystick_buttons_updated[joy_id]:
            return False
        return not self._joystick_buttons_down[joy_id].get(button, True)

    def get_joystick_button(self, joy_id: int, button: int):
        return self._joystick_buttons_down[joy_id].get(button, False)

    def get_joystick_axes(self, joy_id: int, axes: int):
        if axes not in self._joystick_axes[joy_id]:
            return {0: 0, 1: 0}
        return self._joystick_axes[joy_id]

    def get_joystick_hat(self, joy_id: int, hat: int):
        if hat not in self._joystick_hat[joy_id]:
            return [0, 0]
        return self._joystick_hat[joy_id]

    def last_axis(self, joy_id):
        return self._joystick_hat_or_axis[joy_id] == 0

    def mouse_moved(self, grab_id=None):
        if self._mouse_grab_id is not None and self._mouse_grab_id != grab_id:
            return False
        return self._mouse_position_updated

    def grab_keyboard(self, grab_id) -> None:
        if self._key_grab_id is None:
            self._key_grab_id = grab_id

    def release_keyboard(self):
        self._key_grab_id = None

    def grab_mouse(self, grab_id) -> None:
        if self._mouse_grab_id is None:
            self._mouse_position_pre_grab = self._mouse_position
            self._mouse_grab_id = grab_id

    def release_mouse(self):
        self._mouse_grab_id = None
