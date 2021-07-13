# Ported from: https://github.com/pleonex/tinke by Cervi for Team Top Hat

from .SoundBase import *
from .binaryedit.binreader import *
from .binaryedit.binwriter import *
from .Compression.IMA_ADPCM import ImaAdpcm
from .Compression.Procyon import Procyon
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
        self.interleave_block_size = 0x10


class SADL(SoundBase):
    def __init__(self, file: str, id_: int):
        SoundBase.__init__(self, file, id_, "SADL", "vgmstream", True)
        self.sadl = SADLStruct()
        self._ignore_loop = True

        self.buffer = []
        self.hist = []
        self.length = []
        self.offset = []
        self._sample_extend = 0
        self._current_extend = 0

        self.samples_written = 0

        self._force_channels = 1

        self.pos = 0
        self.ima_decompressers = []

    def create_objects(self):
        start_offset = 0x100
        self._pcm16 = []
        self.ima_decompressers = []
        self.offset = []
        self.length = []
        self.hist = []

        for i in range(0, self._channels):
            self.offset.append(start_offset + self._block_size * i)
            self.length.append(0)
            self.hist.append([I32(0), I32(0)])
            self.ima_decompressers.append(ImaAdpcm())
            self._pcm16.append(list())

        if not self._loop_enabled:
            self.pos = start_offset
        else:
            self.pos = start_offset + self._loop_begin_sample * 2 * self._block_size

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

        self.create_objects()

        self.encoded = buffer.copy()
        self._force_channels = self._channels

        return buffer

    def decode(self, sample_steps=-1) -> list:
        if self.sadl.coding == Coding.NDS_PROCYON:
            return self.decode_procyon(sample_steps=sample_steps)
        elif self.sadl.coding == Coding.INT_IMA:
            return self.decode_ima_adpcm(sample_steps=sample_steps)
        raise NotImplementedError

    def decode_ima_adpcm(self, sample_steps=-1):
        channels = []

        for i in range(self._channels):
            channels.append(bytearray())

        if sample_steps < 0:
            sample_steps = len(self.encoded)

        for i in range(0, sample_steps):
            if self.pos >= len(self.encoded):
                break
            for i in range(self._channels):
                buffer = self.encoded[self.pos:self.pos + self.sadl.interleave_block_size]
                self.pos += len(buffer)
                channels[i].extend(buffer)

        # Decompress channels
        channels_decompressed = []
        for i, channel in enumerate(channels):
            decompressed = self.ima_decompressers[i].decompress(channel)
            channels_decompressed.append(decompressed)

        for i, buff in enumerate(channels_decompressed):
            self._pcm16[i].extend(buff)
        buffer_parsed = self.convert_channels_to_samples(channels_decompressed)

        return buffer_parsed

    def decode_procyon(self, sample_steps=-1) -> list:
        buffer = []

        for i in range(self._channels):
            buffer.append([])

        if sample_steps != -1:
            sample_steps = min(self.samples_written + (sample_steps * 30), self.number_samples)
        else:
            sample_steps = self.number_samples

        while self.samples_written < sample_steps:
            samples_to_do = 30
            if self.samples_written + samples_to_do > sample_steps:
                samples_to_do = sample_steps - self.samples_written

            for chan in range(0, self._channels):
                temp = Procyon.decode(self.encoded, self.offset[chan],
                                      samples_to_do, self.hist[chan])

                buffer[chan].extend(temp)
                self.length[chan] += len(temp)

                self.offset[chan] += int(self._block_size * self._channels)

            self.samples_written += samples_to_do

        for i, buff in enumerate(buffer):
            self._pcm16[i].extend(buff)
        buffer_parsed = self.convert_channels_to_samples(buffer)

        return buffer_parsed

    def convert_channels_to_samples(self, channel_buffers):
        # Duplicate samples to match sample rate (no interpolation, still good)
        buffer_parsed = []
        for buf_off in range(len(channel_buffers[0])):
            this_buffer = [0] * self._force_channels
            for chan in range(self._force_channels):
                buffer_chan = chan % len(channel_buffers)
                this_buffer[chan] = channel_buffers[buffer_chan][buf_off]
                while self._current_extend >= 0 and chan == self._channels-1:
                    buffer_parsed.append(this_buffer)
                    self._current_extend -= 1
                if chan == self._channels-1:
                    self._current_extend += self._sample_extend
        return buffer_parsed

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
        if self._sample_rate == 16364:
            cod |= 2
        else:
            cod |= 4
        bw.write_byte(int(I8(cod)))

        br.close()
        bw.close()

    def encode_with_encoding(self, coding: int) -> bytearray:
        if coding == Coding.INT_IMA:
            return self._encode_ima_adpcm()
        elif coding == Coding.NDS_PROCYON and False:
            return self._encode_nds_procyon(self._pcm16)
        else:
            raise NotImplementedError("Encoding {} not supported".format(coding))

    def _encode_ima_adpcm(self) -> bytearray:
        # TODO: Implement stereo
        # if self._channels != 1:
        #     raise NotImplementedError("Only mono implemented")

        # TODO: Implement sample rate converter
        if self._sample_rate != 16364 and self._sample_rate != 32728:
            raise NotImplementedError("Only implemented sample rate 16364 and 32728.\n" +
                                      "This audio has {}. Please convert it.".format(self._sample_rate))

        # TODO: Implement sample bit converter
        if self._sample_bit_depth != 16:
            raise NotImplementedError("Only sample of 16 bits is allowed.\n" +
                                      "This audio has {}. Please convert it.".format(self.sample_bit_depth))

        # Force to use IMA ADPCM encoding since Procyon encoding has not been implemented yet.
        self.sadl.coding = Coding.INT_IMA
        self._sample_rate = 16364

        # self._sample_rate = 32728

        channels_compressed = []

        for i, channel in enumerate(self._pcm16):
            self.ima_decompressers[i].reset()
            compressed = self.ima_decompressers[i].compress(self._pcm16[i])
            channels_compressed.append(compressed)

            rest = len(channels_compressed[-1]) % (self.sadl.interleave_block_size * 2)
            if rest != 0:
                channels_compressed[-1].extend(b"\x00" * ((self.sadl.interleave_block_size * 2) - rest))

        merged_channels = bytearray()

        self._block_size = self.sadl.interleave_block_size
        for i in range(0, len(channels_compressed[0]), self._block_size):
            for channel in channels_compressed:
                merged_channels += channel[i:i+self._block_size]

        return merged_channels

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
