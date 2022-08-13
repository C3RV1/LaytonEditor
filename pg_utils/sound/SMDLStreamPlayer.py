import os

from formats.sound.smdl import smdl
import numpy as np

from pg_utils.sound.StreamPlayerAbstract import StreamPlayerAbstract
from formats.sound import sample_transform
from formats.sound import sf2, swdl
from typing import Optional
from pg_utils.sound.SMDLFluidSynthSequencer import SMDLFluidSynthSequencer

import pygame as pg


# in the smdl format different tracks can loop at different points
# if we want to loop a smdl stream we can't use pygame default, which would loop the whole Sound object
# instead we create a Sound object with a default size (10 seconds for example)
# then, we create a variable which tracks the current buffer position
# when using this buffer position, we clip it to the actual sound buffer
# Example:
#
# player
# pointer   (pointer and player at the same position on startup)
# ↓
# | Sound Buffer |
#
# player  pointer (the pointer loads sound in front of the player)
#     ↓-LOAD-↓
# | Sound Buffer |
#
#  pointer player (the pointer loads sound in front of the player and loops back, overwriting the old data)
# -LOAD-↓       ↓-LOAD-
# | Sound Buffer |


class SMDLStreamPlayer(StreamPlayerAbstract):
    SOUND_SECONDS = 10
    LOAD_SECONDS = 0.25

    def __init__(self, loops=False):
        super(SMDLStreamPlayer, self).__init__(loops=loops)
        self.smd_sequencer: Optional[SMDLFluidSynthSequencer] = None
        self.tmp_sf2_path = None
        self.buffer_size = 0
        self.load_size = 0

    def create_temporal_sf2(self, swd_file: swdl.SWDL, sample_bank: swdl.SWDL):
        sf = sf2.SoundFont()
        sf.samples = swd_file.samples
        sf.programs = swd_file.programs
        sf.set_sample_data(sample_bank.samples)
        if not os.path.isdir(os.getcwd() + f"\\temporary"):
            os.mkdir(os.getcwd() + f"\\temporary")
        self.tmp_sf2_path = os.getcwd() + f"\\temporary\\temp_sf2.sf2"
        with open(self.tmp_sf2_path, "wb") as f:
            sf.write_stream(f)

    def add_samples(self, first_init=False):
        target_buffer_position = self.expected_buffer_position + self.load_size
        samples_to_do = target_buffer_position - self.buffer_offset
        ticks_to_do = self.smd_sequencer.samples_to_ticks(samples_to_do)
        if ticks_to_do <= 0:
            return
        new_samples = self.smd_sequencer.generate_samples(ticks_to_do)
        new_samples = new_samples.swapaxes(0, 1)
        new_samples = sample_transform.change_channels(new_samples, self.channels)
        new_samples = new_samples.swapaxes(0, 1)
        if new_samples.shape[0] == 0:
            self.loading = False
            return
        new_samples_pos = 0
        new_samples_remain = new_samples.shape[0]
        while new_samples_remain > 0:
            # write all possible samples until the end of the buffer, then loop back and overwrite

            expected_end = self.buffer_offset + new_samples_remain  # where are we supposed to stop writing
            # max buffer (ex. buf_size=8: buf_pos=5 -> buf_max=8, buf_pos=11 -> buf_max=16)
            #             f(buf_pos) = (floor(buf_pos / buf_size) + 1) * buf_size
            buffer_max = (int(self.buffer_offset / self.buffer_size) + 1) * self.buffer_size
            buffer_end = min(expected_end, buffer_max)

            new_samples_trim = expected_end - buffer_end  # how many samples can't we fit
            new_samples_copy_length = new_samples_remain - new_samples_trim  # how many samples can we write
            new_samples_end = new_samples_copy_length + new_samples_pos  # the end of where we have to copy from

            buffer_pos_real = self.buffer_offset % self.buffer_size  # the real buffer position
            # the real buffer end position (ex. buf_size=8: end=5, real_end=5, end=11, real_end=3, end=8, real_end=8)
            #                              f(end) = (end - 1) % buf_size + 1
            buffer_end_real = (buffer_end - 1) % self.buffer_size + 1

            # copy the buffer
            self.sound_buffer[buffer_pos_real:buffer_end_real] = new_samples[new_samples_pos:new_samples_end]

            # change offsets and remaining
            new_samples_pos += new_samples_copy_length
            new_samples_remain -= new_samples_copy_length
            self.buffer_offset = buffer_end

    def _load_sound(self, snd_obj: smdl.SMDL):
        if not SMDLFluidSynthSequencer.get_dependencies_met() or self.tmp_sf2_path is None:
            return False
        self.buffer_size = self.SOUND_SECONDS * self.sample_rate
        self.load_size = self.LOAD_SECONDS * self.sample_rate
        self.smd_sequencer = SMDLFluidSynthSequencer(snd_obj, sample_rate=self.sample_rate)
        self.smd_sequencer.load_sf2(self.tmp_sf2_path)
        self.sound_obj = pg.sndarray.make_sound(np.zeros((self.buffer_size, self.channels), dtype=np.int16))
        self.sound_buffer = pg.sndarray.samples(self.sound_obj)
        return True

    def stop(self):
        if not self.playing:
            return
        super(SMDLStreamPlayer, self).stop()

    def play(self):
        if self.playing:
            self.stop()
        if self.expected_buffer_position != 0:
            # SMDL requires reset when stopping
            self.smd_sequencer.reset()
            self.smd_sequencer.loops = self.loops
            self.buffer_offset = 0
            self.expected_buffer_position = 0
            self.loading = True
            self.add_samples(first_init=True)

        self.channel = self.sound_obj.play(loops=-1)  # SMDL ignores loops
        self.playing = True
        self.paused = False

    @staticmethod
    def get_playable():
        return SMDLFluidSynthSequencer.get_dependencies_met()
