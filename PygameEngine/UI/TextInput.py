from .UIElement import UIElement
from .Text import Text
from ..Input import Input
import pygame as pg
import re
import random


class TextInput(UIElement, Text):
    def __init__(self, groups, default_text="Enter text..."):
        super(TextInput, self).__init__()
        Text.__init__(self, groups)
        self.value = ""
        self.valid_regex = None

        self.check_interacting = self._check_interacting
        self.interact = self._interact

        self.default_text = default_text

        self.accept_input = True

        self.grab_id = str(random.random())

    def update_display_text(self):
        if self.value == "" and self.accept_input:
            self.text = self.default_text
        else:
            self.text = self.value

    def set_font(self, font_path, size, is_font_map=False, letter_spacing=1, line_spacing=1):
        Text.set_font(self, font_path, size, is_font_map=is_font_map, letter_spacing=letter_spacing, line_spacing=1)
        self.update_display_text()

    def _check_interacting(self):
        mouse_pos = Input().get_screen_mouse_pos()
        if not self.interacting:
            if Input().get_mouse_down(1):
                if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    self.interacting = True
        else:
            if Input().get_mouse_down(1):
                if not self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    self.interacting = False
        if not self.accept_input:
            self.interacting = False

    def _interact(self):
        Input().grab_key_input(self.grab_id)
        for event in Input().last_events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.interacting = False
                    continue
                elif event.key == pg.K_BACKSPACE:
                    self.value = self.value[:-1]
                else:
                    pre_value = self.value
                    self.value += event.unicode
                    if self.valid_regex is not None:
                        if not re.match(self.valid_regex, self.value):
                            self.value = pre_value
                self.update_display_text()
