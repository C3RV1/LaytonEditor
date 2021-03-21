import pygame
from .Joysticks import Joysticks
from .Debug import Debug


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
            self._key_down_dict = {}
            self._key_updated = []

            self._mouse_down_dict = {}
            self._mouse_updated = []

            self._joystick_manager = Joysticks()

            self._joystick_dict = {}
            self._joystick_updated = {}
            self._joystick_axis = {}
            for joystick in self._joystick_manager.joy_order:
                self._joystick_dict[joystick] = {}
                self._joystick_axis[joystick] = {}
                self._joystick_updated[joystick] = []
            self.quit = False
            self.last_events = None
            self._key_grab_id = None
            self._mouse_grab_id = None

    def update_events(self, events):
        self._key_grab_id = None
        self._mouse_grab_id = None
        self.last_events = events
        self._key_updated = []
        self._mouse_updated = []
        self.quit = False
        for joy_number in self._joystick_updated.keys():
            self._joystick_updated[joy_number] = []
        for event in events:
            if event.type == pygame.KEYDOWN:
                key = event.key
                self._key_down_dict[key] = True
                self._key_updated.append(key)
            elif event.type == pygame.KEYUP:
                key = event.key
                self._key_down_dict[key] = False
                self._key_updated.append(key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button = event.button
                self._mouse_down_dict[button] = True
                self._mouse_updated.append(button)
            elif event.type == pygame.MOUSEBUTTONUP:
                button = event.button
                self._mouse_down_dict[button] = False
                self._mouse_updated.append(button)
            elif event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                joy_id = event.joy
                if joy_id not in self._joystick_manager.joy_order:
                    Debug.log_warning("Joy {} event, but not in joy_order", "Input Manager")
                    continue
                joy_number = self._joystick_manager.joy_order.index(joy_id)
                self._joystick_dict[joy_number][button] = True
                self._joystick_updated[joy_number].append(button)
            elif event.type == pygame.JOYBUTTONUP:
                button = event.button
                joy_id = event.joy
                if joy_id not in self._joystick_manager.joy_order:
                    Debug.log_warning("Joy {} event, but not in joy_order", "Input Manager")
                    continue
                joy_number = self._joystick_manager.joy_order.index(joy_id)
                self._joystick_dict[joy_number][button] = False
                self._joystick_updated[joy_number].append(button)
            elif event.type == pygame.JOYAXISMOTION:
                joy_id = event.joy
                axis = event.axis
                if joy_id not in self._joystick_manager.joy_order:
                    Debug.log_warning("Joy {} event, but not in joy_order", "Input Manager")
                    continue
                joy_number = self._joystick_manager.joy_order.index(joy_id)
                if axis not in self._joystick_axis[joy_number].keys():
                    self._joystick_axis[joy_number][axis] = 0
                self._joystick_axis[joy_number][axis] = event.value
            elif event.type == pygame.QUIT:
                self.quit = True

    def get_key_down(self, key, grab_id=None):
        if self._key_grab_id is not None and self._key_grab_id != grab_id:
            return False
        if key not in self._key_updated or key not in self._key_down_dict.keys():
            return False
        is_key_down = self._key_down_dict.get(key, False)
        return is_key_down

    def get_key_up(self, key, grab_id=None):
        if self._key_grab_id is not None and self._key_grab_id != grab_id:
            return False
        if key not in self._key_updated or key not in self._key_down_dict.keys():
            return False
        is_key_down = self._key_down_dict.get(key, False)
        return not is_key_down

    def get_key(self, key, grab_id=None):
        if self._key_grab_id is not None and self._key_grab_id != grab_id:
            return False
        return self._key_down_dict.get(key, False)

    def get_mouse_down(self, button, grab_id=None):
        if self._mouse_grab_id is not None and self._mouse_grab_id != grab_id:
            return False
        if button not in self._mouse_updated or button not in self._mouse_down_dict.keys():
            return False
        is_button_down = self._mouse_down_dict.get(button, False)
        return is_button_down

    def get_mouse_up(self, button, grab_id=None):
        if self._mouse_grab_id is not None and self._mouse_grab_id != grab_id:
            return False
        if button not in self._mouse_updated or button not in self._mouse_down_dict.keys():
            return False
        is_button_down = self._mouse_down_dict.get(button, False)
        return not is_button_down

    def get_mouse(self, button, grab_id=None):
        if self._mouse_grab_id is not None and self._mouse_grab_id != grab_id:
            return False
        return self._mouse_down_dict.get(button, False)

    def get_joystick_button_down(self, joy_number, button):
        if joy_number < 0 or joy_number >= self._joystick_manager.joystick_count:
            Debug.log_error("Requested joystick_button from joystick {}, out of range".format(joy_number), self)
            return False
        if button not in self._joystick_dict[joy_number].keys() or button not in self._joystick_updated[joy_number]:
            return False
        is_button_down = self._joystick_dict[joy_number][button]
        return is_button_down

    def get_joystick_button_up(self, joy_number, button):
        if joy_number < 0 or joy_number >= self._joystick_manager.joystick_count:
            Debug.log_error("Requested joystick_button from joystick {}, out of range".format(joy_number), self)
            return False
        if button not in self._joystick_dict[joy_number].keys() or button not in self._joystick_updated[joy_number]:
            return False
        is_button_down = self._joystick_dict[joy_number][button]
        return not is_button_down

    def get_joystick_button(self, joy_number, button):
        if joy_number < 0 or joy_number >= self._joystick_manager.joystick_count:
            Debug.log_error("Requested joystick_button from joystick {}, out of range".format(joy_number), self)
            return False
        if button not in self._joystick_dict[joy_number].keys():
            return False
        return self._joystick_dict[joy_number][button]

    def get_joystick_axis(self, joy_number, axis):
        if joy_number < 0 or joy_number >= self._joystick_manager.joystick_count:
            Debug.log_error("Requested joystick_axis from joystick {}, out of range".format(joy_number), self)
            return 0
        if axis not in self._joystick_axis[joy_number].keys():
            return 0
        return self._joystick_axis[joy_number][axis]

    @staticmethod
    def get_screen_mouse_pos():
        mouse_pos = pygame.mouse.get_pos()
        return mouse_pos

    def grab_key_input(self, grab_id):
        self._key_grab_id = grab_id

    def grab_mouse_input(self, grab_id):
        self._mouse_grab_id = grab_id
