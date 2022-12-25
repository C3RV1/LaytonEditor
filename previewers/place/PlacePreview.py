import k4pg
import pygame as pg
from formats.place import Place
from pg_utils.rom.RomSingleton import RomSingleton
from pg_utils.TwoScreenRenderer import TwoScreenRenderer
from pg_utils.sound.SMDLStreamPlayer import SMDLStreamPlayer


class FadeInOutBtn(k4pg.ButtonSprite):
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
        self.inp = k4pg.Input()

        self.top_bg = k4pg.Sprite()
        self.sprite_loader.load(f"data_lt2/bg/map/map{self.place.map_image_index}", self.top_bg,
                                sprite_sheet=False, convert_alpha=False)
        self.btm_bg = k4pg.Sprite()
        self.sprite_loader.load(f"data_lt2/bg/map/main{self.place.background_image_index}", self.btm_bg,
                                sprite_sheet=False, convert_alpha=False)
        self.map_icon = k4pg.Sprite(position=pg.Vector2(self.place.map_x - 256 // 2, self.place.map_y - 192 // 2),
                                    center=pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP))
        self.sprite_loader.load(f"data_lt2/ani/map/mapicon.arj", self.map_icon,
                                convert_alpha=False)

        self.move_mode = False
        self.move_button = k4pg.ButtonSprite(position=pg.Vector2(256 // 2 - 3, 192 // 2 - 3),
                                             center=[k4pg.Alignment.RIGHT, k4pg.Alignment.BOTTOM],
                                             pressed_tag="on", not_pressed_tag="off")
        self.sprite_loader.load(f"data_lt2/ani/map/movemode.arc", self.move_button,
                                convert_alpha=False)

        self.bgm = SMDLStreamPlayer()

        self.sprites = []
        self.objects = []
        self.exits = []

        for sprite_obj in self.place.sprites:
            if sprite_obj.filename == "":
                continue
            sprite = k4pg.Sprite(position=pg.Vector2(sprite_obj.x - 256 // 2, sprite_obj.y - 192 // 2),
                                 center=pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP),
                                 color_key=pg.Color(0, 255, 0))
            self.sprite_loader.load(f"data_lt2/ani/bgani/{sprite_obj.filename}", sprite,
                                    sprite_sheet=True, convert_alpha=False)
            sprite.set_tag("gfx")
            self.sprites.append(sprite)

        for object_obj in self.place.objects:
            if object_obj.width <= 0:
                continue
            obj = k4pg.Sprite(position=pg.Vector2(object_obj.x - 256 // 2, object_obj.y - 192 // 2),
                              center=pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP),
                              color_key=pg.Color(0, 255, 0))
            if object_obj.character_index != 0:
                self.sprite_loader.load(f"data_lt2/ani/eventobj/obj_{object_obj.character_index}.arc", obj,
                                        sprite_sheet=True, convert_alpha=False)
                obj.set_tag("gfx")
            self.objects.append(obj)

        for exit_obj in self.place.exits:
            if exit_obj.width <= 0:
                continue
            exit_ = FadeInOutBtn(position=pg.Vector2(exit_obj.x - 256 // 2, exit_obj.y - 192 // 2),
                                 center=pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP),
                                 color_key=pg.Color(0, 255, 0),
                                 pressed_tag="gfx2", not_pressed_tag="gfx")
            self.sprite_loader.load(f"data_lt2/ani/map/exit_{exit_obj.image_index}.arc", exit_,
                                    sprite_sheet=True, convert_alpha=False)
            self.exits.append(exit_)

        overlay = pg.Surface((256, 192), flags=pg.SRCALPHA)
        overlay_cam = k4pg.Camera(overlay, alignment=pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP))

        for hint_coin in self.place.hintcoins:
            hc_rect = pg.Rect(hint_coin.x, hint_coin.y, hint_coin.width, hint_coin.height)
            k4pg.draw.rect(overlay_cam, pg.Color(230, 212, 14), hc_rect)
        for comment in self.place.comments:
            comment_rect = pg.Rect(comment.x, comment.y, comment.width, comment.height)
            k4pg.draw.rect(overlay_cam, pg.Color(14, 212, 230), comment_rect)
        for obj in self.place.objects:
            obj_rect = pg.Rect(obj.x, obj.y, obj.width, obj.height)
            k4pg.draw.rect(overlay_cam, pg.Color(14, 230, 21), obj_rect)

        self.overlay_sprite = k4pg.Sprite()
        self.overlay_sprite.surf = overlay
        self.overlay_sprite.alpha = 180

        self.sprite_loader_os = k4pg.SpriteLoaderOS(base_path_os="data_permanent/sprites")
        self.overlay_toggle = k4pg.ButtonSprite(pressed_counter=0.05)
        self.overlay_toggle.position = pg.Vector2(-128 + 5, -96 + 5)
        self.overlay_toggle.scale = pg.Vector2(0.5, 0.5)
        self.overlay_toggle.center = pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP)
        self.sprite_loader_os.load("overlay_icon.png", self.overlay_toggle, sprite_sheet=True, convert_alpha=False)
        self.overlay_toggle.color_key = pg.Color(0, 255, 0)
        self.overlay_toggle.set_tag("OFF")

        self.overlay_active = True

    def update(self, dt: float):
        for sprite in self.sprites:
            sprite.animate(dt)
        for obj in self.objects:
            obj.animate(dt)
        for exit_ in self.exits:
            exit_.animate(dt)

        self.bgm.update(dt)

        if self.overlay_toggle.get_pressed(self.btm_camera, dt):
            self.overlay_active = not self.overlay_active
            self.overlay_toggle.set_tag("OFF" if self.overlay_active else "ON")

        if not self.move_mode:
            self.move_button.animate(dt)
            if self.move_button.get_pressed(self.btm_camera, dt):
                self.move_mode = True
        else:
            for exit_ in self.exits:
                if exit_.get_pressed(self.btm_camera, dt):
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

        if self.overlay_active:
            self.overlay_sprite.draw(self.btm_camera)
        
        if not self.move_mode:
            self.move_button.draw(self.btm_camera)
        else:
            for exit_ in self.exits:
                exit_.draw(self.btm_camera)

        self.overlay_toggle.draw(self.btm_camera)
