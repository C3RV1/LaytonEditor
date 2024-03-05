import k4pg
from .EventCharacter import EventCharacter
import pygame as pg
import pg_utils.sound.SADLStreamPlayer
from pg_utils.rom.rom_extract import load_sadl
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .EventPlayer import EventPlayer

from utility.replace_substitutions import replace_substitutions


class TextPage:
    def __init__(self, text: str):
        self.text = text
        self.page_loaded_once = False
        self.character_states = []
        self.current_pause_start = 0

    @classmethod
    def from_text(cls, text):
        return cls(text)

    @classmethod
    def text_to_pages(cls, text) -> list:
        pages_text = text.split("@c\n")
        return [cls.from_text(t) for t in pages_text]


class EventDialogue(k4pg.Sprite):
    NUMBER_OF_LINES = 5

    def __init__(self, event_player: 'EventPlayer', *args, **kwargs):
        super(EventDialogue, self).__init__(*args, **kwargs)
        self.gm = k4pg.GameManager()

        self.event_player: 'EventPlayer' = event_player

        self.inner_text: k4pg.Text = k4pg.Text(center=pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP))

        self.char_name = k4pg.Sprite()
        self.char_name.center = pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.BOTTOM)

        self.inp = k4pg.Input()

        self.current_pause = 0

        self.pages: list[TextPage] = []
        self.current_page = 0

        self.text_left_to_do = ""
        self.paused = False

        self.current_time_between_progress = 0
        self.time_to_progress = 1/60

        self.character_talking: Optional[EventCharacter] = None

        self.voice_player = pg_utils.sound.SADLStreamPlayer.SADLStreamPlayer(loops=False)
        self.voice_player.set_volume(0.5)
        self.voice_line = -1

        self.dialogue_sfx_player = pg_utils.sound.SADLStreamPlayer.SADLStreamPlayer(loops=False)
        self.dialogue_sfx_player.set_volume(0.5)
        self.dialogue_sfx_id = -1

        self.on_dialogue = False

    def update_(self, dt: float):
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

    def start_dialogue(self, character, chr_anim, text, voice, dialogue_sfx, loader: k4pg.SpriteLoader):
        self.character_talking = character
        self.reset_all()
        if chr_anim is not None and self.character_talking is not None:
            self.character_talking.set_anim(chr_anim)
        # self.text_left_to_do = "I can change the #rcolor@B Also continue next line#x."

        self.pages = TextPage.text_to_pages(replace_substitutions(text))
        self.current_page = 0
        self.load_page()

        self.voice_line = voice
        self.dialogue_sfx_id = dialogue_sfx
        self.on_dialogue = True
        self.show()
        if self.character_talking is not None:
            self.init_char_name(loader)
        else:
            self.char_name.visible = False
        self.set_talking()

    def load_page(self):
        if self.current_page == len(self.pages):
            return
        if not self.pages[self.current_page].page_loaded_once:
            self.pages[self.current_page].current_pause_start = self.current_pause
            for i in range(8):
                if self.event_player.characters[i] is None:
                    break
                self.pages[self.current_page].character_states.append(
                    self.event_player.characters[i].copy_state()
                )
            self.pages[self.current_page].page_loaded_once = True
        else:
            self.current_pause = self.pages[self.current_page].current_pause_start
            for i, state in enumerate(self.pages[self.current_page].character_states):
                self.event_player.characters[i].load_state(state)
        self.text_left_to_do = self.pages[self.current_page].text

    def set_talking(self):
        # If there is a voice line play it (first we stop it)
        if self.voice_line != -1:
            # USA workaround
            sfx = load_sadl(f"data_lt2/stream/event/?/{str(self.voice_line).zfill(3)}_{self.current_pause}.SAD")
            if sfx is not None:
                self.voice_player.load_sound(sfx)
                self.voice_player.play()

        if self.character_talking is not None:
            self.character_talking.set_talking(True)

    def set_not_talking(self):
        if self.character_talking is not None:
            self.character_talking.set_talking(False)

    def init_text(self, font_loader: k4pg.FontLoader):
        # Init dialogue positions
        font_loader.load("fontevent", 12, self.inner_text)
        self.inner_text.position.update((- 256 // 2) + 10, self.get_world_rect().y + 19)
        self.inner_text.center = pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP)
        self.inner_text.line_spacing = 3
        self.char_name.position.update(- 256 // 2 + 2, self.get_world_rect().y + 12)

    def end(self):
        self.on_dialogue = False
        self.hide()
        self.set_not_talking()
        self.voice_player.stop()
        self.dialogue_sfx_player.stop()

    def interact(self, cam: k4pg.Camera, dt: float):
        self.update_(dt)
        if self.finished and not self.paused:
            self.end()
            return
        self.on_dialogue = True

        # TODO: Tie to edit mode.
        if self.inp.get_key_down(pg.K_LEFT):
            self.current_page = max(0, self.current_page - 1)
            self.load_page()
            self.reset_texts()
            self.unpause()

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
        self.current_time_between_progress += self.gm.delta_time
        while self.current_time_between_progress > self.time_to_progress and not self.paused:
            self.current_time_between_progress -= self.time_to_progress
            self.progress_text()

    def progress_text(self):
        # Commands starting with & (event 10060) and @s
        if self.finished_page:
            self.current_page += 1
            self.load_page()
            if not self.finished:
                self.reset_texts()
            else:
                self.pause()
        elif self.text_left_to_do.startswith("@p"):  # Pause
            self.current_pause += 1
            self.pause()
            self.text_left_to_do = self.text_left_to_do[2:]
            return
        elif self.text_left_to_do.startswith("&"):
            command = ""
            self.text_left_to_do = self.text_left_to_do[1:]
            while not self.text_left_to_do.startswith("&") and len(self.text_left_to_do) > 0:
                command += self.text_left_to_do[0]
                self.text_left_to_do = self.text_left_to_do[1:]
            self.text_left_to_do = self.text_left_to_do[1:]
            if self.character_talking is not None:
                self.event_player.execute_str_command(command)
            if self.finished:
                self.pause()
            return
        elif self.text_left_to_do.startswith("@s"):
            self.text_left_to_do = self.text_left_to_do[2:]
            if self.dialogue_sfx_id != -1:
                sadl = load_sadl(f"data_lt2/stream/ST_{str(self.dialogue_sfx_id).zfill(3)}.SAD")
                if sadl is not None:
                    self.dialogue_sfx_player.load_sound(sadl)
                    self.dialogue_sfx_player.play()

        # Move one character from self.text_left_to_do to current_text
        self.inner_text.text += self.text_left_to_do[:1]
        self.text_left_to_do = self.text_left_to_do[1:]

        # Update current text object
        self.inner_text.color = pg.Color(0, 0, 0)

    # Complete until we pause
    def complete(self):
        while not self.paused and not self.finished:
            self.progress_text()

    # Reset the texts
    def reset_texts(self):
        self.inner_text.text = ""

    # Reset all (texts, paused, and current_pause)
    def reset_all(self):
        self.current_page = 0
        self.current_pause = 0
        self.paused = False
        self.reset_texts()

    # Init character name sprite
    def init_char_name(self, loader: k4pg.SpriteLoader):
        loader.load(f"data_lt2/ani/eventchr/?/chr{self.character_talking.char_id}_n.arc", self.char_name,
                    sprite_sheet=True)

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
    def finished_page(self):
        return self.text_left_to_do == ""

    @property
    def finished(self):
        return self.finished_page and self.current_page == len(self.pages)

    def busy(self):
        return self.on_dialogue

    def draw(self, cam: k4pg.Camera):
        if not self.visible:
            return
        super(EventDialogue, self).draw(cam)
        self.inner_text.draw(cam)
        self.char_name.draw(cam)
