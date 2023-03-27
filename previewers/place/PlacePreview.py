import k4pg
import pygame as pg
from formats.place import Place, PlaceSprite, PlaceObject, PlaceExit, PlaceHintCoin, PlaceComment
from pg_utils.rom.RomSingleton import RomSingleton
from pg_utils.rom.loaders import SpriteLoaderROM
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


class TranslucentOverlay(k4pg.Sprite):
    def __init__(self, place, *args, **kwargs):
        super(TranslucentOverlay, self).__init__(*args, **kwargs)
        self._inner = place

    def generate(self):
        surface = pg.Surface((256, 192), flags=pg.SRCALPHA)

        overlay_cam = k4pg.Camera(surface, alignment=pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP))

        for hint_coin in self._inner.hint_coins:
            hc_rect = pg.Rect(hint_coin.x, hint_coin.y, hint_coin.width, hint_coin.height)
            k4pg.draw.rect(overlay_cam, pg.Color(230, 212, 14), hc_rect)
        for comment in self._inner.comments:
            comment_rect = pg.Rect(comment.x, comment.y, comment.width, comment.height)
            k4pg.draw.rect(overlay_cam, pg.Color(14, 212, 230), comment_rect)
        for obj in self._inner.objects:
            obj_rect = pg.Rect(obj.x, obj.y, obj.width, obj.height)
            k4pg.draw.rect(overlay_cam, pg.Color(14, 230, 21), obj_rect)

        self.surf = surface


