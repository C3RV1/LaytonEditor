import os

import pg_engine as pge
from pg_engine import Sprite
from pg_engine.sprite.Sprite import Frame, Tag
import pygame as pg
from formats.filesystem import NintendoDSRom
from formats.graphics.ani import AniSprite
from formats.graphics.bg import BGImage


def set_extension(path, ext):
    return os.path.splitext(path)[0] + ext


class SpriteLoaderROM(pge.SpriteLoader):
    def __init__(self, rom: NintendoDSRom, base_path=None):
        self.base_path: [str, None] = base_path
        self.rom = rom

    def load(self, path: str, sprite: Sprite, sprite_sheet=True, convert_alpha=True):
        # sprite_sheet and convert_alpha are ignored
        if self.base_path is not None:
            path = os.path.join(self.base_path, path).replace("\\", "/")
        if path not in self.rom.filenames:
            return
        path = set_extension(path, ".arc")
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
            surf = pg.Surface((w, h), flags=pg.SRCALPHA)
            for i, img in ani_sprite.images:
                img_surf = pg.surfarray.make_surface(ani_sprite.palette[img])
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
        else:
            bg_sprite = BGImage(path, rom=self.rom)
            surf = pg.surfarray.make_surface(bg_sprite.palette[bg_sprite.image])
        sprite.load_sprite(self, surf, frames, tags, vars_=vars_)
