from typing import Any

from pg_utils.TwoScreenRenderer import TwoScreenRenderer
import pg_engine as pge
from pg_utils.sound.StreamPlayerAbstract import StreamPlayerAbstract
from pg_utils.rom.RomSingleton import RomSingleton
import pygame as pg


class SoundPreview(TwoScreenRenderer):
    def __init__(self, player: StreamPlayerAbstract, snd_obj: Any, name: str):
        super(SoundPreview, self).__init__()

        self.sprite_loader = RomSingleton().get_sprite_loader()
        self.sprite_loader_os = pge.SpriteLoaderOS(base_path_os="data_permanent/sprites")
        self.font_loader = RomSingleton().get_font_loader()

        self.now_playing_text = pge.Text(position=[0, -10], center=[pge.Alignment.CENTER, pge.Alignment.BOTTOM],
                                         scale=[1, 1])
        self.font_loader.load("font_event", 12, self.now_playing_text)
        self.now_playing_text.text = "Now playing:"

        self.track_name = pge.Text(position=[0, 10], center=[pge.Alignment.CENTER, pge.Alignment.TOP])
        self.font_loader.load("font_event", 12, self.track_name)
        self.track_name.text = name.replace("\\", "/").split("/")[-1]

        self.explanation_text = pge.Text(position=[0, -50])
        self.font_loader.load("font_event", 12, self.explanation_text)
        self.explanation_text.text = "Touch the headphones to play"

        self.play_btn = pge.Button(pressed_counter=0.09)
        self.sprite_loader_os.load("headphones_play.png", self.play_btn, sprite_sheet=True, convert_alpha=False)
        self.play_btn.color_key = pg.Color(0, 255, 0)

        self.volume_slider = pge.Slider(min_value=0, max_value=1, start_value=0.5)
        self.sprite_loader_os.load("slider_main.png", self.volume_slider, sprite_sheet=False)
        self.sprite_loader_os.load("slider_ball.png", self.volume_slider.child, sprite_sheet=False)
        self.volume_slider.center = [pge.Alignment.CENTER, pge.Alignment.BOTTOM]
        self.volume_slider.position[1] = 192 // 2 - 20

        self.player: StreamPlayerAbstract = player
        self.player.set_volume(0.5)
        self.snd_obj: Any = snd_obj
        self.playing = False
        if self.check_playable():
            self.explanation_text.text = "Touch the headphones to play"
            self.play_btn.set_tag("OFF")
        else:
            self.explanation_text.text = "Missing dependencies"
            self.play_btn.set_tag("CAN'T BE PLAYED")

    def unload(self):
        super(SoundPreview, self).unload()
        self.now_playing_text.unload()
        self.track_name.unload()
        self.explanation_text.unload()
        self.play_btn.unload()
        self.player.stop()

    def check_playable(self):
        return self.player.get_playable()

    def toggle_sound(self):
        if not self.check_playable():
            return
        if self.playing:
            self.stop_sound()
        else:
            self.start_sound()

    def start_sound(self):
        self.play_btn.set_tag("ON")
        if self.snd_obj and not self.playing:
            self.playing = True
            self.player.start_sound(self.snd_obj, loops=True)

    def stop_sound(self):
        self.play_btn.set_tag("OFF")
        self.playing = False
        self.player.stop()

    def update(self, dt: float):
        if self.play_btn.pressed(self.btm_camera, dt):
            self.toggle_sound()
        self.play_btn.animate(dt)
        self.player.update(dt)

    def draw(self):
        self.top_camera.surf.fill((40, 40, 40))
        self.now_playing_text.draw(self.top_camera)
        self.track_name.draw(self.top_camera)
        self.play_btn.draw(self.btm_camera)
        self.explanation_text.draw(self.btm_camera)
        slider_value, changed = self.volume_slider.get_value(self.btm_camera)
        if changed:
            self.player.set_volume(slider_value)
        self.volume_slider.draw(self.btm_camera)
