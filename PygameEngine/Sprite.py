import pygame as pg
import json
from .Debug import Debug
from .Alignment import Alignment
from typing import Optional


class Sprite(pg.sprite.DirtySprite):
    ALIGNMENT_TOP = Alignment.TOP
    ALIGNMENT_CENTER = Alignment.CENTER
    ALIGNMENT_BOTTOM = Alignment.BOTTOM
    ALIGNMENT_RIGHT = Alignment.RIGHT
    ALIGNMENT_LEFT = Alignment.LEFT

    ASPECT_RATIO_MAX = 0
    ASPECT_RATIO_MIN = 1

    sprite_cache = {}

    def __init__(self, groups, world_rect=pg.Rect(0, 0, 0, 0),
                 draw_alignment=(Alignment.CENTER, Alignment.CENTER), is_world=True):
        pg.sprite.DirtySprite.__init__(self, groups)
        self.__path: Optional[str] = None
        self.__original_image: Optional[pg.Surface] = None
        self.__original_size = [0, 0]
        self.__scale_ratio = [1, 1]
        self.__flipped = [False, False]
        self.__angle = 0
        self.__color_key: Optional[pg.Color] = None
        self.__alpha: Optional[int] = None

        self.world_rect = world_rect.copy()
        self.rect = pg.Rect(0, 0, 0, 0)
        self.world_source_rect: Optional[pg.rect.Rect] = None

        self.draw_alignment = list(draw_alignment)

        self.is_world = is_world

        self.__is_sprite_sheet = False
        self.frame_num: Optional[int] = None
        self.frame_count: Optional[int] = None
        self.sprite_sheet_info: Optional[dict] = None
        self.__frame_source_rect: Optional[pg.rect.Rect] = None

        self.current_camera = None
        self.cam_updated = False
        self.cam_scale = 1

        self.__should_transform = False

        self.image: Optional[pg.Surface] = None

    def load(self, path, convert_alpha=True, from_cache=True):
        self.__path = path
        if path in Sprite.sprite_cache.keys() and from_cache:
            self.__original_image = Sprite.sprite_cache[path]
        else:
            self.__original_image = pg.image.load(path)
            if convert_alpha:
                self.__original_image = self.__original_image.convert_alpha()
            else:
                self.__original_image = self.__original_image.convert()
            Sprite.sprite_cache[path] = self.__original_image
        self.image = self.__original_image.copy()
        self.__scale_ratio = [1, 1]
        self.__is_sprite_sheet = False
        self.frame_num = None
        self.frame_count = None
        self.sprite_sheet_info = None
        self.__frame_source_rect = None
        self.__reset_world_rect()
        self.__should_transform = True

    def __reset_world_rect(self):
        self.world_rect.w = self.__original_image.get_rect().w
        self.world_rect.h = self.__original_image.get_rect().h
        self.__original_size = [self.world_rect.w, self.world_rect.h]
        self.__flipped = [False, False]
        self.scale_by_ratio(self.__scale_ratio)
        # self.cam_scale = 1
        self.__should_transform = True

    def load_sprite_sheet(self, path, convert_alpha=True):
        self.load(path, convert_alpha=convert_alpha)

        sprite_sheet_info_file = open(path + ".json", "r")
        self.sprite_sheet_info = json.loads(sprite_sheet_info_file.read())
        self.frame_count = len(self.sprite_sheet_info["frames"])
        sprite_sheet_info_file.close()
        self.__is_sprite_sheet = True
        self.set_frame(0)

    def set_frame(self, frame=None):
        if not self.__is_sprite_sheet:
            return
        if self.__frame_source_rect is None:
            self.__frame_source_rect = pg.Rect(0, 0, 0, 0)
        if frame is None:
            frame = self.frame_num
        elif frame >= self.frame_count or frame < 0:
            Debug.log_warning(f"Trying to set frame {frame} with frame count {self.frame_count}, clipping.", self)
            frame = max(0, frame)
            frame = min(self.frame_count, frame)
        self.frame_num = frame
        self._update_frame_info()

    def _update_frame_info(self):
        if not self.__is_sprite_sheet:
            Debug.log_warning("Trying to update frame info in no sprite sheet", self)
            return
        self.__frame_source_rect.x = self.sprite_sheet_info["frames"][self.frame_num]["frame"]["x"]
        self.__frame_source_rect.y = self.sprite_sheet_info["frames"][self.frame_num]["frame"]["y"]
        self.__frame_source_rect.w = self.sprite_sheet_info["frames"][self.frame_num]["frame"]["w"]
        self.__frame_source_rect.h = self.sprite_sheet_info["frames"][self.frame_num]["frame"]["h"]
        self.world_rect.w = self.__frame_source_rect.w
        self.world_rect.h = self.__frame_source_rect.h
        self.__should_transform = True
        self.dirty = 1

    def update_frame(self):
        self.set_frame()

    def scale(self, size, conserve_aspect_ratio=False, aspect_ratio_mode=ASPECT_RATIO_MAX):
        if self.__original_size[0] == 0 or self.__original_size[1] == 0:
            return

        if conserve_aspect_ratio:
            scale_axis = 0

            # Determine which axis to scale if we are conserving the aspect ratio
            if self.world_rect.w > self.world_rect.h:
                scale_axis = 1
            if aspect_ratio_mode == self.ASPECT_RATIO_MIN:
                scale_axis = 1 - scale_axis

            if scale_axis == 0:
                scale_ratio = size[scale_axis] / self.world_rect.w
                self.world_rect.w = size[scale_axis]
                self.world_rect.h = int(scale_ratio * self.world_rect.h)
            else:
                scale_ratio = size[scale_axis] / self.world_rect.h
                self.world_rect.h = size[scale_axis]
                self.world_rect.w = int(scale_ratio * self.world_rect.w)
        else:
            self.world_rect.w = size[0]
            self.world_rect.h = size[1]

        if not self.__is_sprite_sheet:
            self.__scale_ratio[0] = self.world_rect.w / self.__original_size[0]
            self.__scale_ratio[1] = self.world_rect.h / self.__original_size[1]
        else:
            self.__scale_ratio[0] = self.world_rect.w / self.sprite_sheet_info["frames"][self.frame_num]["frame"]["w"]
            self.__scale_ratio[1] = self.world_rect.h / self.sprite_sheet_info["frames"][self.frame_num]["frame"]["h"]

        if self.__is_sprite_sheet:
            self._update_frame_info()

        self.__should_transform = True

    def scale_by_ratio(self, ratio):
        size = [self.world_rect.w, self.world_rect.h]
        size[0] = int(round(size[0] * ratio[0]))
        size[1] = int(round(size[1] * ratio[1]))
        self.scale(size)

    def unload(self):
        self.__path = None
        self.__original_image = None
        self.kill()
        self.image = None

    def update_(self):
        pass

    def flip(self, x_bool: bool, y_bool: bool):
        # XORing values so that we don't flip if we are already flipped
        x_bool = x_bool ^ self.__flipped[0]
        y_bool = y_bool ^ self.__flipped[1]
        if x_bool is False and y_bool is False:
            return
        if x_bool:
            self.__flipped[0] = not self.__flipped[0]
        if y_bool:
            self.__flipped[1] = not self.__flipped[1]

        self.__should_transform = True

    def rotate(self, angle):
        if angle == 0:
            return
        self.__angle += angle
        self.__angle %= 360
        self.__should_transform = True

    def set_rotation(self, angle):
        if angle == self.__angle:
            return
        self.__angle = angle
        self.__angle %= 360
        self.__should_transform = True

    def set_alpha(self, value):
        if value < 0:
            value = 0
        elif value > 255:
            value = 255
        self.__alpha = value
        if self.image is not None:
            self.image.set_alpha(self.__alpha)
        self.dirty = 1

    def update_transformations(self):
        if not self.__should_transform:
            return

        self.__should_transform = False
        if self.__frame_source_rect is not None:
            self.image = pg.Surface([self.__frame_source_rect.w, self.__frame_source_rect.h])
            self.image.blit(self.__original_image, dest=(0, 0), area=self.__frame_source_rect)
        else:
            self.image = self.__original_image.copy()

        self.image = pg.transform.flip(self.image, self.__flipped[0], self.__flipped[1])

        new_size = [self.image.get_rect().w, self.image.get_rect().h]
        new_size[0] = int(round(new_size[0] * self.__scale_ratio[0] * self.cam_scale))
        new_size[1] = int(round(new_size[1] * self.__scale_ratio[1] * self.cam_scale))
        self.image = pg.transform.scale(self.image, new_size)

        self.image = pg.transform.rotate(self.image, self.__angle)

        self.world_rect.w = self.image.get_rect().w / self.cam_scale
        self.world_rect.h = self.image.get_rect().h / self.cam_scale

        if not self.image.get_flags() & pg.SRCALPHA:
            self.image.set_colorkey(self.__color_key)
            self.image.set_alpha(self.__alpha)

        self.dirty = 1

    def set_color_key(self, color_key: pg.Color):
        self.__color_key = color_key
        if self.image is not None:
            self.image.set_colorkey(self.__color_key)

    def render_again(self):
        self.__should_transform = True

    @property
    def path(self):
        return self.__path

    @property
    def flipped(self):
        return self.__flipped.copy()

    @property
    def original_size(self):
        return self.__original_size.copy()

    @property
    def original_image(self):
        self.__should_transform = True
        return self.__original_image

    @original_image.setter
    def original_image(self, value):
        self.__original_image = value
        self.__reset_world_rect()
        self.__should_transform = True

    @property
    def color_key(self):
        return self.__color_key

    @color_key.setter
    def color_key(self, value):
        self.set_color_key(value)

    @property
    def is_sprite_sheet(self):
        return self.__is_sprite_sheet

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, value):
        self.set_rotation(value)

    @property
    def alpha(self):
        return self.__alpha

    @alpha.setter
    def alpha(self, value):
        self.set_alpha(value)

    @property
    def should_transform(self):
        return self.__should_transform

    @staticmethod
    def clear_cache():
        Sprite.sprite_cache = {}
