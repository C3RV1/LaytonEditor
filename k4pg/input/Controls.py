from .Input import JOYSTICK_BUTTONS, JOYSTICK_AXIS, JOYSTICK_HATS, Input
import pygame as pg


class Controls:
    def __init__(self, *args, **kwargs):
        super(Controls, self).__init__(*args, **kwargs)

    def up(self):
        return False

    def down(self):
        return False

    def right(self):
        return False

    def left(self):
        return False

    def confirm(self):
        return False

    def back(self):
        return False


class KeyBoardControls(Controls):
    def __init__(self, *args, **kwargs):
        super(KeyBoardControls, self).__init__(*args, **kwargs)
        self.inp = Input()

    def up(self):
        return self.inp.get_key_down(pg.K_UP)

    def down(self):
        return self.inp.get_key_down(pg.K_DOWN)

    def right(self):
        return self.inp.get_key_down(pg.K_RIGHT)

    def left(self):
        return self.inp.get_key_down(pg.K_LEFT)

    def confirm(self):
        return self.inp.get_key_down(pg.K_RETURN)

    def back(self):
        return self.inp.get_key_down(pg.K_ESCAPE)


class JoystickControls(Controls):
    def __init__(self, joy_id, *args, **kwargs):
        super(JoystickControls, self).__init__(*args, **kwargs)
        self.inp = Input()
        self.joy_id = joy_id
        self.pressed_before = {}

    def up(self):
        v = False
        if self.inp.get_joystick_button_down(self.joy_id, JOYSTICK_BUTTONS.UP):
            v = True
        if self.inp.last_axis(self.joy_id):
            if self.inp.get_joystick_axes(self.joy_id, JOYSTICK_AXIS.HORIZONTAL)[1] < -0.5:
                v = True
        else:
            if self.inp.get_joystick_hat(self.joy_id, JOYSTICK_HATS.HAT)[1] > 0.5:
                v = True
        if v:
            if self.pressed_before.get(0, False):
                return False
            self.pressed_before[0] = True
            return True
        else:
            self.pressed_before[0] = False
            return False

    def down(self):
        v = False
        if self.inp.get_joystick_button_down(self.joy_id, JOYSTICK_BUTTONS.DOWN):
            v = True
        if self.inp.last_axis(self.joy_id):
            if self.inp.get_joystick_axes(self.joy_id, JOYSTICK_AXIS.HORIZONTAL)[1] > 0.5:
                v = True
        else:
            if self.inp.get_joystick_hat(self.joy_id, JOYSTICK_HATS.HAT)[1] < -0.5:
                v = True
        if v:
            if self.pressed_before.get(1, False):
                return False
            self.pressed_before[1] = True
            return True
        else:
            self.pressed_before[1] = False
            return False

    def right(self):
        v = False
        if self.inp.get_joystick_button_down(self.joy_id, JOYSTICK_BUTTONS.RIGHT):
            v = True
        if self.inp.last_axis(self.joy_id):
            if self.inp.get_joystick_axes(self.joy_id, JOYSTICK_AXIS.HORIZONTAL)[0] > 0.5:
                v = True
        else:
            if self.inp.get_joystick_hat(self.joy_id, JOYSTICK_HATS.HAT)[0] > 0.5:
                v = True
        if v:
            if self.pressed_before.get(2, False):
                return False
            self.pressed_before[2] = True
            return True
        else:
            self.pressed_before[2] = False
            return False

    def left(self):
        v = False
        if self.inp.get_joystick_button_down(self.joy_id, JOYSTICK_BUTTONS.LEFT):
            v = True
        if self.inp.last_axis(self.joy_id):
            if self.inp.get_joystick_axes(self.joy_id, JOYSTICK_AXIS.HORIZONTAL)[0] < -0.5:
                v = True
        else:
            if self.inp.get_joystick_hat(self.joy_id, JOYSTICK_HATS.HAT)[0] < -0.5:
                v = True
        if v:
            if self.pressed_before.get(3, False):
                return False
            self.pressed_before[3] = True
            return True
        else:
            self.pressed_before[3] = False
            return False

    def confirm(self):
        return self.inp.get_joystick_button_down(self.joy_id, JOYSTICK_BUTTONS.A)

    def back(self):
        return self.inp.get_joystick_button_down(self.joy_id, JOYSTICK_BUTTONS.B)
