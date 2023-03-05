import k4pg
from .EventCharacter import EventCharacter
import pygame as pg
import pg_utils.sound.SADLStreamPlayer
from pg_utils.rom.rom_extract import load_sadl
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .EventPlayer import EventPlayer

from utility.replace_substitutions import replace_substitutions


class EventDialogue(k4pg.Sprite, k4pg.FontSupportive):
    on_dialogue: bool
    dialogue_sfx_id: int
    current_pause: int
    voice_line: int
    text_left_to_do: str
    paused: bool

    def __init__(self, event_player: 'EventPlayer', *args, **kwargs):
        super(EventDialogue, self).__init__(*args, **kwargs)
        self.event_player: 'EventPlayer' = event_player

        self.inner_text: k4pg.Text = k4pg.Text(center=pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP),
                                               line_spacing=3, color=pg.Color(0, 0, 0))

        self.char_name = k4pg.Sprite()
        self.char_name.center = pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.BOTTOM)

        self.current_cooldown = 0
        self.cooldown = 1 / 60

        self.character_talking: Optional[EventCharacter] = None

        self.voice_player = pg_utils.sound.SADLStreamPlayer.SADLStreamPlayer(loops=False)
        self.voice_player.set_volume(0.5)

        self.dialogue_sfx_player = pg_utils.sound.SADLStreamPlayer.SADLStreamPlayer(loops=False)
        self.dialogue_sfx_player.set_volume(0.5)

    def setup(self):
        self.on_dialogue = False
        self.dialogue_sfx_id = -1
        self.voice_line = -1

        self.current_pause = 0
        self.text_left_to_do = ""
        self.paused = False

    def update(self, dt: float):
        self.voice_player.update(dt)
        self.dialogue_sfx_player.update(dt)

    def unload(self):
        self.voice_player.stop()
        self.dialogue_sfx_player.stop()

    def show(self):
        self.visible = True
        self.inner_text.visible = True
        self.char_name.visible = True

    def hide(self):
        self.visible = False
        self.inner_text.visible = False
        self.char_name.visible = False

    def start_dialogue(self, character, chr_anim, text, voice, dialogue_sfx):
        self.character_talking = character
        self.reset_all()
        if self.character_talking is not None:
            self.character_talking.set_anim(chr_anim)
        self.text_left_to_do = replace_substitutions(text)
        self.voice_line = voice
        self.dialogue_sfx_id = dialogue_sfx
        self.on_dialogue = True
        self.show()
        if self.character_talking is not None:
            self.init_char_name()
        else:
            self.char_name.visible = False
        self.set_talking()

    def set_talking(self):
        # If there is a voice line play it (first we stop it)
        if self.voice_line != -1:
            sfx = load_sadl(f"data_lt2/stream/event/?/{str(self.voice_line).zfill(3)}_{self.current_pause}.SAD")
            self.voice_player.load_sound(sfx)
            self.voice_player.play()

        if self.character_talking is not None:
            self.character_talking.set_talking()

    def set_not_talking(self):
        if self.character_talking is not None:
            self.character_talking.set_not_talking()

    def load_sprite(self, loader: k4pg.SpriteLoader, surface: pg.Surface, frame_info, tag_info, vars_=None):
        super(EventDialogue, self).load_sprite(loader, surface, frame_info, tag_info, vars_=vars_)
        self.inner_text.position.update((- 256 // 2) + 10, self.get_world_rect().y + 19)
        self.char_name.position.update(- 256 // 2 + 2, self.get_world_rect().y + 12)

    def set_font(self, f: k4pg.Font):
        super(EventDialogue, self).set_font(f)
        self.inner_text.set_font(f)

    def interact(self, cam: k4pg.Camera, dt: float):
        self.update(dt)
        if self.finished and not self.paused:
            self.on_dialogue = False
            self.hide()
            self.set_not_talking()
            self.voice_player.stop()
            self.dialogue_sfx_player.stop()
            return
        self.on_dialogue = True

        # Get if the mouse was pressed in the display port of the current camera (bottom camera)
        mouse_pressed = self.inp.get_mouse_down(1) and cam.viewport.collidepoint(self.inp.get_mouse_pos())
        if self.paused:
            if mouse_pressed:
                self.unpause()
            return
        if mouse_pressed:
            self.complete()
            return

        # See if we have to progress the text
        self.current_cooldown += self.gm.delta_time
        while self.current_cooldown > self.cooldown and not self.paused:
            self.progress_text()

    def progress_text(self):
        # Commands starting with & (event 10060) and @s
        if self.text_left_to_do.startswith("@p"):  # Pause
            self.current_pause += 1
            self.pause()
            self.text_left_to_do = self.text_left_to_do[2:]
        elif self.text_left_to_do.startswith("@c\n"):  # Next page
            self.inner_text.text = ""
            self.text_left_to_do = self.text_left_to_do[3:]
        elif self.text_left_to_do.startswith("&"):
            command = ""
            self.text_left_to_do = self.text_left_to_do[1:]
            while not self.text_left_to_do.startswith("&") and len(self.text_left_to_do) > 0:
                command += self.text_left_to_do[0]
                self.text_left_to_do = self.text_left_to_do[1:]
            self.text_left_to_do = self.text_left_to_do[1:]
            if self.character_talking is not None:
                self.event_player.execute_str_command(command)
        elif self.text_left_to_do.startswith("@s"):
            self.text_left_to_do = self.text_left_to_do[2:]
            if self.dialogue_sfx_id != -1:
                sadl = load_sadl(f"data_lt2/stream/ST_{str(self.dialogue_sfx_id).zfill(3)}.SAD")
                self.dialogue_sfx_player.load_sound(sadl)
                self.dialogue_sfx_player.play()
        else:
            self.inner_text.text += self.text_left_to_do[:1]
            self.text_left_to_do = self.text_left_to_do[1:]
            self.current_cooldown -= self.cooldown

        # If we have finished we pause
        if self.finished:
            self.pause()

    # Complete until we pause
    def complete(self):
        while not self.paused and not self.finished:
            self.progress_text()

    # Reset all (texts, paused, and current_pause)
    def reset_all(self):
        self.current_pause = 0
        self.paused = False
        self.inner_text.text = ""

    # Init character name sprite
    def init_char_name(self):
        self.char_name.visible = True
        self.loader.load(f"data_lt2/ani/eventchr/?/chr{self.character_talking.char_id}_n.arc", self.char_name, True)

    # Pause the text
    def pause(self):
        self.paused = True
        self.set_not_talking()

    # Unpause the text
    def unpause(self):
        self.paused = False
        if not self.finished:
            self.set_talking()

    @property
    def finished(self):
        return self.text_left_to_do == ""

    def busy(self):
        return self.on_dialogue

    def draw(self, cam: k4pg.Camera):
        if not self.visible:
            return
        super(EventDialogue, self).draw(cam)
        self.inner_text.draw(cam)
        self.char_name.draw(cam)
