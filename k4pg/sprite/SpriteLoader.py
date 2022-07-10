import os
import pygame as pg
from k4pg.sprite.Sprite import Sprite, Tag, Frame
import json


class SpriteLoader:
    def load(self, path: str, sprite: Sprite, sprite_sheet=False, convert_alpha=True, do_copy=False):
        pass


class SpriteLoaderOS(SpriteLoader):
    CACHE = {}

    def __init__(self, base_path_os=None):
        self.base_path = base_path_os

    def load(self, path: str, sprite: Sprite, sprite_sheet=False, convert_alpha=True, do_copy=False):
        if self.base_path:
            path = os.path.join(self.base_path, path)
        if path in SpriteLoaderOS.CACHE:
            surf, frame_info, tag_info = SpriteLoaderOS.CACHE[path]
        else:
            if not os.path.isfile(path):
                return
            if sprite_sheet and not os.path.isfile(path + ".json"):
                sprite_sheet = False
            surf = pg.image.load(path)
            if convert_alpha:
                surf = surf.convert_alpha()
            else:
                surf = surf.convert()
            frame_info = []
            tag_info = []
            if sprite_sheet:
                with open(path + ".json", "r") as json_file:
                    data = json.loads(json_file.read())

                for frame in data["frames"]:
                    frame_data = frame["frame"]
                    frame_info.append(Frame(frame_data["x"], frame_data["y"], frame_data["w"], frame_data["h"]))

                for tag in data["meta"]["frameTags"]:
                    frames = []
                    frame_durations = []
                    if "frames" in tag:
                        frames = tag["frames"]
                    elif "from" in tag and "to" in tag:
                        frames = list(range(tag["from"], tag["to"] + 1))
                    if "durations" in tag:
                        for duration in tag["durations"]:
                            frame_durations.append(duration / 1000.0)
                    else:
                        for frame in frames:
                            frame_durations.append(data["frames"][frame]["duration"] / 1000.0)
                    tag_info.append(Tag(tag["name"], frames, frame_durations))
                SpriteLoaderOS.CACHE[path] = [surf, frame_info, tag_info]
        if not do_copy:
            sprite.load_sprite(self, surf, frame_info, tag_info)
        else:
            sprite.load_sprite(self, surf.copy(), frame_info.copy(), tag_info.copy())
