from formats.sound import smd
from formats import binary
import io
from queue import PriorityQueue
import numpy as np
from pg_utils.sound.StreamPlayerAbstract import StreamPlayerAbstract
from formats.sound.soundtypes import Preset
from typing import Dict

from dataclasses import dataclass, field
from typing import Any

import pygame as pg
import os

try:
    import custom_fluidsynth.custom_fluidsynth as fluidsynth
except ImportError as e:
    # Can still run without the synth
    print(f"Error importing fluidsynth: {e}")
    fluidsynth = None


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


class SMDLSequencer:
    TRACK_SELECT = -1

    def __init__(self, smd_obj: smd.SMDL, sample_rate=44100):
        self.smd_obj: smd.SMDL = smd_obj

        self.sample_rate = sample_rate
        sf2_path = os.path.dirname(__file__) + "/layton2.sf2"
        self.loops = False

        self.loop_start = [0] * len(self.smd_obj.tracks)
        self.last_note_length = [0] * len(self.smd_obj.tracks)
        self.last_delay = [0] * len(self.smd_obj.tracks)
        self.bpm = 120
        self.octave = [0] * len(self.smd_obj.tracks)
        self.tracks_br = []
        self.track_lengths = []
        self.track_completed = [False] * len(self.smd_obj.tracks)

        self.event_queue = PriorityQueue()
        self.current_tick = 0
        self.completed = False

        self.PROGRAM_MAP = {}

        if fluidsynth is None or not os.path.isfile(sf2_path):
            self.fs = None
            return
        self.fs = fluidsynth.Synth(samplerate=self.sample_rate, gain=0.5)
        self.sf_id = self.fs.sfload(sf2_path)
        self.fs.program_select(0, self.sf_id, 0, 0)

        for track in self.smd_obj.tracks:
            track_br = binary.BinaryReader(io.BytesIO(track.track_content.event_bytes))
            self.tracks_br.append(track_br)
            track_br.seek(-1, io.SEEK_END)
            track_length = track_br.tell()
            track_br.seek(0)
            self.track_lengths.append(track_length)

    def ticks_to_samples(self, ticks):
        # ticks to seconds -> ticks * (60 / (bpm * ticks per quarter note))
        # seconds to samples -> sample_rate * seconds
        # ticks to samples: sample_rate * ticks * 60 / bmp * ticks per quarter note
        return int((self.sample_rate * ticks * 60) / (self.bpm * self.smd_obj.song_chunk.tpqn))

    PAUSE_TICKS = [96, 72, 64, 48, 36, 32, 24, 18, 16, 12, 9, 8, 6, 4, 3, 2]

    # NO: 365, 812, 818, 849, 859, 869, 888, 898, 899, 1100, 1114, 1120, 1126, 1201
    SAMPLE_TO_PROGRAM = {
        105: [76, 98],  # Piano (Bright)
        27: [103, 104, 105, 106, 107, 108, 109, 110, 111, 112],  # Vibraphone
        0: [126, 127, 128, 129, 130, 131, 132, 133, 134, 135],  # Accordion
        # For some reason some Bandoneon notes don't work correctly
        # 0: [126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 843, 845, 847, 855, 857, 865, 867],  # Accordion + Bandoneon
        115: [210, 212, 214, 216],  # BD Cym Shaker
        114: [294, 302, 303, 795, 797],  # Maracas WBlock Tri
        62: [306, 311, 315, 318, 320, 328],  # Oboe/Violin
        81: [342, 349, 358, 366, 372],  # String Ensemble 1
        117: [465],  # Crash Cymbal
        103: [486, 492, 504, 506, 514, 516, 518],  # Harpsichord
        33: [668, 672, 674, 676, 678, 680, 682, 684],  # Marimba
        99: [711, 717, 725, 729, 733, 741, 745],  # Guitar
        78: [806, 809, 811, 813, 815, 819, 821, 829],  # Cello
        10: [843, 845, 847, 855, 857, 859, 865, 867],  # Bandoneon
        83: [877, 879, 881, 884, 887, 889, 891, 894, 897, 901],  # String Ensemble 2
        93: [970, 972, 974, 975],  # Upright Bass
        21: [1090, 1092, 1096, 1098, 1104, 1106, 1108, 1112, 1118, 1122, 1124],  # Celesta/Music Box
        120: [1161],  # Timpani
        113: [1190, 1191, 1192, 1193, 1194, 1195, 1196, ],  # Flute
        85: [1197, 1198, 1199, 1200, 1202, 1203, 1204],  # Bassoon-ish
        116: [1213, 1214, 1215, 1216, 1217, 1218, 1219],
        106: [1229, 1230, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1239]  # Piano (Muted)
    }

    def map_preset(self, preset: Preset):
        for sample in preset.split_entries:
            for program in self.SAMPLE_TO_PROGRAM.keys():
                if sample.sample_info.sample_index in self.SAMPLE_TO_PROGRAM[program]:
                    return program
        return None

    def create_program_map(self, presets: Dict[int, Preset]):
        for preset_index in presets.keys():
            mapped_preset = self.map_preset(presets[preset_index])
            print(f"Preset {preset_index} mapped to {mapped_preset}")
            if mapped_preset is not None:
                self.PROGRAM_MAP[preset_index] = mapped_preset

    def read_pauses(self, track_id):
        track_br = self.tracks_br[track_id]
        while track_br.tell() < self.track_lengths[track_id] and not self.track_completed[track_id]:
            prefix = f"[Track {track_id} tick: {self.current_tick}]\t"
            event = track_br.read_uint8()

            def post_pause(track_id1=track_id):
                self.read_pauses(track_id1)
            if event == 0x98:
                self.track_completed[track_id] = True
                break
            elif 0x0 <= event <= 0x7F:  # Note
                note_data = track_br.read_uint8()

                nb_param_bytes = (note_data & 0b11000000) >> 6

                duration = track_br.read_char_array(nb_param_bytes)
                if len(duration) == 0:
                    duration = self.last_note_length[track_id]
                else:
                    duration = [x[0] for x in duration]
                    for i in range(len(duration) - 1):
                        v = duration.pop(0)
                        duration[0] += v << 8
                    duration = duration[0]  # ticks
                    self.last_note_length[track_id] = duration
                # notes are on even, pauses on odd (pauses after notes)
                note_end = (self.current_tick + duration) * 2

                queue_stop_object = PrioritizedItem(note_end, None)
                self.event_queue.put(queue_stop_object)
            elif 0x80 <= event <= 0x8F:  # Pause
                pause_time = self.PAUSE_TICKS[event - 0x80]  # ticks
                self.last_delay[track_id] = pause_time

                # notes are on even, pauses on odd (pauses after notes)
                pause_end = (self.current_tick + pause_time) * 2 + 1

                queue_stop_object = PrioritizedItem(pause_end, post_pause)
                self.event_queue.put(queue_stop_object)
                return
            elif event == 0x90:
                pause_end = (self.current_tick + self.last_delay[track_id]) * 2 + 1
                queue_stop_object = PrioritizedItem(pause_end, post_pause)
                self.event_queue.put(queue_stop_object)
                return
            elif event == 0x91:
                self.last_delay[track_id] += track_br.read_uint8()
                pause_end = (self.current_tick + self.last_delay[track_id]) * 2 + 1
                queue_stop_object = PrioritizedItem(pause_end, post_pause)
                self.event_queue.put(queue_stop_object)
                return
            elif event == 0x92:
                self.last_delay[track_id] = track_br.read_uint8()
                pause_end = (self.current_tick + self.last_delay[track_id]) * 2 + 1
                queue_stop_object = PrioritizedItem(pause_end, post_pause)
                self.event_queue.put(queue_stop_object)
                return
            elif event == 0x93:
                a = track_br.read_uint16()
                self.last_delay[track_id] = a
                pause_end = (self.current_tick + self.last_delay[track_id]) * 2 + 1
                queue_stop_object = PrioritizedItem(pause_end, post_pause)
                self.event_queue.put(queue_stop_object)
                return
            elif event == 0x94:
                a = track_br.read_uint16()
                a |= track_br.read_uint8() << 16
                self.last_delay[track_id] = a
                pause_end = (self.current_tick + self.last_delay[track_id]) * 2 + 1
                queue_stop_object = PrioritizedItem(pause_end, post_pause)
                self.event_queue.put(queue_stop_object)
                return
            elif event == 0xa4 or event == 0xa5:
                self.bpm = track_br.read_uint8()
            elif event == 0x99:
                self.loops = True
            elif event in [0xAB,  # Should remain here
                           # Unknown
                           0x95, 0x9C, 0xA9, 0xAA, 0xB1, 0xB2, 0xB3,
                           0xB5, 0xB6, 0xBC, 0xBE, 0xBF, 0xC0, 0xC3,
                           0xD0, 0xD1, 0xD2, 0xDB, 0xDF, 0xE1, 0xE7,
                           0xE9, 0xEF, 0xF6, 0x91, 0x92, 0xa0, 0xa1,
                           0xac, 0xe0, 0xe3, 0xe8]:
                track_br.read_char_array(1)
            elif event in [0xCB, 0xF8,  # Should remain here
                           # Unknown
                           0xA8, 0xB4, 0xD5, 0xD6, 0xD8, 0xF2, 0x93,
                           0xd7]:
                track_br.read_char_array(2)
            elif event in [0xAF, 0xD4, 0xE2, 0xEA, 0xF3, 0x94]:  # Unknown
                track_br.read_char_array(3)
            elif event in [0xDD, 0xE5, 0xED, 0xF1]:  # Unknown
                track_br.read_char_array(4)
            elif event in [0xDC, 0xE4, 0xEC, 0xF0]:  # Unknown
                track_br.read_char_array(5)

    def read_events(self, track_id):
        track_br = self.tracks_br[track_id]
        while track_br.tell() < self.track_lengths[track_id] and not self.track_completed[track_id]:
            prefix = f"[Track {track_id} tick: {self.current_tick}]\t"

            def post_pause(track_id1=track_id):
                self.read_events(track_id1)
            event = track_br.read_uint8()
            if event == 0x98:
                self.track_completed[track_id] = True
                break
            elif 0x0 <= event <= 0x7F:  # Note
                note_data = track_br.read_uint8()

                velocity = event

                nb_param_bytes = (note_data & 0b11000000) >> 6
                octave_mod = ((note_data & 0b00110000) >> 4) - 2
                note = note_data & 0b00001111
                self.octave[track_id] += octave_mod
                # midi_note = 12 * (self.octave[track_id] - 1) + note
                midi_note = 12 * self.octave[track_id] + note

                duration = track_br.read_char_array(nb_param_bytes)
                if len(duration) == 0:
                    duration = self.last_note_length[track_id]
                else:
                    duration = [x[0] for x in duration]
                    for i in range(len(duration) - 1):
                        v = duration.pop(0)
                        duration[0] += v << 8
                    duration = duration[0]  # ticks
                    self.last_note_length[track_id] = duration
                # notes are on even, pauses on odd (pauses after notes)
                note_end = (self.current_tick + duration) * 2
                # print(f"{prefix}Note {midi_note} with duration {duration}, ending on {note_end}")

                self.fs.noteon(track_id, midi_note, velocity)

                def on_note_end(note1=midi_note, channel=track_id):
                    self.fs.noteoff(channel, note1)

                queue_stop_object = PrioritizedItem(note_end, on_note_end)
                self.event_queue.put(queue_stop_object)
            elif 0x80 <= event <= 0x8F:  # Pause
                pause_time = self.PAUSE_TICKS[event - 0x80]  # ticks
                self.last_delay[track_id] = pause_time

                # notes are on even, pauses on odd (pauses after notes)
                pause_end = (self.current_tick + pause_time) * 2 + 1
                # print(f"{prefix}Pause 1 ending on {pause_end}")

                queue_stop_object = PrioritizedItem(pause_end, post_pause)
                self.event_queue.put(queue_stop_object)
                return
            elif event == 0x90:
                pause_end = (self.current_tick + self.last_delay[track_id]) * 2 + 1
                # print(f"{prefix}Pause 2 ending on {pause_end}")
                queue_stop_object = PrioritizedItem(pause_end, post_pause)
                self.event_queue.put(queue_stop_object)
                return
            elif event == 0x91:
                self.last_delay[track_id] += track_br.read_uint8()
                pause_end = (self.current_tick + self.last_delay[track_id]) * 2 + 1
                # print(f"{prefix}Pause 3 ending on {pause_end}")
                queue_stop_object = PrioritizedItem(pause_end, post_pause)
                self.event_queue.put(queue_stop_object)
                return
            elif event == 0x92:
                self.last_delay[track_id] = track_br.read_uint8()
                pause_end = (self.current_tick + self.last_delay[track_id]) * 2 + 1
                # print(f"{prefix}Pause 4 ending on {pause_end}, {self.last_delay[track_id]}")
                queue_stop_object = PrioritizedItem(pause_end, post_pause)
                self.event_queue.put(queue_stop_object)
                return
            elif event == 0x93:
                a = track_br.read_uint16()
                self.last_delay[track_id] = a
                pause_end = (self.current_tick + self.last_delay[track_id]) * 2 + 1
                # print(f"{prefix}Pause 5 ending on {pause_end}")
                queue_stop_object = PrioritizedItem(pause_end, post_pause)
                self.event_queue.put(queue_stop_object)
                return
            elif event == 0x94:
                a = track_br.read_uint16()
                a |= track_br.read_uint8() << 16
                self.last_delay[track_id] = a
                pause_end = (self.current_tick + self.last_delay[track_id]) * 2 + 1
                # print(f"{prefix}Pause 6 ending on {pause_end}")
                queue_stop_object = PrioritizedItem(pause_end, post_pause)
                self.event_queue.put(queue_stop_object)
                return
            elif event == 0x99:
                # Loop does not work because of pygame
                self.loop_start[track_id] = track_br.tell()
                # print(f"{prefix}Loop start: {track_br.tell()}")
            elif event == 0xa0:
                self.octave[track_id] = track_br.read_uint8()
                # print(f"{prefix}Setting octave to {self.octave[track_id]}")
            elif event == 0xa1:
                octave_mod = track_br.read_uint8()
                self.octave[track_id] += octave_mod
            elif event == 0xa4 or event == 0xa5:
                self.bpm = track_br.read_uint8()
                # print(f"{prefix}Set tempo: {self.bpm}")
            elif event == 0xac:
                program = track_br.read_uint8()
                print(f"{prefix}Program select: {program}")
                if program in self.PROGRAM_MAP.keys():
                    program = self.PROGRAM_MAP[program]
                    self.fs.program_select(track_id, self.sf_id, 0, program)
                else:
                    print(f"PROGRAM {program} not in PROGRAM_MAP")
            elif event == 0xd7:
                bend = track_br.read_uint16()
                # print(f"{prefix}Bending note: {bend}")
                self.fs.pitch_bend(track_id, bend)
            elif event == 0xe0:  # Change volume
                volume = track_br.read_uint8()
                # print(f"{prefix}Changing volume to {volume}")
                self.fs.cc(track_id, 0x07, volume)
            elif event == 0xe3:
                expression = track_br.read_uint8()
                # print(f"{prefix}Changing expression to {expression}")
                self.fs.cc(track_id, 0x0B, expression)
            elif event == 0xe8:  # pan
                pan = track_br.read_uint8()
                # print(f"{prefix}Changing pan to {pan}")
                self.fs.cc(track_id, 0x0a, pan)
            elif event in [0xAB,  # Should remain here
                           # Unknown
                           0x95, 0x9C, 0xA9, 0xAA, 0xB1, 0xB2, 0xB3,
                           0xB5, 0xB6, 0xBC, 0xBE, 0xBF, 0xC0, 0xC3,
                           0xD0, 0xD1, 0xD2, 0xDB, 0xDF, 0xE1, 0xE7,
                           0xE9, 0xEF, 0xF6]:
                track_br.read_char_array(1)
                # v = track_br.read_char_array(1)
                # print(f"[Track {track_id} tick: {self.current_tick}]\tEvent: {hex(event)} Value: {v}")
            elif event in [0xCB, 0xF8,  # Should remain here
                           # Unknown
                           0xA8, 0xB4, 0xD5, 0xD6, 0xD8, 0xF2]:
                track_br.read_char_array(2)
                # v = track_br.read_char_array(2)
                # print(f"[Track {track_id} tick: {self.current_tick}]\tEvent: {hex(event)} Value: {v}")
            elif event in [0xAF, 0xD4, 0xE2, 0xEA, 0xF3]:  # Unknown
                track_br.read_char_array(3)
                # v = track_br.read_char_array(3)
                # print(f"[Track {track_id} tick: {self.current_tick}]\tEvent: {hex(event)} Value: {v}")
            elif event in [0xDD, 0xE5, 0xED, 0xF1]:  # Unknown
                track_br.read_char_array(4)
                # v = track_br.read_char_array(4)
                # print(f"[Track {track_id} tick: {self.current_tick}]\tEvent: {hex(event)} Value: {v}")
            elif event in [0xDC, 0xE4, 0xEC, 0xF0]:  # Unknown
                track_br.read_char_array(5)
                # v = track_br.read_char_array(5)
                # print(f"[Track {track_id} tick: {self.current_tick}]\tEvent: {hex(event)} Value: {v}")

    def compute_sample_count(self):
        if self.fs is None:
            return 0
        self.reset()
        for i in range(len(self.tracks_br)):
            if i != self.TRACK_SELECT and self.TRACK_SELECT > 0:
                continue
            track_start = PrioritizedItem(0, lambda track_id=i: self.read_pauses(track_id))
            self.event_queue.put(track_start)
        samples = 0
        while not self.event_queue.empty():
            task: PrioritizedItem = self.event_queue.get()
            task_start = task.priority
            task_function = task.item
            ticks_to_do = (task_start // 2) - self.current_tick
            if ticks_to_do > 0:
                samples += self.ticks_to_samples(ticks_to_do)
                self.current_tick = task_start // 2
            if callable(task_function):
                task_function()
        print(f"SAMPLES: {self.current_tick}")
        return samples  # 2 extra seconds

    def reset(self):
        if not self.fs:
            return
        for track_br in self.tracks_br:
            track_br.seek(0)
        self.current_tick = 0
        self.last_note_length = [0] * len(self.smd_obj.tracks)
        self.track_completed = [False] * len(self.smd_obj.tracks)
        self.last_delay = [0] * len(self.smd_obj.tracks)
        self.bpm = 120
        self.completed = False

    def generate_samples2(self, ticks_to_create=0):
        samples = np.zeros((0, 2), dtype=np.int16)
        if self.fs is None:
            return samples
        start_tick = self.current_tick
        if self.event_queue.empty() and not self.completed:
            for i in range(len(self.tracks_br)):
                if i != self.TRACK_SELECT and self.TRACK_SELECT > 0:
                    continue
                track_start = PrioritizedItem(0, lambda track_id=i: self.read_events(track_id))
                self.event_queue.put(track_start)
        while not self.event_queue.empty():
            task: PrioritizedItem = self.event_queue.get()
            task_start = task.priority
            task_function = task.item
            ticks_to_do = (task_start // 2) - self.current_tick
            if ticks_to_do > 0:
                # print(f"Creating {ticks_to_do} ticks")
                array = self.fs.get_samples(self.ticks_to_samples(ticks_to_do))
                array = np.swapaxes(array, 0, 1)
                # print(array.shape[0], self.ticks_to_samples(ticks_to_do))
                samples = np.append(samples, array, axis=0)
                self.current_tick = task_start // 2
            if callable(task_function):
                task_function()
            if self.current_tick - start_tick >= ticks_to_create > 0:
                return samples
        self.completed = True
        return samples

    @staticmethod
    def get_dependencies_met():
        sf2_path = os.path.dirname(__file__) + "/layton2.sf2"
        return fluidsynth is not None and os.path.isfile(sf2_path)


class SMDLStreamPlayer(StreamPlayerAbstract):
    def __init__(self):
        super(SMDLStreamPlayer, self).__init__()
        self.smd_sequencer: SMDLSequencer = None
        self.sound_obj: [pg.mixer.Sound] = None
        self.sound_buffer = None
        self.loading = False
        self.loading_finished = False
        self.buffer_offset = 0
        self.preset_dict: Dict[int, Preset] = {}
        self.volume = 0.0

        self.fading = False
        self.current_fade_time = 0.0
        self.fade_time = 0.0

    def set_preset_dict(self, preset_dict: Dict[int, Preset]):
        self.preset_dict = preset_dict

    def update_(self, delta_time):
        if self.loading:
            self.add_samples()
        if self.fading:
            self.do_fade(delta_time)

    def do_fade(self, delta_time):
        if self.current_fade_time >= self.fade_time:
            self.current_fade_time = self.fade_time
            self.fading = False
        percentage = (self.current_fade_time / self.fade_time)
        if not self.is_fade_in:
            percentage = 1 - percentage
        new_volume = self.volume * percentage
        if self.sound_obj is not None:
            self.sound_obj.set_volume(new_volume)
        self.current_fade_time += delta_time

    def add_samples(self, first_init=False):
        ticks_to_do = 48
        if first_init:
            ticks_to_do *= 5  # If the sound gets cut increase this number (slower load, better playback)
        new_samples = self.smd_sequencer.generate_samples2(ticks_to_do)
        if new_samples.shape[0] == 0:
            self.loading = False
            self.loading_finished = True
            return
        self.sound_buffer[self.buffer_offset:self.buffer_offset + new_samples.shape[0]] = new_samples
        self.buffer_offset += new_samples.shape[0]

    def start_sound(self, snd_obj: smd.SMDL, loops=0, volume=0.5):
        self.fading = False
        if not SMDLSequencer.get_dependencies_met():
            return
        if self.sound_obj is not None:
            self.sound_obj.stop()
        if self.smd_sequencer:
            do_load = self.smd_sequencer.smd_obj is not snd_obj
        else:
            do_load = True
        if do_load:
            sample_rate = pg.mixer.get_init()[0]
            self.smd_sequencer = SMDLSequencer(snd_obj, sample_rate=sample_rate)
            self.smd_sequencer.create_program_map(self.preset_dict)
            length = self.smd_sequencer.compute_sample_count()
            self.smd_sequencer.reset()
            self.sound_obj = pg.sndarray.make_sound(np.zeros((length, 2), dtype=np.int16))
            self.sound_buffer = pg.sndarray.samples(self.sound_obj)
            self.loading_finished = False
            self.buffer_offset = 0
            self.add_samples(first_init=True)
        if not self.loading_finished:
            self.loading = True
        # We ignore the loops passed
        if self.smd_sequencer.loops:
            loops = -1
        else:
            loops = 0
        self.sound_obj.play(loops=loops)
        self.sound_obj.set_volume(volume)
        self.volume = volume

    def stop(self):
        self.loading_finished = False
        self.loading = False
        if self.sound_obj is not None:
            self.sound_obj.stop()

    @staticmethod
    def get_playable():
        return SMDLSequencer.get_dependencies_met()

    def fade(self, time, fade_in):
        self.fading = True
        self.fade_time = time
        self.current_fade_time = 0.0
        self.is_fade_in = fade_in
