from pygame_utils.TwoScreenRenderer import TwoScreenRenderer
from PygameEngine.UI.Text import Text
from PygameEngine.Alignment import Alignment
from pygame_utils.SADLStreamPlayer import SoundPlayer
from pygame_utils.rom.rom_extract import load_sadl
from PygameEngine.UI.Button import Button
import pygame as pg


class SADLPreview(TwoScreenRenderer):
    def __init__(self):
        super(SADLPreview, self).__init__()

        self.now_playing_text = Text((self.top_group,))
        self.now_playing_text.set_font("data_permanent/fonts/font_event.png?cp1252", [9, 12], is_font_map=True)
        self.now_playing_text.world_rect.y -= 10
        self.now_playing_text.text = "Now playing:"
        self.now_playing_text.update_transformations()
        self.now_playing_text.scale_by_ratio([0.7, 0.7])
        self.now_playing_text.draw_alignment = [Alignment.CENTER, Alignment.TOP]

        self.track_name = Text((self.top_group,))
        self.track_name.set_font("data_permanent/fonts/font_event.png?cp1252", [9, 12], is_font_map=True)
        self.track_name.draw_alignment = [Alignment.CENTER, Alignment.TOP]
        self.track_name.text = "Default Track Name"
        self.track_name.world_rect.y += 10

        self.explanation_text = Text((self.btm_group,))
        self.explanation_text.set_font("data_permanent/fonts/font_event.png?cp1252", [9, 12], is_font_map=True)
        self.explanation_text.world_rect.y -= 50
        self.explanation_text.text = "Touch the headphones to play"

        self.play_btn = Button(())
        self.play_btn.post_interact = self.toggle_sound
        self.play_btn.time_interact_command = 0.09
        self.play_btn.color_key = pg.Color(0, 255, 0)

        self.track_player = SoundPlayer()
        self.playing = False

        self.sadl = None

    def load(self):
        super(SADLPreview, self).load()
        self.play_btn.load_sprite_sheet("data_permanent/sprites/headphones_play.png")
        self.btm_group.add(self.play_btn)
        self.ui_manager.clear()
        self.ui_manager.add(self.play_btn)

    def unload(self):
        super(SADLPreview, self).unload()
        self.play_btn.unload()
        self.ui_manager.clear()
        self.track_player.stop()

    def load_sound(self, path: str):
        self.stop_sound()
        self.sadl = load_sadl(path)
        self.track_name.text = path.split("/")[-1]

    def toggle_sound(self):
        if self.playing:
            self.stop_sound()
        else:
            self.start_sound()

    def start_sound(self):
        self.play_btn.set_tag("ON")
        if self.sadl and not self.playing:
            self.playing = True
            self.track_player.start_sound(self.sadl, volume=0.5)

    def stop_sound(self):
        self.play_btn.set_tag("OFF")
        self.playing = False
        self.track_player.stop()

    def update(self):
        super(SADLPreview, self).update()
        self.track_player.update_()
        self.ui_manager.update()
        self.play_btn.update_animation()

