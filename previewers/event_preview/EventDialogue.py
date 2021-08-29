import pg_engine as pge
from .EventCharacter import EventCharacter
import pygame as pg
import pg_utils.sound.SADLStreamPlayer
from pg_utils.rom.rom_extract import load_sadl

from utility.replace_substitutions import replace_substitutions


class EventDialogue(pge.Sprite):
    NUMBER_OF_LINES = 5

    def __init__(self, event_player, *args, **kwargs):
        super(EventDialogue, self).__init__(*args, **kwargs)
        self.gm = pge.GameManager()

        self.event_player = event_player

        self.inner_text: pge.Text = pge.Text()

        self.char_name = pge.Sprite(())
        self.char_name.center = [pge.Alignment.RIGHT, pge.Alignment.BOTTOM]

        self.inp = pge.Input()

        self.current_line = 0
        self.current_pause = 0
        self.text_left_to_do = ""
        self.current_text = ""
        self.paused = False

        self.current_time_between_progress = 0
        self.time_to_progress = 1/60

        self.character_talking: EventCharacter = None

        self.voice_player = pg_utils.sound.SADLStreamPlayer.SADLStreamPlayer()
        self.voice_line = -1

        self.dialogue_sfx_player = pg_utils.sound.SADLStreamPlayer.SADLStreamPlayer()
        self.dialogue_sfx_id = -1

        self.on_dialogue = True

    def update_(self, dt: float):
        self.voice_player.update_(dt)
        self.dialogue_sfx_player.update_(dt)

    def unload(self):
        self.voice_player.stop()
        self.dialogue_sfx_player.stop()
        super(EventDialogue, self).unload()

    def show(self):
        self.visible = True
        self.inner_text.visible = True
        self.char_name.visible = True

    def hide(self):
        self.visible = False
        self.inner_text.visible = False
        self.char_name.visible = False

    def start_dialogue(self, character, chr_anim, text, voice, dialogue_sfx, loader: pge.SpriteLoader):
        self.character_talking = character
        self.reset_all()
        if chr_anim is not None and self.character_talking is not None:
            self.character_talking.set_anim(chr_anim)
        self.text_left_to_do = text
        # self.text_left_to_do = "I can change the #rcolor@B Also continue next line#x."
        self.text_left_to_do = replace_substitutions(self.text_left_to_do)
        self.voice_line = voice
        self.dialogue_sfx_id = dialogue_sfx
        self.on_dialogue = True
        self.show()
        if self.character_talking is not None:
            self.init_char_name(loader)
        else:
            self.char_name.visible = False
        self.set_talking()

    def set_talking(self):
        # If there is a voice line play it (first we stop it)
        if self.voice_line != -1:
            sfx = load_sadl(f"data_lt2/stream/event/?/{str(self.voice_line).zfill(3)}_{self.current_pause}.SAD")
            self.voice_player.start_sound(sfx, volume=1)

        if self.character_talking is not None:
            self.character_talking.set_talking()

    def set_not_talking(self):
        if self.character_talking is not None:
            self.character_talking.set_not_talking()

    def init_text(self, font_loader: pge.FontLoader):
        # Init dialogue positions
        font_loader.load("font_event", 12, self.inner_text)
        # self.inner_text.set_font("data_permanent/fonts/font_event.png?cp1252", [9, 12], is_font_map=True,
        #                          line_spacing=2, letter_spacing=1)
        self.inner_text.position[0] = (- 256 // 2) + 10
        self.inner_text.position[1] = self.get_world_rect().y + 20
        self.inner_text.center = [pge.Alignment.RIGHT, pge.Alignment.BOTTOM]
        self.char_name.position[1] = self.get_world_rect().y
        self.char_name.position[0] = - 256 // 2

    def interact(self, cam: pge.Camera):
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
        self.current_time_between_progress += self.gm.delta_time
        while self.current_time_between_progress > self.time_to_progress:
            self.current_time_between_progress -= self.time_to_progress
            self.progress_text()

    def progress_text(self):
        # Commands starting with & (event 10060) and @s
        if self.text_left_to_do.startswith("@p"):  # Pause
            self.current_pause += 1
            self.pause()
            self.text_left_to_do = self.text_left_to_do[2:]
            return
        elif self.text_left_to_do.startswith("@c"):  # Next page
            self.reset_texts()
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
                self.event_player.execute_command(command)
            if self.finished:
                self.pause()
            return
        elif self.text_left_to_do.startswith("@s"):
            self.text_left_to_do = self.text_left_to_do[2:]
            if self.dialogue_sfx_id != -1:
                sadl = load_sadl(f"data_lt2/stream/ST_{str(self.dialogue_sfx_id).zfill(3)}.SAD")
                self.dialogue_sfx_player.start_sound(sadl)

        # Move one character from self.text_left_to_do to current_text
        self.current_text += self.text_left_to_do[:1]
        self.text_left_to_do = self.text_left_to_do[1:]

        # Update current text object
        self.inner_text.color = pg.Color(0, 0, 0)
        self.inner_text.bg_color = pg.Color(0, 255, 0)
        self.inner_text.mask_color = pg.Color(0, 255, 0)
        self.inner_text.text = self.current_text

        # If we have finished we pause
        if self.finished:
            self.pause()

    # Complete until we pause
    def complete(self):
        while not self.paused and not self.finished:
            self.progress_text()

    # Reset the texts
    def reset_texts(self):
        self.current_line = 0
        self.current_text = ""
        self.inner_text.text = ""

    # Reset all (texts, paused, and current_pause)
    def reset_all(self):
        self.current_pause = 0
        self.paused = False
        self.reset_texts()

    # Init character name sprite
    def init_char_name(self, loader: pge.SpriteLoader):
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
    def finished(self):
        return self.text_left_to_do == ""

    def busy(self):
        return self.on_dialogue

    def draw(self, cam: pge.Camera):
        super(EventDialogue, self).draw(cam)
        self.inner_text.draw(cam)
        self.char_name.draw(cam)
