import pg_engine as pge
import pygame as pg
from formats.place import Place
from pg_utils.rom.RomSingleton import RomSingleton
from pg_utils.TwoScreenRenderer import TwoScreenRenderer
from pg_utils.rom.rom_extract import load_smd
from pg_utils.sound.SMDLStreamPlayer import SMDLStreamPlayer


class FadeInOutBtn(pge.Button):
    def __init__(self, *args, **kwargs):
        super(FadeInOutBtn, self).__init__(*args, **kwargs)
        self.current_time = 0.0
        self.time = 1.0
        self.fade_in = True
    
    def animate(self, dt: float):
        self.current_time += dt
        if self.current_time >= self.time:
            self.current_time = 0.0
            self.fade_in = not self.fade_in
        if self.fade_in:
            self.alpha = int(255 * (self.current_time / self.time))
        else:
            self.alpha = 255 - int(255 * (self.current_time / self.time))
        super(FadeInOutBtn, self).animate(dt)


class PlacePreview(TwoScreenRenderer):
    def __init__(self, place: Place):
        super(PlacePreview, self).__init__()
        self.place = place

        self.sprite_loader = RomSingleton().get_sprite_loader()
        self.font_loader = RomSingleton().get_font_loader()
        self.inp = pge.Input()

        self.top_bg = pge.Sprite()
        self.sprite_loader.load(f"data_lt2/bg/map/map{self.place.map_image_index}", self.top_bg,
                                sprite_sheet=False, convert_alpha=False)
        self.btm_bg = pge.Sprite()
        self.sprite_loader.load(f"data_lt2/bg/map/main{self.place.background_image_index}", self.btm_bg,
                                sprite_sheet=False, convert_alpha=False)
        self.map_icon = pge.Sprite(position=[self.place.map_x - 256 // 2, self.place.map_y - 192 // 2],
                                   center=[pge.Alignment.LEFT, pge.Alignment.TOP])
        self.sprite_loader.load(f"data_lt2/ani/map/mapicon.arj", self.map_icon, sprite_sheet=True,
                                convert_alpha=False)

        self.move_mode = False
        self.move_button = pge.Button(position=[256 // 2 - 3, 192 // 2 - 3],
                                      center=[pge.Alignment.RIGHT, pge.Alignment.BOTTOM],
                                      pressed_tag="on", not_pressed_tag="off")
        self.sprite_loader.load(f"data_lt2/ani/map/movemode.arc", self.move_button, sprite_sheet=True,
                                convert_alpha=False)

        self.bgm = SMDLStreamPlayer()

        self.sprites = []
        self.objects = []
        self.exits = []

        for sprite_obj in self.place.sprites:
            if sprite_obj.filename == "":
                continue
            sprite = pge.Sprite(position=[sprite_obj.x - 256 // 2, sprite_obj.y - 192 // 2],
                                center=[pge.Alignment.LEFT, pge.Alignment.TOP],
                                color_key=pg.Color(0, 255, 0))
            self.sprite_loader.load(f"data_lt2/ani/bgani/{sprite_obj.filename}", sprite,
                                    sprite_sheet=True, convert_alpha=False)
            sprite.set_tag("gfx")
            self.sprites.append(sprite)

        for object_obj in self.place.objects:
            if object_obj.character_index == 0:
                continue
            obj = pge.Sprite(position=[object_obj.x - 256 // 2, object_obj.y - 192 // 2],
                             center=[pge.Alignment.LEFT, pge.Alignment.TOP],
                             color_key=pg.Color(0, 255, 0))
            self.sprite_loader.load(f"data_lt2/ani/eventobj/obj_{object_obj.character_index}.arc", obj,
                                    sprite_sheet=True, convert_alpha=False)
            obj.set_tag("gfx")
            self.objects.append(obj)

        for exit_obj in self.place.exits:
            if exit_obj.width == 0:
                continue
            exit_ = FadeInOutBtn(position=[exit_obj.x - 256 // 2, exit_obj.y - 192 // 2],
                                 center=[pge.Alignment.LEFT, pge.Alignment.TOP],
                                 color_key=pg.Color(0, 255, 0),
                                 pressed_tag="gfx2", not_pressed_tag="gfx")
            self.sprite_loader.load(f"data_lt2/ani/map/exit_{exit_obj.image_index}.arc", exit_,
                                    sprite_sheet=True, convert_alpha=False)
            self.exits.append(exit_)

    def update(self, dt: float):
        for sprite in self.sprites:
            sprite.animate(dt)
        for obj in self.objects:
            obj.animate(dt)
        for exit_ in self.exits:
            exit_.animate(dt)
        self.bgm.update_(dt)
        if not self.move_mode:
            self.move_button.animate(dt)
            if self.move_button.pressed(self.btm_camera, dt):
                self.move_mode = True
        else:
            for exit_ in self.exits:
                if exit_.pressed(self.btm_camera, dt):
                    break
                if exit_._pressed:
                    break
            else:
                if self.inp.get_mouse_down(1):
                    self.move_mode = False

    def draw(self):
        self.top_bg.draw(self.top_camera)
        self.map_icon.draw(self.top_camera)

        self.btm_bg.draw(self.btm_camera)

        for sprite in self.sprites:
            sprite.draw(self.btm_camera)
        for obj in self.objects:
            obj.draw(self.btm_camera)
        if not self.move_mode:
            self.move_button.draw(self.btm_camera)
        else:
            for exit_ in self.exits:
                exit_.draw(self.btm_camera)
