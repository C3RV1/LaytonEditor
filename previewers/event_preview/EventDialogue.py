import PygameEngine.UI.UIElement
import PygameEngine.UI.Text
import PygameEngine.Sprite
import PygameEngine.GameManager
import PygameEngine.Input
from .EventCharacter import EventCharacter
from pygame_utils.rom.rom_extract import load_animation
from typing import Optional
import pygame as pg
import pygame_utils.SADLStreamPlayer
from pygame_utils.rom.rom_extract import load_sadl

from .abstracts.EventDialogueAbstract import EventDialogueAbstract
from utility.replace_substitutions import replace_substitutions


class EventDialogue(PygameEngine.UI.UIElement.UIElement, PygameEngine.Sprite.Sprite,
                    EventDialogueAbstract):
    NUMBER_OF_LINES = 5

    def __init__(self, groups, voice_player: pygame_utils.SADLStreamPlayer.SoundPlayer, event_player):
        PygameEngine.UI.UIElement.UIElement.__init__(self)
        PygameEngine.Sprite.Sprite.__init__(self, ())
        EventDialogueAbstract.__init__(self)
        self.gm = PygameEngine.GameManager.GameManager()

        self.event_player = event_player

        self.check_interacting = self._check_interacting
        self.pre_interact = self.pre_interact_
        self.post_interact = self.end_dialogue

        self.interact = self._interact
        self.inner_text = None

        self.char_name = PygameEngine.Sprite.Sprite(())
        self.char_name.layer = 101
        self.char_name.draw_alignment = [self.ALIGNMENT_RIGHT, self.ALIGNMENT_BOTTOM]

        self.inp = PygameEngine.Input.Input()

        self.current_line = 0
        self.current_pause = 0
        self.text_left_to_do = ""
        self.current_text = ""
        self.paused = False

        self.current_time_between_progress = 0
        self.time_to_progress = 1/60

        self.character_talking: Optional[EventCharacter] = None

        self.voice_player = voice_player
        self.voice_line = -1

        self.groups_perseverance = groups

        self.on_dialogue = True

    def show(self):
        if not self.alive():
            self.add(self.groups_perseverance)
        if not self.inner_text.alive():
            self.inner_text.add(self.groups_perseverance)
        if not self.char_name.alive():
            self.char_name.add(self.groups_perseverance)
        self.dirty = 1

    def hide(self):
        if self.current_camera is not None:
            if len(self.groups()) > 0:
                self.current_camera.draw(self.groups()[0], dirty_all=True)
        self.kill()
        if self.inner_text is not None:
            self.inner_text.kill()
        self.char_name.kill()

    def start_dialogue(self, character, chr_anim, text, voice):
        self.character_talking = character
        self.reset_all()
        if chr_anim is not None and self.character_talking is not None:
            self.character_talking.set_anim(chr_anim)
        self.text_left_to_do = text
        # self.text_left_to_do = "I can change the #rcolor@B Also continue next line#x."
        self.text_left_to_do = replace_substitutions(self.text_left_to_do)
        self.voice_line = voice
        self.on_dialogue = True
        self.show()
        if self.character_talking is not None:
            self.init_char_name()
        else:
            self.char_name.kill()
        self.set_talking()

    def set_talking(self):
        # If there is a voice line play it (first we stop it)
        self.voice_player.stop()
        if self.voice_line != -1:
            sfx = load_sadl(f"data_lt2/stream/event/?/{str(self.voice_line).zfill(3)}_{self.current_pause}.SAD")
            self.voice_player.start_sound(sfx)

        if self.character_talking is not None:
            self.character_talking.set_talking()

    def set_not_talking(self):
        if self.character_talking is not None:
            self.character_talking.set_not_talking()

    def init_position(self):
        # Init dialogue positions
        self.inner_text = PygameEngine.UI.Text.Text(())
        self.inner_text.layer = 120
        self.inner_text.set_font("data_permanent/fonts/font_event.png?cp1252", [9, 12], is_font_map=True,
                                 line_spacing=2, letter_spacing=1)
        self.inner_text.world_rect.x = (- 256 // 2) + 10
        self.inner_text.world_rect.y = self.world_rect.y - self.world_rect.h + 20
        self.inner_text.draw_alignment = [self.inner_text.ALIGNMENT_RIGHT, self.inner_text.ALIGNMENT_BOTTOM]
        self.char_name.world_rect.y = self.world_rect.y - self.world_rect.h
        self.char_name.world_rect.x = - 256 // 2

    # Check if we are interacting with the dialogue (UIElement)
    def _check_interacting(self):
        if self.finished and not self.paused:
            self.voice_player.stop()
            self.interacting = False
            return
        self.interacting = True

    # Once we start to interact we set talking (UIElement)
    def pre_interact_(self):
        self.on_dialogue = True

    def end_dialogue(self):
        self.text_left_to_do = ""
        self.on_dialogue = False
        self.hide()
        self.set_not_talking()

    # When we are interacting (UIElement)
    def _interact(self):
        # Get if the mouse was pressed in the display port of the current camera (bottom camera)
        mouse_pressed = self.inp.get_mouse_down(1) and \
                        self.current_camera.display_port.collidepoint(self.inp.get_screen_mouse_pos())
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
        # TODO: commands starting with & (event 10060) and @s
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
    def init_char_name(self):
        load_animation(f"data_lt2/ani/eventchr/?/chr{self.character_talking.char_id}_n.arc", self.char_name)

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
