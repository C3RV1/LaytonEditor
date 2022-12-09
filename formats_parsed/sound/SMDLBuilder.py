import logging

import mido
from formats.sound.smdl.smdl import SMDL, Track
from formats.binary import BinaryWriter
from formats import conf


class SMDLBuilderMidi:
    def __init__(self, smd: SMDL):
        self.smd = smd

    PAUSE_TICKS = [96, 72, 64, 48, 36, 32, 24, 18, 16, 12, 9, 8, 6, 4, 3, 2]

    def build_midi(self, midi: mido.MidiFile):
        self.smd.tracks = []
        for i, track in enumerate(midi.tracks):
            track: mido.MidiTrack
            if conf.DEBUG_AUDIO:
                logging.debug(f"Track {i}")

            smd_track = Track()
            self.smd.tracks.append(smd_track)
            smd_track.track_preamble.track_id = i
            smd_track.track_preamble.channel_id = max(i - 1, 0)

            track_bw = BinaryWriter()

            current_tick = 0
            last_delay = 0

            def add_pause(midi_ticks):
                nonlocal last_delay
                if conf.DEBUG_AUDIO:
                    logging.debug(f"Adding pause of {midi_ticks} midi ticks")
                while midi_ticks > 0:
                    if midi_ticks == last_delay:  # same delay
                        track_bw.write_uint8(0x90)
                        last_delay = midi_ticks
                    elif midi_ticks in self.PAUSE_TICKS:
                        track_bw.write_uint8(self.PAUSE_TICKS.index(midi_ticks) + 0x80)
                        last_delay = midi_ticks
                    elif 1 <= midi_ticks - last_delay <= 0xFF and last_delay != 0:
                        track_bw.write_uint8(0x91)
                        track_bw.write_uint8(midi_ticks - last_delay)
                        last_delay = midi_ticks
                    elif midi_ticks <= 0xFF:
                        track_bw.write_uint8(0x92)
                        track_bw.write_uint8(midi_ticks)
                        last_delay = midi_ticks
                    elif midi_ticks <= 0xFFFF:
                        track_bw.write_uint8(0x93)
                        track_bw.write_uint16(midi_ticks)
                        last_delay = midi_ticks
                    elif midi_ticks <= 0xFFFFFF:
                        track_bw.write_uint8(0x94)
                        track_bw.write_uint16(midi_ticks & 0xFFFF)
                        track_bw.write_uint8((midi_ticks & 0xFF0000) >> 16)
                        last_delay = midi_ticks
                    else:
                        track_bw.write_uint8(0x94)
                        track_bw.write_uint16(0xFFFF)
                        track_bw.write_uint8(0xFF)
                        last_delay = 0xFFFFFF
                    midi_ticks -= last_delay

            note_pairs = []
            pending_close_notes = {}
            current_octave = 0
            last_note_length = 0

            current_tick = 0
            for msg in track:
                current_tick += msg.time
                if msg.type == "note_on":
                    note_pairs.append([msg, None])
                    pending_close_notes[msg.note] = note_pairs[-1]
                elif msg.type == "note_off":
                    pending_close = pending_close_notes.pop(msg.note)
                    pending_close[1] = current_tick

            current_tick = 0
            current_smdl_tick = 0

            def write_event(ev):
                nonlocal current_smdl_tick
                tick_diff = current_tick - current_smdl_tick
                add_pause(tick_diff)
                current_smdl_tick = current_tick
                track_bw.write_uint8(ev)

            for msg in track:
                current_tick += msg.time
                if msg.type == "note_off":
                    continue
                if msg.type == "set_tempo":
                    write_event(0xa4)
                    track_bw.write_uint8(int(round(mido.tempo2bpm(msg.tempo))))
                elif msg.type == "note_on":
                    note_pair = note_pairs.pop(0)

                    assert note_pair[0] == msg
                    if conf.DEBUG_AUDIO:
                        logging.debug(f"{msg} ending on {note_pair[1]}")

                    duration = note_pair[1] - current_tick

                    octave = msg.note // 12
                    octave_diff = octave - current_octave
                    current_octave = octave
                    if abs(octave_diff) > 1:
                        write_event(0xa0)
                        track_bw.write_uint8(octave)
                        octave_diff = 0

                    note = msg.note % 12
                    write_event(msg.velocity)  # event is velocity

                    note_data = (octave_diff + 2) << 4
                    note_data += note
                    if last_note_length == duration:
                        track_bw.write_uint8(note_data)
                    else:
                        last_note_length = duration
                        duration_values = []
                        param_count = 0
                        while 1:
                            duration_values.insert(0, duration & 0xFF)
                            duration >>= 8
                            param_count += 1
                            if duration == 0:
                                break
                        note_data += param_count << 6
                        track_bw.write_uint8(note_data)
                        for duration_value in duration_values:
                            track_bw.write_uint8(duration_value)
                elif msg.type == "control_change":
                    if msg.control == 0x07:  # volume
                        write_event(0xe0)
                    elif msg.control == 0x0B:  # expression
                        write_event(0xe3)
                    elif msg.control == 0x0a:  # pan
                        write_event(0xe8)
                    track_bw.write_uint8(msg.value)
                elif msg.type == "program_change":
                    write_event(0xac)
                    track_bw.write_uint8(msg.program)
                elif msg.type == "pitchwheel":
                    write_event(0xd7)
                    track_bw.write_uint16(msg.pitch)
                elif msg.type == "end_of_track":
                    write_event(0x98)
                elif msg.type == "text":
                    if msg.text == "start_loop":
                        write_event(0x99)
                else:
                    if conf.DEBUG_AUDIO:
                        logging.debug(f"MSG not implemented {msg}")

            smd_track.track_content.event_bytes = track_bw.getvalue()
