from typing import List

from formats.sound.smdl.SMDLSequencer import SMDLSequencer
from formats.sound.smdl import smdl
import mido


class SMDLMidiSequencer(SMDLSequencer):
    def __init__(self, smd_obj: smdl.SMDL):
        super(SMDLMidiSequencer, self).__init__(smd_obj, loops=False)

        self.last_midi_tick = [0] * len(self.smd_obj.tracks)
        self.midi_file = mido.MidiFile(type=2)
        self.midi_file.ticks_per_beat = self.smd_obj.song_chunk.tpqn
        self.tracks: List[mido.MidiTrack] = []
        for i in range(len(self.smd_obj.tracks)):
            self.tracks.append(mido.MidiTrack())
            self.midi_file.tracks.append(self.tracks[-1])

    def set_time_delta(self, channel):
        time_delta = self.current_tick - self.last_midi_tick[channel]
        self.last_midi_tick[channel] = self.current_tick
        if len(self.tracks[channel]) > 0:
            prev_msg: mido.Message = self.tracks[channel][-1]
            prev_msg.time = time_delta

    def note_on(self, channel, midi_note, velocity):
        track: mido.MidiTrack = self.tracks[channel]
        track.append(mido.Message('note_on', channel=channel, note=midi_note, velocity=velocity))
        self.set_time_delta(channel)

    def note_off(self, channel, midi_note):
        track: mido.MidiTrack = self.tracks[channel]
        track.append(mido.Message('note_off', channel=channel, note=midi_note))
        self.set_time_delta(channel)

    def start_loop(self, channel):
        pass

    def set_octave(self, channel, octave):
        pass

    def mod_octave(self, channel, octave_mod):
        pass

    def set_bpm(self, channel, bpm):
        track: mido.MidiTrack = self.tracks[channel]
        track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm)))
        self.set_time_delta(channel)

    def set_program(self, channel, program):
        track: mido.MidiTrack = self.tracks[channel]
        track.append(mido.Message('program_change', channel=channel, program=program))
        self.set_time_delta(channel)

    def pitch_bend(self, channel, pitch_bend):
        track: mido.MidiTrack = self.tracks[channel]
        try:
            track.append(mido.Message('pitchwheel', channel=channel, pitch=pitch_bend))
        except ValueError:  # bend out of midi range (ignore?)
            pass
        self.set_time_delta(channel)

    def change_volume(self, channel, volume):
        track: mido.MidiTrack = self.tracks[channel]
        track.append(mido.Message('control_change', channel=channel, control=0x07, value=volume))
        self.set_time_delta(channel)

    def change_expression(self, channel, expression):
        track: mido.MidiTrack = self.tracks[channel]
        track.append(mido.Message('control_change', channel=channel, control=0x0B, value=expression))
        self.set_time_delta(channel)

    def change_pan(self, channel, pan):
        track: mido.MidiTrack = self.tracks[channel]
        track.append(mido.Message('control_change', channel=channel, control=0x0a, value=pan))
        self.set_time_delta(channel)

    def generate_mid(self) -> mido.MidiFile:
        self.generate_samples(-1)
        return self.midi_file
