from formats.sound import smd
from formats import binary
import io
from queue import PriorityQueue
import numpy as np

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

        self.event_queue = PriorityQueue()
        self.current_tick = 0
        self.completed = False

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

    PROGRAM_MAP = {78: 78, 12: 0, 30: 27, 27: 27, 93: 93, 21: 21, 22: 21, 23: 21, 81: 81, 105: 105}

    def read_pauses(self, track_id):
        track_br = self.tracks_br[track_id]
        while track_br.tell() < self.track_lengths[track_id]:
            event = track_br.read_uint8()

            def post_pause(track_id1=track_id):
                self.read_pauses(track_id1)
            if event == 0x98:
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
        while track_br.tell() < self.track_lengths[track_id]:
            # prefix = f"[Track {track_id} tick: {self.current_tick}]\t"

            def post_pause(track_id1=track_id):
                self.read_events(track_id1)
            event = track_br.read_uint8()
            if event == 0x98:
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
                # print(f"{prefix}Program select: {program}")
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
            track_start = PrioritizedItem(0, lambda track_id=i: self.read_pauses(track_id))
            self.event_queue.put(track_start)
        while not self.event_queue.empty():
            task: PrioritizedItem = self.event_queue.get()
            task_start = task.priority
            task_function = task.item
            ticks_to_do = (task_start // 2) - self.current_tick
            if ticks_to_do > 0:
                self.current_tick = task_start // 2
            if callable(task_function):
                task_function()
        return self.ticks_to_samples(self.current_tick)  # 2 extra seconds

    def reset(self):
        if not self.fs:
            return
        for track_br in self.tracks_br:
            track_br.seek(0)
        self.current_tick = 0
        self.last_note_length = [0] * len(self.smd_obj.tracks)
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


class SMDStreamPlayer:
    def __init__(self):
        self.smd_sequencer: [SMDLSequencer] = None
        self.sound_obj: [pg.mixer.Sound] = None
        self.sound_buffer = None
        self.loading = False
        self.loading_finished = False
        self.buffer_offset = 0

    def update_(self):
        if self.loading:
            self.add_samples()

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

    def start_sound(self, smd_obj: smd.SMDL, volume=0.5):
        if self.sound_obj is not None:
            self.sound_obj.stop()
        if self.smd_sequencer:
            do_load = self.smd_sequencer.smd_obj is not smd_obj
        else:
            do_load = True
        if do_load:
            sample_rate = pg.mixer.get_init()[0]
            self.smd_sequencer = SMDLSequencer(smd_obj, sample_rate=sample_rate)
            length = self.smd_sequencer.compute_sample_count()
            self.smd_sequencer.reset()
            self.sound_obj = pg.sndarray.make_sound(np.zeros((length, 2), dtype=np.int16))
            self.sound_buffer = pg.sndarray.samples(self.sound_obj)
            self.loading_finished = False
            self.buffer_offset = 0
            self.add_samples(first_init=True)
        if not self.loading_finished:
            self.loading = True
        if self.smd_sequencer.loops:
            loops = -1
        else:
            loops = 0
        self.sound_obj.play(loops=loops)
        self.sound_obj.set_volume(volume)

    def stop(self):
        self.loading_finished = False
        self.loading = False
        if self.sound_obj is not None:
            self.sound_obj.stop()


if __name__ == '__main__':
    pg.init()
    with open("smd/BG_004.SMD", "rb") as smd_file:
        smd_br = binary.BinaryReader(smd_file)
        smd_obj_test = smd.SMDL()
        smd_obj_test.read(smd_br)

    samples_total = []
    smd_player = SMDStreamPlayer()
    smd_player.start_sound(smd_obj_test)

    print("Playing")
    running = True
    while running:
        events = pg.event.get()
        for pg_event in events:
            if pg_event.type == pg.QUIT:
                running = False
        smd_player.update_()