class SpriteLive(k4pg.Sprite):
    def __init__(self, place_sprite: PlaceSprite, *args, **kwargs):
        super(SpriteLive, self).__init__(*args, **kwargs)
        self._inner = place_sprite
        self._filename = ""

    def update(self):
        self.loader: SpriteLoaderROM
        self.position.update(self._inner.x - 256 // 2, self._inner.y - 192 // 2)

        if self._filename == self._inner.filename:
            return

        self._filename = self._inner.filename
        if self._filename != "":
            self.loader.load(f"data_lt2/ani/bgani/{self._filename}", self,
                             sprite_sheet=True, convert_alpha=False)
            self.set_tag("gfx")
            self.visible = True
        else:
            self.visible = False


class ObjectLive(k4pg.Sprite):
    def __init__(self, place_object: PlaceObject, overlay: TranslucentOverlay, *args, **kwargs):
        super(ObjectLive, self).__init__(*args, **kwargs)
        self._inner = place_object
        self._overlay = overlay
        self._x = self._inner.x
        self._y = self._inner.y
        self._width = self._inner.width
        self._height = self._inner.height
        self._character_index = -1

    def update(self):
        self.position.update(self._inner.x - 256 // 2, self._inner.y - 192 // 2)

        if self._character_index != self._inner.character_index:
            self.update_character_index()

        different_position = self._x != self._inner.x or self._y != self._inner.y
        different_size = self._width != self._inner.width or self._height != self._inner.height

        if different_position or different_size:
            self._x, self._y = self._inner.x, self._inner.y
            self._width, self._height = self._inner.width, self._inner.height
            self._overlay.generate()

    def update_character_index(self):
        self.loader: SpriteLoaderROM
        self._character_index = self._inner.character_index

        if self._character_index != 0:
            self.loader.load(f"data_lt2/ani/eventobj/obj_{self._character_index}.arc", self,
                             sprite_sheet=True, convert_alpha=False)
            self.set_tag("gfx")
            self.visible = True
        else:
            self.visible = False


class ExitLive(FadeInOutBtn):
    def __init__(self, place_exit: PlaceExit, *args, **kwargs):
        super(ExitLive, self).__init__(*args, **kwargs)
        self._inner = place_exit
        self._image_index = -1

    def update(self):
        self.loader: SpriteLoaderROM
        self.position.update(self._inner.x - 256 // 2, self._inner.y - 192 // 2)
        self.visible = self._inner.event_or_place_index != 0

        if self._image_index == self._inner.image_index:
            return

        self._image_index = self._inner.image_index
        self.loader.load(f"data_lt2/ani/map/exit_{self._image_index}.arc", self,
                         sprite_sheet=True, convert_alpha=False)


class HintCoinLive:
    def __init__(self, place_hint_coin: PlaceHintCoin, overlay: TranslucentOverlay):
        self._inner = place_hint_coin
        self._overlay = overlay

        self._x = self._inner.x
        self._y = self._inner.y
        self._width = self._inner.width
        self._height = self._inner.height

    def update(self):
        different_pos = self._x != self._inner.x or self._y != self._inner.y
        different_width = self._width != self._inner.width or self._height != self._inner.height

        if not (different_pos or different_width):
            return

        self._x = self._inner.x
        self._y = self._inner.y
        self._width = self._inner.width
        self._height = self._inner.height
        self._overlay.generate()


class CommentLive:  # TODO: On click show comment
    def __init__(self, place_comment: PlaceComment, overlay: TranslucentOverlay):
        self._inner = place_comment
        self._overlay = overlay
        self._x = self._inner.x
        self._y = self._inner.y
        self._width = self._inner.width
        self._height = self._inner.height

    def update(self):
        different_pos = self._x != self._inner.x or self._y != self._inner.y
        different_width = self._width != self._inner.width or self._height != self._inner.height

        if not (different_pos or different_width):
            return

        self._x = self._inner.x
        self._y = self._inner.y
        self._width = self._inner.width
        self._height = self._inner.height
        self._overlay.generate()


class PlacePreview(TwoScreenRenderer):
    OVERLAY_ACTIVE = True  # keep overlay active between different previews

    def __init__(self, place: Place):
        super(PlacePreview, self).__init__()
        self.show_cursor_pos = True

        self.place = place

        self.sprite_loader = RomSingleton().get_sprite_loader()
        self.sprite_loader_os = k4pg.SpriteLoaderOS(base_path_os="data_permanent/sprites")
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
        self.sprite_loader.load(f"data_lt2/ani/map/mapicon.arj", self.map_icon, True,
                                convert_alpha=False)

        self.move_mode = False
        self.move_button = k4pg.ButtonSprite(position=pg.Vector2(256 // 2 - 3, 192 // 2 - 3),
                                             center=pg.Vector2(k4pg.Alignment.RIGHT, k4pg.Alignment.BOTTOM),
                                             pressed_tag="on", not_pressed_tag="off")
        self.sprite_loader.load(f"data_lt2/ani/map/movemode.arc", self.move_button, True,
                                convert_alpha=False)

        self.music = SMDLStreamPlayer()

        self.sprites = []
        self.objects = []
        self.exits = []
        self.hint_coins = []
        self.comments = []
        self.overlay = TranslucentOverlay(self.place, alpha=180)

        for sprite_obj in self.place.sprites:
            sprite = SpriteLive(sprite_obj, center=pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP),
                                color_key=pg.Color(0, 255, 0))
            sprite.set_loader(self.sprite_loader)
            self.sprites.append(sprite)

        for object_obj in self.place.objects:
            obj = ObjectLive(object_obj, self.overlay, center=pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP),
                             color_key=pg.Color(0, 255, 0))
            obj.set_loader(self.sprite_loader)
            self.objects.append(obj)

        for exit_obj in self.place.exits:
            exit_ = ExitLive(exit_obj, center=pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP),
                             color_key=pg.Color(0, 255, 0),
                             pressed_tag="gfx2", not_pressed_tag="gfx")
            exit_.set_loader(self.sprite_loader)
            self.exits.append(exit_)

        for hint_coin_obj in self.place.hint_coins:
            hint_coin = HintCoinLive(hint_coin_obj, self.overlay)
            self.hint_coins.append(hint_coin)

        for comment_obj in self.place.comments:
            comment = CommentLive(comment_obj, self.overlay)
            self.comments.append(comment)

        self.overlay.generate()

        self.overlay_toggle = k4pg.ButtonSprite(position=pg.Vector2(-128 + 5, -96 + 5), scale=pg.Vector2(0.5, 0.5),
                                                center=pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP),
                                                color_key=pg.Color(0, 255, 0),
                                                pressed_counter=0.05)
        self.sprite_loader_os.load("overlay_icon.png", self.overlay_toggle, sprite_sheet=True, convert_alpha=False)
        self.overlay_toggle.set_tag("OFF" if PlacePreview.OVERLAY_ACTIVE else "ON")

    def update(self, dt: float):
        for sprite in self.sprites:
            sprite.update()
            sprite.animate(dt)
        for obj in self.objects:
            obj.update()
            obj.animate(dt)
        for exit_ in self.exits:
            exit_.update()
            exit_.animate(dt)
        for hint_coin in self.hint_coins:
            hint_coin.update()
        for comment in self.comments:
            comment.update()

        self.music.update(dt)

        if self.overlay_toggle.get_pressed(self.btm_camera):
            PlacePreview.OVERLAY_ACTIVE = not PlacePreview.OVERLAY_ACTIVE
            self.overlay_toggle.set_tag("OFF" if PlacePreview.OVERLAY_ACTIVE else "ON")

        if not self.move_mode:
            self.move_button.animate(dt)
            if self.move_button.get_pressed(self.btm_camera):
                self.move_mode = True
        else:
            for exit_ in self.exits:
                if exit_.get_pressed(self.btm_camera):
                    break
                if exit_._pressed:
                    break
            else:
                if self.inp.get_mouse_down(1):
                    self.move_mode = False
        
        super(PlacePreview, self).update(dt)

    def draw(self):
        self.top_bg.draw(self.top_camera)
        self.map_icon.draw(self.top_camera)

        self.btm_bg.draw(self.btm_camera)

        for sprite in self.sprites:
            sprite.draw(self.btm_camera)
        for obj in self.objects:
            obj.draw(self.btm_camera)

        if PlacePreview.OVERLAY_ACTIVE:
            self.overlay.draw(self.btm_camera)
        
        if not self.move_mode:
            self.move_button.draw(self.btm_camera)
        else:
            for exit_ in self.exits:
                exit_.draw(self.btm_camera)

        self.overlay_toggle.draw(self.btm_camera)
        super(PlacePreview, self).draw()
