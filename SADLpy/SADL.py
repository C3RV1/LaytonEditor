# Ported from: https://github.com/pleonex/tinke by Cervi for Team Top Hat

from .SoundBase import *
from .binaryedit.binreader import *
from .binaryedit.binwriter import *
from .Compression.IMA_ADPCM import ImaAdpcm
from .Compression.Procyon import Procyon
from io import BytesIO
from typing import Union
import time
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

        self.offset = []
        self._sample_extend = 0
        self._current_extend = 0

        self.samples_written = 0

        self._force_channels = 1

        self.pos = 0
        self.adpcm_objects = []
        self.procyon_objects = []

    def create_objects(self):
        start_offset = 0x100
        self._pcm16 = []
        self.adpcm_objects = []
        self.offset = []
        self.length = []
        self.hist = []

        for i in range(0, self._channels):
            self.offset.append(start_offset + self._block_size * i)
            self.adpcm_objects.append(ImaAdpcm())
            self.procyon_objects.append(Procyon())
            self._pcm16.append(list())

        if not self._loop_enabled:
            self.pos = start_offset
        else:
            self.pos = start_offset + self._loop_begin_sample * 2 * self._block_size

    def read_file(self, br: BinaryReader = None) -> bytearray:
        if br is None:
            br = BinaryReader(open(self._sound_file, "rb"))
        elif isinstance(br, bytes) or isinstance(br, bytearray):
            br = BinaryReader(BytesIO(br))

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
            decompressed = self.adpcm_objects[i].decompress(channel)
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
                procyon_obj: Procyon = self.procyon_objects[chan]
                temp = procyon_obj.decode_block(self.encoded[self.offset[chan]:self.offset[chan] + 0x10],
                                                samples_to_do)

                buffer[chan].extend(temp)

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

    def write_file(self, file_out: Union[str, BytesIO], data: bytearray):
        if isinstance(file_out, str):
            bw = BinaryWriter(open(file_out, "wb"))
        elif isinstance(file_out, BytesIO):
            bw = BinaryWriter(file_out)
        else:
            return
        br = BinaryReader(BytesIO(self.encoded))

        # Copy header from original file
        bw.write_bytearray(br.read_bytearray(0x100))

        # Write encoded data
        bw.write_bytearray(data)

        # Update header values
        # .. update file size
        bw.seek(0x40)
        bw.write_uint32(bw.length())

        # .. update loop size
        bw.seek(0x58)
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
        bw.write_ubyte(int(cod))

        br.close()
        if isinstance(file_out, str):
            bw.close()

    def encode(self, progress_func=None) -> bytearray:
        return self.encode_with_encoding(Coding.NDS_PROCYON, progress_func=progress_func)

    def encode_with_encoding(self, coding: int, progress_func=None) -> bytearray:
        self.sadl.coding = coding
        if coding == Coding.INT_IMA:
            return self._encode_ima_adpcm()
        elif coding == Coding.NDS_PROCYON:
            return self._encode_nds_procyon(self._pcm16, progress_func=progress_func)
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

        # self._sample_rate = 16364

        channels_compressed = []

        for i, channel in enumerate(self._pcm16):
            self.adpcm_objects[i].reset()
            compressed = self.adpcm_objects[i].compress(self._pcm16[i])
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

    def _encode_nds_procyon(self, data: list, progress_func=None) -> bytearray:
        for i in range(self._channels):
            self.procyon_objects[i].reset()
        interleave = self.sadl.interleave_block_size
        buffer = bytearray()
        offset = []
        for i in range(self._channels):
            offset.append(interleave * i)

        self.sadl.coding = Coding.NDS_PROCYON

        samples_written = 0
        start_time = time.time()
        while samples_written < self._total_samples:
            samples_to_do = 30
            if samples_written + samples_to_do > self._total_samples:
                samples_to_do = self._total_samples - samples_written

            if samples_written % 900 == 0 and samples_written != 0:
                time_diff = time.time() - start_time
                samples_per_sec = samples_written / time_diff
                time_remaining = (self._total_samples - samples_written) / samples_per_sec
                print(f"{samples_written*100/self._total_samples:.2f}%\t\t"
                      f"{samples_per_sec:.2f} samples per sec\t\t"
                      f"estimated {time_remaining:.2f}s remaining")
                if callable(progress_func):
                    if not progress_func(samples_written*100/self._total_samples):
                        return None

            for chan in range(self._channels):
                procyon_obj: Procyon = self.procyon_objects[chan]
                temp = procyon_obj.encode_block(data[chan][offset[chan]:offset[chan] + samples_to_do])

                offset[chan] += samples_to_do

                buffer.extend(temp)

            samples_written += samples_to_do
        print(f"Time taken: {time.time() - start_time:.2f}s")

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
