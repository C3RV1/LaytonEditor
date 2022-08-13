import logging
from formats.sound.smdl import smdl
from formats.sound.smdl.SMDLSequencer import SMDLSequencer
import numpy as np


try:
    import custom_fluidsynth.custom_fluidsynth as fluidsynth
except ImportError as e:
    # Can still run without the synth
    logging.warning(f"Error importing fluidsynth: {e}")
    fluidsynth = None


class SMDLFluidSynthSequencer(SMDLSequencer):
    def __init__(self, smd_obj: smdl.SMDL, sample_rate=44100, loops=True):
        super(SMDLFluidSynthSequencer, self).__init__(smd_obj, sample_rate=sample_rate, loops=loops)

        if fluidsynth is None:
            self.fs = None
            return
        self.fs = fluidsynth.ModifiedSynth(samplerate=self.sample_rate, gain=0.5)
        self.sf_id = 0
        self.sf2_path = None

    def load_sf2(self, sf2_path):
        self.sf2_path = sf2_path
        self.sf_id = self.fs.sfload(sf2_path)

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
        return fluidsynth is not None

    def reset(self):
        super(SMDLFluidSynthSequencer, self).reset()
        self.fs = fluidsynth.ModifiedSynth(samplerate=self.sample_rate, gain=0.5)
        if self.sf2_path is not None:
            self.sf_id = self.fs.sfload(self.sf2_path)
