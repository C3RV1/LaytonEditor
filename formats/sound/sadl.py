import math

from formats.binary import BinaryReader, BinaryWriter
from formats.sound.sadl_compression import ima_adpcm, procyon
from formats.sound.wav import WAV
from formats.filesystem import FileFormat
import numpy as np
from typing import List


# TODO: add loop support


class Coding:
    EMPTY = 0
    INT_IMA = 0x70
    NDS_PROCYON = 0xB0


class SADL(FileFormat):
    chunk_id: bytes
    original_header: bytes

    file_size: int
    loop_flag: int
    loop_offset: int
    channels: int
    coding: int
    sample_rate: int
    num_samples: int
    interleave_block_size: int = 0x10

    buffer: np.ndarray

    ima_decoders: List[ima_adpcm.ImaAdpcm]
    procyon_decoders: List[procyon.Procyon]
    blocks_done: int
    offset: List[int]

    def read_stream(self, stream):
        if not isinstance(stream, BinaryReader):
            rdr = BinaryReader(stream)
        else:
            rdr = stream
        self.original_header = rdr.read(0x100)
        rdr.seek(0)

        self.chunk_id = rdr.read(4)
        if self.chunk_id != b"sadl":
            raise ValueError("SADL does not start with magic value")
        rdr.seek(0x31)
        self.loop_flag = rdr.read_uint8()
        self.channels = rdr.read_uint8()

        coding = rdr.read_uint8()
        if coding & 0x06 == 4:
            self.sample_rate = 32728
        elif coding & 0x06 == 2:
            self.sample_rate = 16364
        self.coding = coding & 0xf0

        rdr.seek(0x40)
        self.file_size = rdr.read_uint32()

        if self.coding == Coding.INT_IMA:
            self.num_samples = int((self.file_size - 0x100) / self.channels * 2)
        elif self.coding == Coding.NDS_PROCYON:
            self.num_samples = int((self.file_size - 0x100) / self.channels / 16 * 30)
        else:
            raise NotImplementedError()

        rdr.seek(0x54)
        if self.loop_flag != 0:
            if self.coding == Coding.INT_IMA:
                self.loop_offset = int((rdr.read_uint32() - 0x100) / self.channels * 2)
            elif self.coding == Coding.NDS_PROCYON:
                self.loop_offset = int((rdr.read_uint32() - 0x100) / self.channels / 16 * 30)

        rdr.seek(0x100)
        buffer = rdr.read(self.file_size - 0x100)
        buffer = np.frombuffer(buffer, dtype=np.uint8)
        buffer = buffer.reshape(((self.file_size - 0x100) // 0x10 // self.channels, self.channels, 0x10))
        buffer = buffer.swapaxes(0, 1)
        self.buffer = buffer.reshape((buffer.shape[0], buffer.shape[1] * buffer.shape[2]))
        self.offset = [0] * self.channels
        self.ima_decoders = []
        self.procyon_decoders = []
        for i in range(self.channels):
            self.ima_decoders.append(ima_adpcm.ImaAdpcm())
            self.procyon_decoders.append(procyon.Procyon())
        self.blocks_done = 0

    def write_stream(self, stream):
        if not isinstance(stream, BinaryWriter):
            wtr = BinaryWriter(stream)
        else:
            wtr = stream

        wtr.write(self.original_header)
        wtr.seek(0)
        wtr.write(self.chunk_id)
        wtr.seek(0x31)
        wtr.write_uint8(self.loop_flag)
        wtr.write_uint8(self.channels)

        coding = self.coding
        if self.sample_rate == 32728:
            coding |= 4
        elif self.sample_rate == 16364:
            coding |= 2
        else:
            raise NotImplementedError()

        wtr.seek(0x100)
        buffer = self.buffer.copy()
        buffer = buffer.reshape((buffer.shape[0], buffer.shape[1] // 0x10, 0x10))
        buffer = buffer.swapaxes(0, 1)
        wtr.write(buffer.tobytes())

        size = wtr.tell()
        wtr.seek(0x40)
        wtr.write_uint32(size)
        wtr.seek(0x58)
        wtr.write_uint32(size)

    def decode(self, blocks=-1):
        if self.coding == Coding.INT_IMA:
            if blocks == -1:
                blocks = self.num_samples // 2 // 0x10 - self.blocks_done
            decoded = np.zeros((self.channels, blocks * 32))
            for chan in range(self.channels):
                for i in range(blocks):
                    if i + self.blocks_done == self.num_samples // 2 // 0x10:
                        continue
                    block = self.buffer[chan][self.offset[chan]:self.offset[chan]+0x10]
                    decoded_block = self.ima_decoders[chan].decompress(block)
                    self.offset[chan] += 0x10 * self.channels
                    decoded[chan][i:i+32] = decoded_block
            self.blocks_done += blocks
        elif self.coding == Coding.NDS_PROCYON:
            if blocks == -1:
                blocks = self.num_samples // 30 - self.blocks_done
            decoded = np.zeros((self.channels, blocks * 30), dtype=np.int16)
            for chan in range(self.channels):
                for i in range(blocks):
                    if i + self.blocks_done >= self.num_samples // 30:
                        break
                    block = self.buffer[chan][self.offset[chan]:self.offset[chan]+0x10]
                    self.procyon_decoders[chan].decode_block(block, decoded[chan][i*30:(i*30)+30])
                    self.offset[chan] += 0x10
            self.blocks_done += blocks
        else:
            raise NotImplementedError()
        return decoded

    def to_wav(self) -> WAV:
        wav = WAV()
        wav.fmt.num_channels = self.channels
        wav.fmt.sample_rate = self.sample_rate
        wav.fmt.bits_per_sample = 0x10
        wav.data.data = self.decode()
        return wav

    def from_wav(self, wav: WAV):
        self.channels = wav.fmt.num_channels
        if self.channels > 2:
            self.channels = 2
        self.sample_rate = wav.fmt.sample_rate
        if self.sample_rate <= 16364:
            self.sample_rate = 16364
        else:
            self.sample_rate = 32728
        wav.change_channels(self.channels)
        wav.change_sample_rate(self.sample_rate)
        with open("test_change_sample_rate.wav", "wb") as f:
            wav.write_stream(f)
        decoded = wav.data.data
        self.encode(decoded)

    def encode(self, decoded: np.ndarray):
        self.num_samples = decoded.shape[1]
        # Professor Layton 2 only supports Procyon encoding
        self.coding = Coding.NDS_PROCYON
        self.buffer = np.zeros((decoded.shape[0], int(math.ceil(self.num_samples / 30)) * 16), dtype=np.uint8)

        self.procyon_decoders = []
        self.offset = []
        for i in range(self.channels):
            self.procyon_decoders.append(procyon.Procyon())
            self.offset.append(0)

        print(f"Encoding {self.num_samples} samples")

        for chan in range(self.channels):
            buffer_off = 0
            for i in range(0, self.num_samples, 30):
                block = decoded[chan][i:i+30]
                decoded_block = self.procyon_decoders[chan].encode_block(block)
                self.buffer[chan][buffer_off:buffer_off + 0x10] = decoded_block
                buffer_off += 0x10
            self.procyon_decoders[chan].reset()
            self.offset[chan] = 0
        self.blocks_done = 0
