from pygame_utils.TwoScreenRenderer import TwoScreenRenderer
from PygameEngine.UI.Text import Text
from PygameEngine.Alignment import Alignment
from pygame_utils.SADLStreamPlayer import SADLStreamPlayer
from pygame_utils.SMDLStreamPlayer import SMDLStreamPlayer
from pygame_utils.StreamPlayerAbstract import StreamPlayerAbstract
from pygame_utils.rom.rom_extract import load_sadl, load_smd
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

        self.sadl_player = SADLStreamPlayer()
        self.smdl_player = SMDLStreamPlayer()
        self.current_player: StreamPlayerAbstract = StreamPlayerAbstract()
        self.snd_obj = None
        self.playing = False

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
        self.current_player.stop()

    def load_sadl(self, path: str):
        self.stop_sound()
        self.snd_obj = load_sadl(path)
        self.current_player = self.sadl_player
        self.track_name.text = path.split("/")[-1]
        if self.check_playable():
            self.explanation_text.text = "Touch the headphones to play"
            self.play_btn.set_tag("OFF")
        else:
            self.explanation_text.text = "Missing dependencies"
            self.play_btn.set_tag("CAN'T BE PLAYED")

    def load_smdl(self, path):
        self.stop_sound()
        self.snd_obj, presets = load_smd(path)
        self.current_player = self.smdl_player
        self.current_player.set_preset_dict(presets)
        self.track_name.text = path.split("/")[-1]
        if self.check_playable():
            self.explanation_text.text = "Touch the headphones to play"
            self.play_btn.set_tag("OFF")
        else:
            self.explanation_text.text = "Missing dependencies"
            self.play_btn.set_tag("CAN'T BE PLAYED")

    def check_playable(self):
        return self.current_player.get_playable()

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
            self.current_player.start_sound(self.snd_obj, volume=0.5)

    def stop_sound(self):
        self.play_btn.set_tag("OFF")
        self.playing = False
        self.current_player.stop()

    def update(self):
        super(SADLPreview, self).update()
        self.current_player.update_()
        self.ui_manager.update()
        self.play_btn.update_animation()

