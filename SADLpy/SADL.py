# Ported from: https://github.com/pleonex/tinke by Cervi for Team Top Hat

from .SoundBase import *
from .binaryedit.binreader import *
from .binaryedit.binwriter import *
from .Compression.IMA_ADPCM import ImaAdpcm
from .Compression.Procyon import Procyon
from .Helper import Helper
from cint.cint import I32, I8
import math


class Coding:
    EMPTY = 0
    INT_IMA = 0x70
    NDS_PROCYON = 0xB0


class SADLStruct:
    def __init__(self):
        self.id_ = bytes()
        self.file_size = 0
        self.loop_flag = 0
        self.loop_offset = 0
        self.channel = 0
        self.coding = Coding.EMPTY
        self.sample_rate = 0
        self.num_samples = 0
        self.interleave_block_size = 0


class SADL(SoundBase):
    def __init__(self, file: str, id_: int, print_info: bool = False):
        SoundBase.__init__(self, file, id_, "SADL", "vgmstream", True)
        self.sadl = SADLStruct()
        self._ignore_loop = True
        self._print_info = print_info
        start_offset = I32(0x100)

        self.buffer = []
        self.hist = []
        self.length = []
        self.offset = []
        self._sample_extend = 0
        self._current_extend = 0

        self.samples_written = I32(0)

        self._force_channels = 1

    def read_file(self) -> bytearray:
        br = BinaryReader(open(self._sound_file, "rb"))

        self.sadl.id_ = br.read_chars(4)

        br.seek(0x31)
        self.sadl.loop_flag = br.read_byte()
        self.sadl.channel = br.read_byte()

        coding = br.read_byte()
        self.sadl.coding = coding & 0xf0

        if coding & 0x06 == 4:
            self.sadl.sample_rate = 32728
        elif coding & 0x06 == 2:
            self.sadl.sample_rate = 16364

        br.seek(0x40)
        self.sadl.file_size = br.read_uint32()

        start_offset = 0x100
        if self.sadl.coding == Coding.INT_IMA:
            self.sadl.num_samples = int((self.sadl.file_size - start_offset) / self.sadl.channel * 2)
        elif self.sadl.coding == Coding.NDS_PROCYON:
            self.sadl.num_samples = int((self.sadl.file_size - start_offset) / self.sadl.channel / 16 * 30)

        self.sadl.interleave_block_size = 0x10

        br.seek(0x54)
        if self.sadl.loop_flag != 0:
            if self.sadl.coding == Coding.INT_IMA:
                self.sadl.loop_offset = int((br.read_uint32() - start_offset) / self.sadl.channel * 2)
            elif self.sadl.coding == Coding.NDS_PROCYON:
                self.sadl.loop_offset = int((br.read_uint32() - start_offset) / self.sadl.channel / 16 * 30)

        self._total_samples = self.sadl.num_samples
        self._sample_rate = self.sadl.sample_rate
        self._channels = self.sadl.channel
        self._block_size = self.sadl.interleave_block_size
        self._sample_bit_depth = 4

        self._loop_enabled = bool(self.sadl.loop_flag != 0)
        self._loop_begin_sample = self.sadl.loop_offset
        self._loop_end_sample = self.sadl.num_samples

        br.seek(0)
        buffer = br.read_bytearray(br.length())

        br.close()

        for i in range(0, self._channels):
            self.offset.append(start_offset + self._block_size * i)
            self.length.append(I32(0))
            self.hist.append([I32(0), I32(0)])

        self.encoded = buffer.copy()
        self._force_channels = self._channels

        return buffer

    def decode(self, encoded: bytearray, loop_enabled: bool) -> bytearray:
        if self.sadl.coding == Coding.NDS_PROCYON:
            return self.decode_procyon(encoded)
        raise NotImplementedError()

        start_offset = I32(0x100)
        pos = 0

        if not self._loop_enabled:
            pos = start_offset
        else:
            pos = start_offset + self._loop_begin_sample * 2 * self._block_size

        left_channel = bytearray()
        right_channel = bytearray()
        data = bytearray()

        while pos < len(encoded):
            if self.sadl.channel == 2:  # Stereo
                buffer = encoded[pos:pos + self.sadl.interleave_block_size]
                pos += len(buffer)
                left_channel.extend(buffer)

                buffer = encoded[pos:pos + self.sadl.interleave_block_size]
                pos += len(buffer)
                right_channel.extend(buffer)
            else:  # Mono
                buffer = encoded[pos:pos + self.sadl.interleave_block_size * 2]
                pos += len(buffer)
                data.extend(buffer)

        # Decompress channels
        if self.sadl.coding == Coding.INT_IMA:
            if self.sadl.channel == 2:
                d_left_channel = ImaAdpcm.decompress(left_channel)

                d_right_channel = ImaAdpcm.decompress(right_channel)

                data.extend(Helper.merge_channels(d_left_channel, d_right_channel))
            else:
                data = ImaAdpcm.decompress(data)

        return data

    def decode_procyon(self, sample_steps=-1) -> list:
        buffer = []

        for i in range(0, self._channels):
            buffer.append([])

        if sample_steps != -1:
            sample_steps = min(self.samples_written + (sample_steps * 30), self.number_samples)
        else:
            sample_steps = self.number_samples

        while self.samples_written < sample_steps:
            samples_to_do = I32(30)
            if self.samples_written + samples_to_do > sample_steps:
                samples_to_do = sample_steps - self.samples_written

            for chan in range(0, self._channels):
                temp = Procyon.decode(self.encoded, self.offset[chan],
                                      samples_to_do, self.hist[chan])

                buffer[chan].extend(temp)
                self.length[chan] += len(temp)

                self.offset[chan] += int(self._block_size * self._channels)

            self.samples_written += samples_to_do

        # Duplicate samples to match sample rate (no interpolation, still good)
        buffer_parsed = []
        for buf_off in range(len(buffer[0])):
            this_buffer = [0] * self._force_channels
            for chan in range(self._force_channels):
                buffer_chan = chan % len(buffer)
                this_buffer[chan] = buffer[buffer_chan][buf_off]
                while self._current_extend >= 0 and chan == 1:
                    buffer_parsed.append(this_buffer)
                    self._current_extend -= 1
                if chan == 1:
                    self._current_extend += self._sample_extend

        return buffer_parsed

    def _encode(self, data: bytearray) -> bytearray:
        # TODO: Implement stereo
        if self.channels != 1:
            raise NotImplementedError("Only mono implemented")

        # TODO: Implement sample rate converter
        if self.sample_rate != 16362 and self.sample_rate != 32728:
            raise NotImplementedError("Only implemented sample rate 16364 and 32728.\n" +
                                      "This audio has {}. Please convert it.".format(self.sample_rate))

        # TODO: Implement sample bit converter
        if self.sample_bit_depth != 16:
            raise NotImplementedError("Only sample of 16 bits is allowed.\n" +
                                      "This audio has {}. Please convert it.".format(self.sample_bit_depth))

        # Force to use IMA ADPCM encoding since Procyon encoding has not been implemented yet.
        self.sadl.coding = Coding.INT_IMA
        encoded = ImaAdpcm.compress(data)

        self._block_size = self.sadl.interleave_block_size
        rest = len(encoded) % (self.sadl.interleave_block_size * 2)
        if rest != 0:
            encoded.extend(b"\x00"*((self.sadl.interleave_block_size * 2) - rest))

        return encoded

    def write_file(self, file_out: str, data: bytearray):
        bw = BinaryWriter(open(file_out, "wb"))
        br = BinaryReader(open(self._sound_file, "rb"))

        # Copy header from original file
        bw.write_bytearray(br.read_bytearray(0x100))

        # Write encoded data
        bw.write_bytearray(data)

        # Update header values
        # .. update file size
        bw.seek(0x40)
        bw.write_uint32(bw.length())

        # .. update channels
        bw.seek(0x32)
        bw.write_byte(self._channels)

        # ..update encoding and sample rate values
        bw.seek(0x33)
        br.seek(0x33)
        cod = br.read_byte()
        cod &= 0x09
        cod |= self.sadl.coding
        if self.sample_rate == 16364:
            cod |= 2
        else:
            cod |= 4
        bw.write_byte(int(I8(cod)))

        br.close()
        bw.close()

    def encode_with_encoding(self, coding: int) -> bytearray:
        if coding == Coding.INT_IMA:
            return self._encode_ima_adpcm(self._pcm16)
        elif coding == Coding.NDS_PROCYON:
            return self._encode_nds_procyon(self._pcm16)
        else:
            raise NotImplementedError("Encoding {} not supported".format(coding))

    def _encode_ima_adpcm(self, data: bytearray) -> bytearray:
        # TODO: Implement stereo
        if self._channels != 1:
            raise NotImplementedError("Only mono implemented")

        # TODO: Implement sample rate converter
        if self.sample_rate != 16362 and self.sample_rate != 32728:
            raise NotImplementedError("Only implemented sample rate 16364 and 32728.\n" +
                                      "This audio has {}. Please convert it.".format(self.sample_rate))

        # TODO: Implement sample bit converter
        if self.sample_bit_depth != 16:
            raise NotImplementedError("Only sample of 16 bits is allowed.\n" +
                                      "This audio has {}. Please convert it.".format(self.sample_bit_depth))

        # Force to use IMA ADPCM encoding since Procyon encoding has not been implemented yet.
        self.sadl.coding = Coding.INT_IMA
        encoded = ImaAdpcm.compress(data)

        self._block_size = self.sadl.interleave_block_size
        rest = len(encoded) % (self.sadl.interleave_block_size * 2)
        if rest != 0:
            encoded.extend(b"\x00" * ((self.sadl.interleave_block_size * 2) - rest))

        return encoded

    def _encode_nds_procyon(self, data: bytearray) -> bytearray:
        interleave = 60
        buffer = bytearray()
        offset = []
        hist = []
        for i in range(self._channels):
            offset.append(interleave * i)
            hist.append([I32(0), I32(0)])

        self.sadl.coding = Coding.NDS_PROCYON

        samples_written = 0
        while samples_written < self.number_samples - 60:
            samples_to_do = 30
            if samples_written + samples_to_do > self.number_samples:
                samples_to_do = self.number_samples - samples_written - 60

            for chan in range(self._channels):
                temp = Procyon.encode(data, offset[chan], hist[chan], samples_to_do=samples_to_do)

                offset[chan] += interleave * self._channels

                buffer.extend(temp)

            samples_written += samples_to_do

        return buffer

    @property
    def sample_extend(self):
        return self._sample_extend

    @sample_extend.setter
    def sample_extend(self, value):
        self._sample_extend = value
        self._current_extend = self._sample_extend

    @property
    def sample_rate(self):
        return self._sample_rate * self.sample_extend

    @property
    def alloc_size(self):
        return int(math.ceil(self.number_samples * self.sample_extend))

    @sample_rate.setter
    def sample_rate(self, value):
        self.sample_extend = value / self._sample_rate

    @property
    def channels(self):
        return self._force_channels

    @channels.setter
    def channels(self, value):
        self._force_channels = value
