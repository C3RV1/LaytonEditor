import PygameEngine.Sprite
import os
import shutil
import formats.graphics.ani as ani
import formats.graphics.bg as bg
import PIL.Image as imgl
import json
import pygame as pg
from pygame_utils.rom import RomSingleton
import SADLpy.SADL

EXPORT_PATH = "data_extracted"
ORIGINAL_FPS = 60
LANG = "en"


def set_extension(path, ext):
    return ".".join(path.split(".")[:-1]) + ".arc"


def load_animation(path: str, sprite: PygameEngine.Sprite.Sprite):
    rom = RomSingleton.RomSingleton().rom
    path = path.replace("?", LANG)
    path = set_extension(path, ".arc")
    export_path = EXPORT_PATH + "/" + path
    if not os.path.isfile(export_path + ".png"):
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        anim = ani.AniSprite(filename=path, rom=rom)

        # Sprite Sheet
        pil_images = []
        for i in range(len(anim.images)):
            pil_images.append(anim.extract_image_pil(i))
        width = sum([img.size[0] for img in pil_images])
        height = max([img.size[1] for img in pil_images])
        pil_sprite_sheet = imgl.new('RGB', (width, height))
        x_pos = 0
        for image in range(len(pil_images)):
            pil_sprite_sheet.paste(pil_images[image], [x_pos, 0])
            x_pos += pil_images[image].size[0]
        pil_sprite_sheet.save(export_path + ".png")

        sprite_info = {"frames": [], "meta": {"frameTags": []}}
        x_pos = 0
        for i in range(len(anim.images)):
            new_frame_info = {
                "frame": {"x": x_pos,
                          "y": 0,
                          "w": pil_images[i].size[0],
                          "h": pil_images[i].size[1]},
                "duration": None
            }
            sprite_info["frames"].append(new_frame_info)
            x_pos += pil_images[0].size[0]

        for i in range(len(anim.animations)):
            anim_anim: ani.Animation = anim.animations[i]
            new_tag_info = {
                "name": anim_anim.name,
                "frames": list(map(lambda x: x.image_index, anim_anim.frames)),
                "child_x": anim_anim.child_image_x,
                "child_y": anim_anim.child_image_y,
                "child_index": anim_anim.child_image_animation_index
            }
            durations = list(map(lambda x: x.duration, anim_anim.frames))
            for frame_num in range(len(anim_anim.frames)):
                frame = anim_anim.frames[frame_num].image_index
                duration = int(durations[frame_num] * 1000) // ORIGINAL_FPS  # Frames to ms
                sprite_info["frames"][frame]["duration"] = duration
            sprite_info["meta"]["frameTags"].append(new_tag_info)

        with open(export_path + ".json", "w") as anim_file:
            anim_file.write(json.dumps(sprite_info, indent=4))
    sprite.load_sprite_sheet(export_path)
    sprite.set_color_key(pg.color.Color(0, 255, 0))
    sprite.dirty = 1


def load_bg(path: str, sprite: PygameEngine.Sprite.Sprite):
    rom = RomSingleton.RomSingleton().rom
    path = path.replace("?", LANG)
    path = set_extension(path, ".arc")
    export_path = EXPORT_PATH + "/" + path + ".png"
    if not os.path.isfile(export_path):
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        bg_img = bg.BGImage(filename=path, rom=rom)
        bg_img.extract_image_pil().save(export_path)
    sprite.load(export_path)
    sprite.dirty = 1


def load_effect(path: str) -> SADLpy.SADL.SADL:
    rom = RomSingleton.RomSingleton().rom
    path = path.replace("?", LANG)
    sad_export_path = EXPORT_PATH + "/" + path

    if not os.path.isfile(sad_export_path):
        os.makedirs(os.path.dirname(sad_export_path), exist_ok=True)
        sound_data = rom.files[rom.filenames.idOf(path)]
        with open(sad_export_path, "wb") as sad_export_file:
            sad_export_file.write(sound_data)

    sadl = SADLpy.SADL.SADL(sad_export_path, 0, True)
    sadl.read_file()
    return sadl


def clear_extracted():
    if os.path.isdir(EXPORT_PATH):
        shutil.rmtree(EXPORT_PATH)
