import logging
import math
from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING, Tuple, Dict

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
    draw_off: List[pg.Vector2] = field(default_factory=list)
    child_x: int = 0
    child_y: int = 0
    child_index: int = 0


class Sprite(Renderable):
    SNAP_MAX = 0
    SNAP_MIN = 1

    def __init__(self, *args, rotation=0, scale=None, flipped=None, special_flags=0, color_key=None, alpha=None,
                 **kwargs):
        super().__init__(*args, **kwargs)
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
        self.transformed_surf: Dict[int, pg.Surface] = {}

        self._frame_info: List[Frame] = []
        self._active_frame: [Frame] = None

        self._tag_info: List[Tag] = []
        self._active_tag: [Tag] = None
        self._tag_time: float = 0.0
        self._tag_frame: int = 0

        self._transform_needed = {}
        self._cam_zoom: Dict[int, List[int]] = {}
        self._flipped = flipped
        self.special_flags = special_flags
        self._color_key = color_key
        self._alpha = alpha

        self.loader = None

        self.vars = {}

    def load_sprite(self, loader: 'SpriteLoader', surface: pg.Surface, frame_info, tag_info, vars_=None):
        self.loader = loader
        if vars_ is None:
            self.vars = {}
        else:
            self.vars = vars_
        self._surf: pg.Surface = surface
        # Surface or cropped surface size depending on whether is sprite sheet or not
        self._size: tuple = surface.get_size()
        self._cropped_surf: [pg.Surface] = None
        self.transformed_surf: Dict[pg.Surface] = {}
        self._frame_info: List[Frame] = frame_info
        self._active_frame: [Frame] = None
        self._tag_info: List[Tag] = tag_info
        self._active_tag: [Tag] = None
        self._cam_zoom: Dict[List[int]] = {}
        self._force_transform(False)

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
        self._force_transform(False)

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
        logging.warning(f"Sprite tag not found (tag: {name}, "
                        f"tags: {[tag.name for tag in self._tag_info]})")
        return

    def set_tag_by_num(self, num: int):
        if num < 0:
            num = len(self._tag_info) + num
        if num >= len(self._tag_info):
            logging.warning(f"Sprite tag num bigger than number of animations (num: {num}, "
                            f"count: {len(self._tag_info)})")
            return
        self.set_tag(self._tag_info[num].name)

    @property
    def tag_count(self) -> int:
        return len(self._tag_info)

    @property
    def tag_names(self) -> List[str]:
        return [tag.name for tag in self._tag_info]

    def get_tag(self) -> Tag:
        return self._active_tag

    def get_tag_num(self) -> int:
        if self._active_tag not in self._tag_info:
            return None
        return self._tag_info.index(self._active_tag)

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
        self._rotation %= 360
        self._force_transform(False)
        self.predict_real_size()

    def predict_real_size(self):
        w, h = self._size
        w *= self._scale[0]
        h *= self._scale[1]
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
            self._real_size = [w, h]

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
        self._force_transform(False)

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
        self._force_transform(False)

    @property
    def surf(self) -> pg.Surface:
        return self._surf

    @surf.setter
    def surf(self, v: pg.Surface):
        if v == self._surf:
            return
        self._surf = v
        if self._surf is None:
            return
        self._size = self._surf.get_size()
        self.predict_real_size()
        # update cropped if sprite_sheet
        self._update_cropped()
        self._force_transform(False)

    def surf_updated(self):
        self._force_transform(False)

    @property
    def flipped(self):
        return self._flipped

    @flipped.setter
    def flipped(self, v: list):
        if self._flipped == v:
            return
        self._flipped[0] = v[0]
        self._flipped[1] = v[1]
        self._force_transform(False)

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
        for cam_id in self._transform_needed:
            self._transform_needed[cam_id] = True
        if calculate:
            self.update_transforms(None)

    def update_transforms(self, cam: [Camera]):
        if self._surf is None:
            self.visible = False
            self._transform_needed[id(cam)] = False
        if id(cam) in self._transform_needed:
            if not self._transform_needed[id(cam)]:
                if cam:
                    if id(cam) in self._cam_zoom:
                        if cam.zoom == self._cam_zoom[id(cam)]:
                            return
                else:
                    return
        if id(cam) not in self._cam_zoom:
            self._cam_zoom[id(cam)] = [1, 1]
        if cam:
            self._cam_zoom[id(cam)][0] = cam.zoom[0]
            self._cam_zoom[id(cam)][1] = cam.zoom[1]

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

        # _real_size = list(surf.get_size())
        # if cam:
        #     _real_size[0] /= cam.zoom[0]
        #     _real_size[1] /= cam.zoom[1]
        #     self._real_size = _real_size
        self.predict_real_size()

        if not cam:
            return
        transformed_surf = surf
        self._transform_needed[id(cam)] = False

        if self._color_key:
            transformed_surf.set_colorkey(self._color_key)
        if self._alpha is not None:
            transformed_surf.set_alpha(int(self._alpha))

        self.transformed_surf[id(cam)] = transformed_surf

    @property
    def color_key(self):
        return self._color_key

    @color_key.setter
    def color_key(self, v: pg.Color):
        if v == self._color_key:
            return
        self._color_key = v
        for transformed_surf in self.transformed_surf.values():
            transformed_surf.set_colorkey(self._color_key)

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, v: float):
        if v == self._alpha:
            return
        self._alpha = v
        for transformed_surf in self.transformed_surf.values():
            transformed_surf.set_alpha(int(self._alpha))

    def get_draw_off(self) -> pg.Vector2:
        if self._active_tag and self._tag_frame < len(self._active_tag.draw_off):
            self._active_tag: Tag
            return self._active_tag.draw_off[self._tag_frame]
        return pg.Vector2(0, 0)

    def get_world_rect(self) -> pg.Rect:
        draw_off = self.get_draw_off()
        return pg.Rect(self.position.x - self._real_size[0] * self.center.x + draw_off.x,
                       self.position.y - self._real_size[1] * self.center.y + draw_off.y,
                       self._real_size[0], self._real_size[1])

    def _position_to_screen(self, cam: Camera):
        draw_off = self.get_draw_off()
        self.position += draw_off
        super(Sprite, self)._position_to_screen(cam)
        self.position -= draw_off

    def get_screen_rect(self, cam: Camera, update_pos=True, do_clip=True) -> Tuple[pg.Rect, pg.Rect]:
        self._position_to_screen(cam)
        size = list(self._real_size)
        size[0] *= cam.zoom[0]
        size[1] *= cam.zoom[1]
        r = [self._screen_position[0], self._screen_position[1], size[0], size[1]]
        r[0] -= size[0] * self.center.x
        r[1] -= size[1] * self.center.y
        if do_clip:
            clip = cam.clip_rect(r)
        else:
            clip = r.copy()
            clip[0] = 0
            clip[1] = 0
        r[0] = math.ceil(r[0])
        r[1] = math.ceil(r[1])
        return pg.Rect(r), pg.Rect(clip)

    def draw(self, cam: Camera):
        super(Sprite, self).draw(cam)
        if self._surf is None:
            return
        self.update_transforms(cam)
        position, clip = self.get_screen_rect(cam, update_pos=False)
        if self.visible:
            cam.surf.blit(self.transformed_surf[id(cam)], (position.x, position.y), area=clip,
                          special_flags=self.special_flags)

    def set_loader(self, loader: 'SpriteLoader'):
        self.loader = loader

    # TODO: Implement some sort of unload? or does python automatically collect it correctly?
