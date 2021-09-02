import math
from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING, Tuple

import pygame as pg

from ..Camera import Camera
from ..Renderable import Renderable

if TYPE_CHECKING:
    from.SpriteLoader import SpriteLoader


@dataclass
class Frame:
    x: int
    y: int
    w: int
    h: int

    @property
    def rect(self):
        return pg.Rect(self.x, self.y, self.w, self.h)

    @property
    def position(self):
        return self.x, self.y

    @property
    def size(self):
        return self.w, self.h


@dataclass
class Tag:
    name: str
    frames: List[int]
    frame_durations: List[float]
    vars_: dict = field(default_factory=dict)


class Sprite(Renderable):
    SNAP_MAX = 0
    SNAP_MIN = 1

    def __init__(self, rotation=0, scale=None, flipped=None, special_flags=0, color_key=None, alpha=None, **kwargs):
        super().__init__(**kwargs)
        if scale is None:
            scale = [1, 1]
        if flipped is None:
            flipped = [False, False]
        self._surf: [pg.Surface] = None
        # Surface or cropped surface size depending on whether is sprite sheet or not
        self._size = (0, 0)
        self._real_size = [0, 0]
        self._cropped_surf: [pg.Surface] = None
        self._scale = scale
        self._rotation = rotation
        self._transformed_surf: [pg.Surface] = None

        self._frame_info: List[Frame] = []
        self._active_frame: Frame = None

        self._tag_info: List[Tag] = []
        self._active_tag: Tag = None
        self._tag_time: float = 0.0
        self._tag_frame: int = 0

        self._transform_needed = True
        self._cam_zoom = [1, 1]
        self._flipped = flipped
        self.special_flags = special_flags
        self._color_key = color_key
        self._alpha = alpha

        self._loader = None

        self.vars = {}

    def load_sprite(self, loader: 'SpriteLoader', surface: pg.Surface, frame_info, tag_info, vars_=None):
        self._loader = loader
        if vars_ is None:
            self.vars = {}
        else:
            self.vars = vars_
        self._surf: pg.Surface = surface
        # Surface or cropped surface size depending on whether is sprite sheet or not
        self._size: tuple = surface.get_size()
        self._cropped_surf: [pg.Surface] = None
        self._transformed_surf: [pg.Surface] = None
        self._frame_info: List[Frame] = frame_info
        self._active_frame: [Frame] = None
        self._tag_info: List[Tag] = tag_info
        self._active_tag: [Tag] = None
        self._cam_zoom = [1, 1]
        self._transform_needed = True

        # Set frame if in sprite sheet
        self.set_frame(0)
        self.predict_real_size()

    def _update_cropped(self):
        if not self._active_frame:
            return
        self._cropped_surf = pg.Surface(self._active_frame.size, flags=self._surf.get_flags())
        self._cropped_surf.blit(self._surf, (0, 0), area=self._active_frame.rect)
        self._size = self._cropped_surf.get_size()
        self.predict_real_size()
        self._transform_needed = True

    def set_frame(self, num: int):
        if num < len(self._frame_info):
            if self._frame_info[num] != self._active_frame:
                self._active_frame = self._frame_info[num]
                self._update_cropped()

    def set_tag(self, name: str):
        for tag in self._tag_info:
            if tag.name == name:
                if tag != self._active_tag:
                    self._active_tag = tag
                    self._tag_time = 0.0
                    self._tag_frame = 0
                    if len(tag.frames) > 0:
                        self.set_frame(tag.frames[0])
                return
        return

    def set_tag_by_num(self, num: int):
        if num >= len(self._tag_info):
            return
        self.set_tag(self._tag_info[num].name)

    def animate(self, dt: float):
        if not self._tag_info:
            pass
        if self._active_tag not in self._tag_info:
            return
        tag = self._active_tag
        if len(self._active_tag.frames) == 0:
            return
        self._tag_time += dt
        duration = tag.frame_durations[self._tag_frame]
        while self._tag_time > duration != 0:
            self._tag_frame += 1
            self._tag_frame %= len(tag.frames)
            self._tag_time -= duration
            duration = tag.frame_durations[self._tag_frame]
        self.set_frame(tag.frames[self._tag_frame])

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, v: float):
        if v == self._rotation:
            return
        self._rotation = v
        self._transform_needed = True
        self.predict_real_size()

    def predict_real_size(self):
        w, h = self._size
        if self._rotation != 0:
            rotation = self._rotation % 180
            if rotation >= 90:
                w, h = h, w
                rotation -= 90
            rotation_rad = rotation * math.pi / 180.0
            new_w = math.ceil(w * math.cos(rotation_rad) + h * math.sin(rotation_rad))
            new_h = math.ceil(w * math.sin(rotation_rad) + h * math.cos(rotation_rad))
            self._real_size = [new_w, new_h]
        else:
            self._real_size = self._size

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, v: list):
        if v == self._scale:
            return
        self._scale[0] = v[0]
        self._scale[1] = v[1]
        self.predict_real_size()
        self._transform_needed = True

    def set_size(self, new_size: list, conserve_ratio=False, ratio_type=SNAP_MAX):
        if self._size[0] == 0 or self._size[1] == 0:
            return
        if not conserve_ratio:
            self._scale[0] = new_size[0] / self._size[0]
            self._scale[1] = new_size[1] / self._size[1]
        else:
            # Axis to scale
            scale_axis = int(self._size[0] > self._size[1])

            if ratio_type == self.SNAP_MIN:
                scale_axis = 1 - scale_axis

            self._scale[scale_axis] = new_size[scale_axis] / self._size[scale_axis]
            self._scale[1 - scale_axis] = self._scale[scale_axis]
        self.predict_real_size()
        self._transform_needed = True

    @property
    def surf(self):
        return self._surf

    @surf.setter
    def surf(self, v: pg.Surface):
        if v == self._surf:
            return
        self._surf = v
        self._size = self._surf.get_size()
        self.predict_real_size()
        # update cropped if sprite_sheet
        self._update_cropped()
        self._transform_needed = True

    @property
    def flipped(self):
        return self._flipped

    @flipped.setter
    def flipped(self, v: list):
        if self._flipped == v:
            return
        self._flipped[0] = v[0]
        self._flipped[1] = v[1]
        self._transform_needed = True

    # TRUTH TABLE
    # FLIP  FLIPPED     NEXT
    # F     F           F
    # T     F           T
    # F     T           T
    # T     T           F
    def flip(self, x: bool, y: bool):
        self._flipped[0] = self._flipped[0] ^ x
        self._flipped[1] = self._flipped[1] ^ y

    def _force_transform(self, calculate=False):
        self._transform_needed = True
        if calculate:
            self._update_transforms(None)

    def _update_transforms(self, cam: [Camera]):
        if self._surf is None:
            self.visible = False
            self._transform_needed = False
        if not self._transform_needed:
            if cam:
                if cam.zoom == self._cam_zoom:
                    return
            else:
                return
        if cam:
            self._cam_zoom[0] = cam.zoom[0]
            self._cam_zoom[1] = cam.zoom[1]

        surf = self._cropped_surf.copy() if self._cropped_surf else self._surf.copy()

        if self._flipped[0] or self._flipped[1]:
            surf = pg.transform.flip(surf, self._flipped[0], self._flipped[1])

        size = list(self._size)
        if cam:
            size[0] *= self._scale[0] * cam.zoom[0]
            size[1] *= self._scale[1] * cam.zoom[1]
        size[0] = int(size[0])
        size[1] = int(size[1])
        if cam:
            if self._scale != [1, 1] or cam.zoom != [1, 1]:
                surf = pg.transform.scale(surf, size)
        else:
            if self._scale != [1, 1]:
                surf = pg.transform.scale(surf, size)

        if self._rotation != 0:
            surf = pg.transform.rotate(surf, self._rotation)

        _real_size = list(surf.get_size())
        if cam:
            _real_size[0] /= cam.zoom[0]
            _real_size[1] /= cam.zoom[1]
            self._real_size = _real_size

        if not cam:
            return
        self._transformed_surf = surf
        self._transform_needed = False

        if not self._transformed_surf.get_flags() & pg.SRCALPHA:
            if self._color_key:
                self._transformed_surf.set_colorkey(self._color_key)
            if self._alpha is not None:
                self._transformed_surf.set_alpha(int(self._alpha))

    @property
    def color_key(self):
        return self._color_key

    @color_key.setter
    def color_key(self, v: pg.Color):
        if v == self._color_key:
            return
        self._color_key = v
        if self._transformed_surf:
            if self._transformed_surf.get_flags() & pg.SRCALPHA:
                self._transformed_surf.set_colorkey(self._color_key)

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, v: float):
        if v == self._alpha:
            return
        self._alpha = v
        if self._transformed_surf:
            if self._transformed_surf.get_flags() & pg.SRCALPHA:
                self._transformed_surf.set_alpha(int(self._alpha))

    def get_world_rect(self) -> pg.Rect:
        return pg.Rect(self.position[0] - self._real_size[0] * self.center[0],
                       self.position[1] - self._real_size[1] * self.center[1],
                       self._real_size[0], self._real_size[1])

    def get_screen_rect(self, cam: Camera, update_pos=True) -> Tuple[pg.Rect, pg.Rect]:
        self._position_to_screen(cam)
        size = list(self._real_size)
        size[0] *= cam.zoom[0]
        size[1] *= cam.zoom[1]
        r = [self._screen_position[0], self._screen_position[1], size[0], size[1]]
        r[0] -= size[0] * self.center[0]
        r[1] -= size[1] * self.center[1]
        clip = cam.clip_rect(r)
        return pg.Rect(r), pg.Rect(clip)

    def draw(self, cam: Camera):
        super(Sprite, self).draw(cam)
        if self._surf is None:
            return
        self._update_transforms(cam)
        position, clip = self.get_screen_rect(cam, update_pos=False)
        if self.visible:
            cam.surf.blit(self._transformed_surf, (position.x, position.y), area=clip, special_flags=self.special_flags)

    def set_loader(self, loader: 'SpriteLoader'):
        self._loader = loader

    # TODO: Implement some sort of unload? or does python automatically collect it correctly?
