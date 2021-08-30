import os

import pg_engine as pge
from formats import conf
from pg_engine import Sprite
from pg_engine.sprite.Sprite import Frame, Tag
import pygame as pg
from formats.filesystem import NintendoDSRom
from formats.graphics.ani import AniSprite
from formats.graphics.bg import BGImage
import numpy as np


def set_extension(path, ext):
    return os.path.splitext(path)[0] + ext


class SpriteLoaderROM(pge.SpriteLoaderOS):
    def __init__(self, rom: NintendoDSRom, base_path=None, base_os_path=None):
        super(SpriteLoaderROM, self).__init__(base_path=base_os_path)
        self._base_rom_path = base_path
        self.rom = rom

    def load(self, path: str, sprite: Sprite, sprite_sheet=True, convert_alpha=False, do_copy=False):
        # sprite_sheet and convert_alpha are ignored
        if self._base_rom_path is not None:
            path = os.path.join(self._base_rom_path, path).replace("\\", "/")
        path = path.replace("?", conf.LANG)
        path = set_extension(path, ".arc")
        if path not in self.rom.filenames:
            super().load(path + ".png", sprite, sprite_sheet=sprite_sheet, convert_alpha=convert_alpha,
                         do_copy=do_copy)
            return
        frames = []
        tags = []
        vars_ = {}
        if sprite_sheet:
            ani_sprite = AniSprite(path, rom=self.rom)
            w, h = 0, 0
            for img in ani_sprite.images:
                img_h, img_w = img.shape
                h = max(img_h, h)
                frames.append(Frame(w, 0, img_w, img_h))
                w += img_w
            surf = pg.Surface((w, h))
            for i, img in enumerate(ani_sprite.images):
                array_surf = ani_sprite.palette[img][:, :, :-1]
                array_surf = np.swapaxes(array_surf, 0, 1)
                img_surf = pg.surfarray.make_surface(array_surf)
                surf.blit(img_surf, frames[i].position)

            for animation in ani_sprite.animations:
                vars_ = dict()
                vars_["child_index"] = animation.child_image_animation_index
                vars_["child_x"] = animation.child_image_x
                vars_["child_y"] = animation.child_image_y
                tags.append(Tag(
                    animation.name,
                    [f.image_index for f in animation.frames],
                    [f.duration for f in animation.frames],
                    vars_=vars_
                ))

            vars_.update(ani_sprite.variables)
            vars_["child_image"] = ani_sprite.child_image
            color_key = pg.Color(0, 255, 0)
        else:
            bg_sprite = BGImage(path, rom=self.rom)
            img_array = bg_sprite.palette[bg_sprite.image][:,:,:-1]
            img_array = np.swapaxes(img_array, 0, 1)
            surf = pg.surfarray.make_surface(img_array)
            color_key = None
        sprite.load_sprite(self, surf, frames, tags, vars_=vars_)
        sprite.color_key = color_key
