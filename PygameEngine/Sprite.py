import pygame as pg
import json


class Sprite(pg.sprite.DirtySprite):
    ALIGNMENT_TOP = 0
    ALIGNMENT_CENTER = 1
    ALIGNMENT_BOTTOM = 2
    ALIGNMENT_RIGHT = 0
    ALIGNMENT_LEFT = 2

    ASPECT_RATIO_MAX = 0
    ASPECT_RATIO_MIN = 1

    images_global = {}
    scales_global = {}

    def __init__(self, groups):
        pg.sprite.DirtySprite.__init__(self, groups)
        self.path = None
        self.world_rect = pg.Rect(0, 0, 0, 0)
        self.rect = pg.Rect(0, 0, 0, 0)
        self._original_size = [0, 0]
        self.scale_ = [1, 1]
        self.flipped = [False, False]
        self.color_key: pg.Color = None

        self.draw_alignment = [Sprite.ALIGNMENT_CENTER, Sprite.ALIGNMENT_CENTER]

        self.is_world = True

        self.is_sprite_sheet = False
        self.frame = None
        self.frame_count = None
        self.sprite_sheet_info = None
        self.source_rect_pre: pg.rect.Rect = None

        self.current_camera = None
        self.cam_updated = False
        self.cam_scale = 1

    def load(self, path, convert_alpha=True, from_cache=True):
        self.path = path
        if path in Sprite.images_global.keys() and from_cache:
            self.image = Sprite.images_global[path]
        else:
            self.image = pg.image.load(path)
            if convert_alpha:
                self.image = self.image.convert_alpha()
            else:
                self.image = self.image.convert()
            Sprite.images_global[path] = self.image
        self.scale_ = [1, 1]
        self.is_sprite_sheet = False
        self.frame = None
        self.frame_count = None
        self.sprite_sheet_info = None
        self.source_rect_pre: pg.rect.Rect = None
        self.reset_world_rect()

    def reset_world_rect(self):
        self.world_rect.w = self.image.get_rect().w
        self.world_rect.h = self.image.get_rect().h
        self._original_size = [self.world_rect.w, self.world_rect.h]
        self.cam_scale = 1
        self.flipped = [False, False]

    def load_sprite_sheet(self, path, convert_alpha=True):
        self.load(path + ".png", convert_alpha=convert_alpha)

        sprite_sheet_info_file = open(path + ".json", "r")
        self.sprite_sheet_info = json.loads(sprite_sheet_info_file.read())
        self.frame_count = len(self.sprite_sheet_info)
        sprite_sheet_info_file.close()
        self.is_sprite_sheet = True
        self.set_frame(0)

    def set_frame(self, frame=None):
        if not self.is_sprite_sheet:
            return
        if self.source_rect_pre is None:
            self.source_rect_pre = pg.Rect(0, 0, 0, 0)
        if frame is None:
            frame = self.frame
        self.frame = frame
        self._update_frame_info()

    def _update_frame_info(self):
        self.source_rect_pre.x = self.sprite_sheet_info["frames"][self.frame]["frame"]["x"] * self.scale_[0]
        self.source_rect_pre.y = self.sprite_sheet_info["frames"][self.frame]["frame"]["y"] * self.scale_[1]
        self.source_rect_pre.w = self.sprite_sheet_info["frames"][self.frame]["frame"]["w"] * self.scale_[0]
        self.source_rect_pre.h = self.sprite_sheet_info["frames"][self.frame]["frame"]["h"] * self.scale_[1]
        self.world_rect.w = self.source_rect_pre.w
        self.world_rect.h = self.source_rect_pre.h
        self.dirty = 1

    def update_frame(self):
        self.set_frame()

    def scale(self, size, conserve_aspect_ratio=False, aspect_ratio_mode=ASPECT_RATIO_MAX):
        if self.world_rect.w == 0 or self.world_rect.h == 0:
            return
        if conserve_aspect_ratio:
            scale_axis = 0
            if self.world_rect.w > self.world_rect.h:
                scale_axis = 1
            if aspect_ratio_mode == self.ASPECT_RATIO_MIN:
                scale_axis = 1 - scale_axis
            if scale_axis == 0:
                scale_factor = size[scale_axis] / self.world_rect.w
                self.world_rect.w = size[scale_axis]
                self.world_rect.h = int(round(scale_factor) * self.world_rect.h)
            else:
                scale_factor = size[scale_axis] / self.world_rect.h
                self.world_rect.h = size[scale_axis]
                self.world_rect.w = int(round(scale_factor) * self.world_rect.w)
            self.scale_[0] = scale_factor
            self.scale_[1] = scale_factor
        else:
            self.scale_[0] = size[0] / self.world_rect.w
            self.scale_[1] = size[1] / self.world_rect.h

            self.world_rect.w = size[0]
            self.world_rect.h = size[1]

        new_size = self._original_size.copy()
        new_size[0] = int(round(new_size[0] * self.scale_[0] * self.cam_scale))
        new_size[1] = int(round(new_size[1] * self.scale_[1] * self.cam_scale))

        self.image = pg.transform.scale(self.image, new_size)
        self.image.set_colorkey(self.color_key)

        if self.is_sprite_sheet:
            self._update_frame_info()

        self.dirty = 1

    def scale_by_factor(self, factor):
        size = [self.world_rect.w, self.world_rect.h]
        size[0] = int(round(size[0] * factor[0]))
        size[1] = int(round(size[1] * factor[1]))
        self.scale(size)

    def unload(self):
        self.path = None
        self.image = None

    def update_(self):
        pass

    def flip(self, xbool: bool, ybool: bool):
        # XORing values
        xbool = xbool ^ self.flipped[0]
        ybool = ybool ^ self.flipped[1]
        if xbool is False and ybool is False:
            return
        if xbool:
            self.flipped[0] = not self.flipped[0]
        if ybool:
            self.flipped[1] = not self.flipped[1]
        self.image = pg.transform.flip(self.image, xbool, ybool)
        if self.sprite_sheet_info is not None:
            if xbool:
                for frame in self.sprite_sheet_info["frames"]:
                    frame["frame"]["x"] = self._original_size[0] - frame["frame"]["x"] - frame["frame"]["w"]
            if ybool:
                for frame in self.sprite_sheet_info["frames"]:
                    frame["frame"]["y"] = self._original_size[0] - frame["frame"]["y"] - frame["frame"]["h"]
            self.update_frame()
        self.image.set_colorkey(self.color_key)

    def set_color_key(self, color_key: pg.Color):
        self.color_key = color_key
        self.image.set_colorkey(self.color_key)

    @staticmethod
    def clear_cache():
        Sprite.images_global = {}
        Sprite.scales_global = {}
