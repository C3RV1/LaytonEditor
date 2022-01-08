import os
from formats.sound import smdl
from formats.sound.SMDLSequencer import SMDLSequencer
import numpy as np


try:
    import custom_fluidsynth.custom_fluidsynth as fluidsynth
except ImportError as e:
    # Can still run without the synth
    print(f"Error importing fluidsynth: {e}")
    fluidsynth = None


class SMDLFluidSynthSequencer(SMDLSequencer):
    def __init__(self, smd_obj: smdl.SMDL, sample_rate=44100, loops=True):
        super(SMDLFluidSynthSequencer, self).__init__(smd_obj, sample_rate=sample_rate, loops=loops)

        sf2_path = os.path.join(os.getcwd(), "layton2.sf2")
        if fluidsynth is None or not os.path.isfile(sf2_path):
            self.fs = None
            return
        self.fs = fluidsynth.Synth(samplerate=self.sample_rate, gain=0.5)
        self.sf_id = self.fs.sfload(sf2_path)
        self.fs.program_select(0, self.sf_id, 0, 0)

    def note_on(self, channel, midi_note, velocity):
        self.fs.noteon(channel, midi_note, velocity)

    def note_off(self, channel, midi_note):
        self.fs.noteoff(channel, midi_note)

    def start_loop(self, channel):
        pass

    def set_octave(self, channel, octave):
        pass

    def mod_octave(self, channel, octave_mod):
        pass

    def set_bpm(self, channel, bpm):
        pass

    def set_program(self, channel, program):
        self.fs.program_select(channel, self.sf_id, 0, program)

    def pitch_bend(self, channel, pitch_bend):
        self.fs.pitch_bend(channel, pitch_bend)

    def change_volume(self, channel, volume):
        self.fs.cc(channel, 0x07, volume)

    def change_expression(self, channel, expression):
        self.fs.cc(channel, 0x0B, expression)

    def change_pan(self, channel, pan):
        self.fs.cc(channel, 0x0a, pan)

    def generate_samples_from_ticks(self, ticks) -> np.ndarray:
        array = self.fs.get_samples(self.ticks_to_samples(ticks))
        array = np.swapaxes(array, 0, 1)
        return array

    def end_channel(self, channel):
        pass

    @staticmethod
    def get_dependencies_met():
        sf2_path = os.path.join(os.getcwd(), "layton2.sf2")
        return fluidsynth is not None and os.path.isfile(sf2_path)
