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
    return ".".join(path.split(".")[:-1]) + ext


def load_animation(path: str, sprite: PygameEngine.Sprite.Sprite):
    rom = RomSingleton.RomSingleton().rom
    path = path.replace("?", LANG)
    path = set_extension(path, ".arc")
    export_path = EXPORT_PATH + "/" + path
    if not rom.filenames.idOf(path):
        print(f"Warning: could not load {path}")
        sprite.original_image = pg.Surface((10, 10))
        return False
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

        sprite_info = {"frames": [], "meta": {"frameTags": [], "drawoff": None}}
        if "drawoff" in anim.variables.keys():
            sprite_info["meta"]["drawoff"] = anim.variables["drawoff"]
        x_pos = 0
        for i in range(len(anim.images)):
            new_frame_info = {
                "frame": {"x": x_pos,
                          "y": 0,
                          "w": pil_images[i].size[0],
                          "h": pil_images[i].size[1]},
            }
            sprite_info["frames"].append(new_frame_info)
            x_pos += pil_images[i].size[0]

        for i in range(len(anim.animations)):
            anim_anim: ani.Animation = anim.animations[i]
            new_tag_info = {
                "name": anim_anim.name,
                "frames": [anim_anim.frames[i].image_index for i in range(len(anim_anim.frames))],
                "child_x": anim_anim.child_image_x,
                "child_y": anim_anim.child_image_y,
                "child_index": anim_anim.child_image_animation_index,
                "frame_durations": [int(anim_anim.frames[i].duration * 1000) // ORIGINAL_FPS for i in range(len(anim_anim.frames))]
            }
            sprite_info["meta"]["frameTags"].append(new_tag_info)

        with open(export_path + ".png.json", "w") as anim_file:
            anim_file.write(json.dumps(sprite_info, indent=4))
    sprite.load_sprite_sheet(export_path + ".png")
    sprite.set_color_key(pg.color.Color(0, 255, 0))
    sprite.dirty = 1
    return True


def load_bg(path: str, sprite: PygameEngine.Sprite.Sprite):
    rom = RomSingleton.RomSingleton().rom
    path = path.replace("?", LANG)
    path = set_extension(path, ".arc")
    export_path = EXPORT_PATH + "/" + path + ".png"
    if not rom.filenames.idOf(path):
        print(f"Warning: could not load {path}")
        sprite.original_image = pg.Surface((10, 10))
        return
    if not os.path.isfile(export_path):
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        bg_img = bg.BGImage(filename=path, rom=rom)
        bg_img.extract_image_pil().save(export_path)
    sprite.load(export_path)
    sprite.dirty = 1


def load_sadl(path: str, rom=None) -> SADLpy.SADL.SADL:
    if rom is None:
        rom = RomSingleton.RomSingleton().rom
    path = path.replace("?", LANG)
    sad_export_path = EXPORT_PATH + "/" + path
    sound_data = rom.files[rom.filenames.idOf(path)]

    # if not os.path.isfile(sad_export_path):
    #     os.makedirs(os.path.dirname(sad_export_path), exist_ok=True)
    #     with open(sad_export_path, "wb") as sad_export_file:
    #         sad_export_file.write(sound_data)

    sadl = SADLpy.SADL.SADL(sad_export_path, 0)
    sadl.read_file(sound_data)

    return sadl


def clear_extracted():
    if os.path.isdir(EXPORT_PATH):
        shutil.rmtree(EXPORT_PATH)
