# Thanks to https://projectpokemon.org/docs/mystery-dungeon-nds/dse-swdl-format-r14/
import logging
from typing import List, Dict, Optional

import numpy as np

from formats import conf
from formats.binary import BinaryReader
from formats.filesystem import FileFormat, NintendoDSRom
from formats.sound.sound_types import Sample, KeyGroup, Split, LFO, Program


VOLUME_ENVELOPE_TABLE_16BIT = [
    0x0000, 0x0001, 0x0002, 0x0003, 0x0004, 0x0005, 0x0006, 0x0007,
    0x0008, 0x0009, 0x000A, 0x000B, 0x000C, 0x000D, 0x000E, 0x000F,
    0x0010, 0x0011, 0x0012, 0x0013, 0x0014, 0x0015, 0x0016, 0x0017,
    0x0018, 0x0019, 0x001A, 0x001B, 0x001C, 0x001D, 0x001E, 0x001F,
    0x0020, 0x0023, 0x0028, 0x002D, 0x0033, 0x0039, 0x0040, 0x0048,
    0x0050, 0x0058, 0x0062, 0x006D, 0x0078, 0x0083, 0x0090, 0x009E,
    0x00AC, 0x00BC, 0x00CC, 0x00DE, 0x00F0, 0x0104, 0x0119, 0x012F,
    0x0147, 0x0160, 0x017A, 0x0196, 0x01B3, 0x01D2, 0x01F2, 0x0214,
    0x0238, 0x025E, 0x0285, 0x02AE, 0x02D9, 0x0307, 0x0336, 0x0367,
    0x039B, 0x03D1, 0x0406, 0x0442, 0x047E, 0x04C4, 0x0500, 0x0546,
    0x058C, 0x0622, 0x0672, 0x06CC, 0x071C, 0x0776, 0x07DA, 0x0834,
    0x0898, 0x0906, 0x096A, 0x09D8, 0x0A50, 0x0ABE, 0x0B40, 0x0BB8,
    0x0C3A, 0x0CBC, 0x0D48, 0x0DDE, 0x0E6A, 0x0F00, 0x0FA0, 0x1040,
    0x10EA, 0x1194, 0x123E, 0x12F2, 0x13B0, 0x146E, 0x1536, 0x15FE,
    0x16D0, 0x17A2, 0x187E, 0x195A, 0x1A40, 0x1B30, 0x1C20, 0x1D1A,
    0x1E1E, 0x1F22, 0x2030, 0x2148, 0x2260, 0x2382, 0x2710, 0x7FFF
]


VOLUME_ENVELOPE_TABLE_32BIT = [
    0x00000000, 0x00000004, 0x00000007, 0x0000000A,
    0x0000000F, 0x00000015, 0x0000001C, 0x00000024,
    0x0000002E, 0x0000003A, 0x00000048, 0x00000057,
    0x00000068, 0x0000007B, 0x00000091, 0x000000A8,
    0x00000185, 0x000001BE, 0x000001FC, 0x0000023F,
    0x00000288, 0x000002D6, 0x0000032A, 0x00000385,
    0x000003E5, 0x0000044C, 0x000004BA, 0x0000052E,
    0x000005A9, 0x0000062C, 0x000006B5, 0x00000746,
    0x00000BCF, 0x00000CC0, 0x00000DBD, 0x00000EC6,
    0x00000FDC, 0x000010FF, 0x0000122F, 0x0000136C,
    0x000014B6, 0x0000160F, 0x00001775, 0x000018EA,
    0x00001A6D, 0x00001BFF, 0x00001DA0, 0x00001F51,
    0x00002C16, 0x00002E80, 0x00003100, 0x00003395,
    0x00003641, 0x00003902, 0x00003BDB, 0x00003ECA,
    0x000041D0, 0x000044EE, 0x00004824, 0x00004B73,
    0x00004ED9, 0x00005259, 0x000055F2, 0x000059A4,
    0x000074CC, 0x000079AB, 0x00007EAC, 0x000083CE,
    0x00008911, 0x00008E77, 0x000093FF, 0x000099AA,
    0x00009F78, 0x0000A56A, 0x0000AB80, 0x0000B1BB,
    0x0000B81A, 0x0000BE9E, 0x0000C547, 0x0000CC17,
    0x0000FD42, 0x000105CB, 0x00010E82, 0x00011768,
    0x0001207E, 0x000129C4, 0x0001333B, 0x00013CE2,
    0x000146BB, 0x000150C5, 0x00015B02, 0x00016572,
    0x00017015, 0x00017AEB, 0x000185F5, 0x00019133,
    0x0001E16D, 0x0001EF07, 0x0001FCE0, 0x00020AF7,
    0x0002194F, 0x000227E6, 0x000236BE, 0x000245D7,
    0x00025532, 0x000264CF, 0x000274AE, 0x000284D0,
    0x00029536, 0x0002A5E0, 0x0002B6CE, 0x0002C802,
    0x000341B0, 0x000355F8, 0x00036A90, 0x00037F79,
    0x000394B4, 0x0003AA41, 0x0003C021, 0x0003D654,
    0x0003ECDA, 0x000403B5, 0x00041AE5, 0x0004326A,
    0x00044A45, 0x00046277, 0x00047B00, 0x7FFFFFFF
]


class EodChunk:
    magic: bytes = b"eod "
    version: int = 0x415
    chunk_beg: int = 0x10
    chunk_len: int = 0

    def read(self, rdr: BinaryReader):
        self.magic = rdr.read(4)
        if self.magic != b"eod ":
            raise ValueError("SWDEodChunk does not start with magic value")
        assert rdr.read_uint16() == 0
        self.version = rdr.read_uint16()
        if self.version != 0x415:
            raise ValueError("SWDEodChunk does not have correct version")
        self.chunk_beg = rdr.read_uint32()
        self.chunk_len = rdr.read_uint32()


class PcmdChunk:
    magic: bytes = b"pcmd"
    version: int = 0x415
    chunk_beg: int = 0x10
    chunk_len: int
    sample_data: np.ndarray

    def read(self, rdr: BinaryReader):
        self.magic = rdr.read(4)
        if self.magic != b"pcmd":
            raise ValueError("SWDPcmdChunk does not start with magic value")
        assert rdr.read_uint16() == 0
        self.version = rdr.read_uint16()
        if self.version != 0x415:
            raise ValueError("SWDPcmdChunk does not have correct version")
        self.chunk_beg = rdr.read_uint32()
        self.chunk_len = rdr.read_uint32()
        self.sample_data = np.frombuffer(rdr.read(self.chunk_len), dtype=np.uint8)


class SWDKeyGroup:
    id_: int
    polyphony: int
    priority: int
    voice_channel_low: int
    voice_channel_hi: int
    unk50: int
    unk51: int

    def read(self, rdr: BinaryReader):
        # key groups used for padding are all 0xAA
        self.id_ = rdr.read_uint16()
        self.polyphony = rdr.read_uint8()
        self.priority = rdr.read_uint8()
        self.voice_channel_low = rdr.read_uint8()
        self.voice_channel_hi = rdr.read_uint8()
        self.unk50 = rdr.read_uint8()  # 0xAA if key_group_id == 0xAAAA else 0
        self.unk51 = rdr.read_uint8()  # 0xAA if key_group_id == 0xAAAA else 0
        if conf.DEBUG_AUDIO:
            logging.debug(f"    KeyGroup: {self.id_}")
            logging.debug(f"        UNK50: {self.unk50}")
            logging.debug(f"        UNK51: {self.unk51}")

    def to_key_group(self) -> KeyGroup:
        key_group = KeyGroup()
        key_group.id_ = self.id_
        key_group.polyphony = self.polyphony
        key_group.priority = self.priority
        key_group.voice_channel_low = self.voice_channel_low
        key_group.voice_channel_high = self.voice_channel_hi
        return key_group


class KgrpChunk:
    magic: bytes = b"kgrp"
    version: int = 0x415
    chunk_beg: int = 0x10
    chunk_len: int
    key_groups: List[SWDKeyGroup]

    def read(self, rdr: BinaryReader):
        if conf.DEBUG_AUDIO:
            logging.debug("KGPRChunk")
        self.magic = rdr.read(4)
        if self.magic != b"kgrp":
            raise ValueError("SWDKgprChunk does not start with magic value")
        assert rdr.read_uint16() == 0
        self.version = rdr.read_uint16()
        if self.version != 0x415:
            raise ValueError("SWDKgprChunk does not have correct version")
        self.chunk_beg = rdr.read_uint32()
        self.chunk_len = rdr.read_uint32()
        pos = rdr.c
        self.key_groups = []
        while rdr.c < pos + self.chunk_len:
            key_group = SWDKeyGroup()
            key_group.read(rdr)
            self.key_groups.append(key_group)


class SWDLFOEntry:
    unk1: int
    # Destination of the lfo output
    # 0 - none/disabled
    # 1 - pitch
    # 2 - volume
    # 3 - pan
    # 4 - low pass / cut off filter
    destination: int
    # Shape of the waveform
    # 1 - square
    # 2 - triangle?
    # 3 - sinus?
    # 4 - ?
    # 5 - Saw?
    # 6 - Noise?
    # 7 - Random
    wshape: int
    rate: int  # maybe hz
    unk29: int  # feedback or resonance? (or maybe just don't touch it)
    depth: int
    delay: int  # milliseconds

    def read(self, rdr: BinaryReader):
        assert rdr.read_uint8() == 0
        self.unk1 = rdr.read_uint8()  # bool? GE_003.SWD/SI_012.SWD is 1 (mostly 0)
        self.destination = rdr.read_uint8()
        self.wshape = rdr.read_uint8()
        self.rate = rdr.read_uint16()
        self.unk29 = rdr.read_uint16()
        if conf.DEBUG_AUDIO:
            logging.debug("        LFOEntry")
            logging.debug(f"            UNK29: {self.unk29}")
        self.depth = rdr.read_uint16()
        self.delay = rdr.read_uint16()
        assert rdr.read_uint16() == 0
        assert rdr.read_uint16() == 0

    def to_lfo(self) -> LFO:
        lfo = LFO()
        lfo.destination = self.destination
        lfo.wshape = self.wshape
        lfo.rate = self.rate
        lfo.depth = self.depth
        lfo.delay = self.delay
        return lfo


class SWDSplitEntry:
    splits_table_id: int
    unk25: int  # possibly bool
    low_key: int = 0
    hi_key: int = 0x7F
    low_vel: int
    hi_vel: int
    unk16: int = 0  # pad_byte?
    unk17: int = 0  # pad_byte?
    sample_id: int  # sample_info in the wavi chunk
    fine_tune: int  # in cents
    coarse_tune: int = -7
    root_key: int
    sample_volume: int
    sample_pan: int
    key_group_id: int
    unk22: int = 0x02
    unk24: int = 0  # pad_byte?
    envelope_on: int  # if is 0, envelope isn't processed
    envelope_multiplier: int
    attack_volume: int
    attack: int
    decay: int
    sustain: int
    hold: int
    decay2: int
    release: int

    def read(self, rdr: BinaryReader):
        assert rdr.read_uint8() == 0
        self.splits_table_id = rdr.read_uint8()
        assert rdr.read_uint8() == 2
        self.unk25 = rdr.read_uint8()  # 1 or 0 (bool)
        self.low_key = rdr.read_int8()
        self.hi_key = rdr.read_int8()
        _low_key2 = rdr.read_int8()  # copy
        _hi_key2 = rdr.read_int8()  # copy
        self.low_vel = rdr.read_int8()
        self.hi_vel = rdr.read_int8()
        _low_vel2 = rdr.read_int8()  # copy
        _hi_vel2 = rdr.read_int8()  # copy
        self.unk16 = rdr.read_uint32()  # 0xAAAAAAAA or 0
        self.unk17 = rdr.read_uint16()  # 0xAAAA or 0
        self.sample_id = rdr.read_uint16()
        self.fine_tune = rdr.read_int8()
        self.coarse_tune = rdr.read_int8()
        self.root_key = rdr.read_int8()
        _key_transpose = rdr.read_int8()  # difference between root key and 60
        self.sample_volume = rdr.read_int8()
        self.sample_pan = rdr.read_int8()
        self.key_group_id = rdr.read_uint8()
        self.unk22 = rdr.read_uint8()  # 0 or 2
        assert rdr.read_uint16() == 0
        self.unk24 = rdr.read_uint16()  # pad byte? 0xAAAA or 0xFFFF
        self.envelope_on = rdr.read_uint8()
        self.envelope_multiplier = rdr.read_uint8()
        assert rdr.read_uint8() == 1
        assert rdr.read_uint8() == 3
        assert rdr.read_uint16() == 0xFF03
        assert rdr.read_uint16() == 0xFFFF
        self.attack_volume = rdr.read_int8()
        self.attack = rdr.read_int8()
        self.decay = rdr.read_int8()
        self.sustain = rdr.read_int8()
        self.hold = rdr.read_int8()
        self.decay2 = rdr.read_int8()
        self.release = rdr.read_int8()
        assert rdr.read_uint8() == 0xFF
        if conf.DEBUG_AUDIO:
            logging.debug(f"        Split Entry {self.splits_table_id}")
            logging.debug(f"            UNK25: {self.unk25}")
            logging.debug(f"            UNK16: {self.unk16}")
            logging.debug(f"            UNK17: {self.unk17}")
            logging.debug(f"            KEY_GROUP_ID: {self.key_group_id}")
            logging.debug(f"            UNK22: {self.unk22}")
            logging.debug(f"            UNK22: {self.unk24}")

    def to_split(self, samples: Dict[int, Sample],
                 key_groups: Dict[int, KeyGroup]) -> Split:
        split = Split()
        split.low_key = self.low_key
        split.high_key = self.hi_key
        split.low_vel = self.low_vel
        split.high_vel = self.hi_vel
        split.sample = samples[self.sample_id]
        split.fine_tune = self.fine_tune
        split.coarse_tune = self.coarse_tune
        split.root_key = self.root_key
        split.volume = self.sample_volume
        split.pan = self.sample_pan
        split.key_group = key_groups[self.key_group_id]
        split.envelope_on = self.envelope_on > 0
        table_to_use = VOLUME_ENVELOPE_TABLE_32BIT if self.envelope_multiplier == 0 else VOLUME_ENVELOPE_TABLE_16BIT
        split.attack_volume = self.attack_volume
        split.attack = table_to_use[self.attack]
        split.decay = table_to_use[self.decay]
        split.sustain = self.sustain
        split.hold = table_to_use[self.hold]
        split.decay2 = table_to_use[self.decay2]
        split.release = table_to_use[self.release]
        return split

    def from_split(self, split: Split):
        self.low_key = split.low_key
        self.hi_key = split.high_key
        self.low_vel = split.low_vel
        self.hi_vel = split.high_vel
        self.sample_id = split.sample.id_
        self.fine_tune = split.fine_tune
        self.coarse_tune = split.coarse_tune
        self.root_key = split.root_key
        self.sample_volume = split.volume
        self.sample_pan = split.pan
        self.key_group_id = split.key_group.id_
        self.envelope_on = split.envelope_on

        self.attack_volume = split.attack_volume
        self.sustain = split.sustain

        def get_closest_table_env(table_: List[int], value: int):
            min_diff = -1
            min_element_i = 0
            for i, element in enumerate(table_):
                diff = value - element
                if abs(diff) < min_diff or min_diff == -1:
                    min_diff = diff
                    min_element_i = i
                if diff < 0:  # if the different is negative, the next diffs can only be greater as the table is sorted
                    break
            return min_diff, min_element_i
        min_avg_diff = -1
        for env_mult, table in enumerate([VOLUME_ENVELOPE_TABLE_32BIT, VOLUME_ENVELOPE_TABLE_16BIT]):
            attack_diff, attack_value = get_closest_table_env(table, split.attack)
            decay_diff, decay_value = get_closest_table_env(table, split.decay)
            hold_diff, hold_value = get_closest_table_env(table, split.hold)
            decay2_diff, decay2_value = get_closest_table_env(table, split.decay2)
            release_diff, release_value = get_closest_table_env(table, split.release)
            avg_diff = sum([attack_diff, decay_diff, hold_diff, decay2_diff, release_diff]) / 5
            if avg_diff < min_avg_diff or min_avg_diff == -1:
                self.attack = attack_value
                self.decay = decay_value
                self.hold = hold_value
                self.decay2 = decay2_value
                self.release = release_value
                self.envelope_multiplier = env_mult
                min_avg_diff = avg_diff


class ProgramInfoEntry:
    id_: int
    splits_count: int
    program_volume: int
    program_pan: int
    lfo_count: int
    pad_byte: int  # 0xAA or 0x00
    lfo_table: List[SWDLFOEntry]
    splits_table: List[SWDSplitEntry]

    def read(self, rdr: BinaryReader):
        self.id_ = rdr.read_uint16()
        self.splits_count = rdr.read_uint16()
        self.program_volume = rdr.read_int8()
        self.program_pan = rdr.read_int8()
        assert rdr.read_uint8() == 0
        assert rdr.read_uint8() == 0xF
        assert rdr.read_uint16() == 0x200
        assert rdr.read_uint8() == 0
        self.lfo_count = rdr.read_uint8()
        self.pad_byte = rdr.read_uint8()
        assert rdr.read_uint8() == 0
        assert rdr.read_uint8() == 0
        assert rdr.read_uint8() == 0
        self.lfo_table = []
        for _ in range(self.lfo_count):
            lfo_entry = SWDLFOEntry()
            lfo_entry.read(rdr)
            self.lfo_table.append(lfo_entry)
        rdr.read(16)  # Uses pad byte padding value
        self.splits_table = []
        for _ in range(self.splits_count):
            split_entry = SWDSplitEntry()
            split_entry.read(rdr)
            self.splits_table.append(split_entry)
        if conf.DEBUG_AUDIO:
            logging.debug(f"    Program {self.id_}")
            logging.debug(f"        Pad Byte {self.pad_byte}")

    def to_program(self, samples: Dict[int, Sample],
                   key_groups: Dict[int, KeyGroup]) -> Program:
        program = Program()
        program.id_ = self.id_
        program.volume = self.program_volume
        program.pan = self.program_pan
        program.lfos = [lfo.to_lfo() for lfo in self.lfo_table]
        program.splits = [split.to_split(samples, key_groups) for split in self.splits_table]
        return program


class PrgiChunk:
    magic: bytes = b"prgi"
    version: int = 0x415
    chunk_beg: int = 0x10
    chunk_len: int
    program_ptr_table: List[int]
    program_info_table: List[ProgramInfoEntry]

    def read(self, rdr: BinaryReader, prgi_slot_count: int):
        if conf.DEBUG_AUDIO:
            logging.debug("PRGIChunk")
        self.magic = rdr.read(4)
        if self.magic != b"prgi":
            raise ValueError("SWDPrgiChunk does not start with magic value")
        assert rdr.read_uint16() == 0
        self.version = rdr.read_uint16()
        if self.version != 0x415:
            raise ValueError("SWDPrgiChunk does not have correct version")
        self.chunk_beg = rdr.read_uint32()
        self.chunk_len = rdr.read_uint32()
        pos = rdr.c
        self.program_ptr_table = []
        for _ in range(prgi_slot_count):
            self.program_ptr_table.append(rdr.read_uint16())
        rdr.align(16)
        self.program_info_table = []
        while rdr.c != pos + self.chunk_len:
            sample_info_entry = ProgramInfoEntry()
            sample_info_entry.read(rdr)
            self.program_info_table.append(sample_info_entry)


class SampleInfoEntry:
    id_: int
    fine_tune: int
    coarse_tune: int
    root_key: int
    key_transpose: int
    volume: int
    pan: int
    version: int = 0x415
    sample_format: int
    # 0 - 8 bits pcm?
    # 0x100 - 16 bits pcm
    # 0x200 - 4 bits adpcm
    # 0x300 - psg?
    loop_enabled: bool
    sample_rate: int
    sample_pos: int
    loop_beginning: int
    loop_length: int
    envelope: int
    envelope_multiplier: int
    attack_volume: int
    attack: int
    decay: int
    sustain: int
    hold: int
    decay2: int
    release: int

    def read(self, rdr: BinaryReader):
        assert rdr.read_uint16() == 0xAA01
        self.id_ = rdr.read_uint16()
        self.fine_tune = rdr.read_int8()
        self.coarse_tune = rdr.read_int8()
        self.root_key = rdr.read_int8()
        self.key_transpose = rdr.read_int8()  # difference between root key and 60
        self.volume = rdr.read_int8()
        self.pan = rdr.read_int8()
        assert rdr.read_uint8() == 0
        assert rdr.read_uint8() == 0x02
        assert rdr.read_uint16() == 0
        assert rdr.read_uint16() == 0xAAAA
        self.version = rdr.read_uint16()
        if self.version != 0x415:
            raise ValueError("SampleInfoEntry does not have correct version")
        self.sample_format = rdr.read_uint16()
        assert rdr.read_uint8() == 0x09
        self.loop_enabled = rdr.read_bool()
        assert rdr.read_uint16() == 0x801
        assert rdr.read_uint16() == 0x400
        assert rdr.read_uint16() == 0x101
        assert rdr.read_uint32() == 1
        self.sample_rate = rdr.read_uint32()
        self.sample_pos = rdr.read_uint32()
        self.loop_beginning = rdr.read_uint32()
        self.loop_length = rdr.read_uint32()
        self.envelope = rdr.read_uint8()
        self.envelope_multiplier = rdr.read_uint8()
        assert rdr.read_uint8() == 0x1
        assert rdr.read_uint8() == 0x3
        assert rdr.read_uint16() == 0xFF03
        assert rdr.read_uint16() == 0xFFFF
        self.attack_volume = rdr.read_int8()
        self.attack = rdr.read_int8()
        self.decay = rdr.read_int8()
        self.sustain = rdr.read_int8()
        self.hold = rdr.read_int8()
        self.decay2 = rdr.read_int8()
        self.release = rdr.read_int8()
        assert rdr.read_uint8() == 0xFF

    def to_sample(self, pcmd_chunk: PcmdChunk) -> Sample:
        sample = Sample()
        sample.id_ = self.id_
        sample.fine_tune = self.fine_tune
        sample.coarse_tune = self.coarse_tune
        sample.root_key = self.root_key
        sample.volume = self.volume
        sample.pan = self.pan
        sample.loop_enabled = self.loop_enabled
        sample.sample_rate = self.sample_rate
        sample.loop_beginning = self.loop_beginning * 4
        # convert from bytes to samples
        if self.sample_format == 0x100:
            sample.loop_beginning /= 2
        elif self.sample_format == 0x200:
            sample.loop_beginning *= 2
        sample.loop_length = self.loop_length * 4
        # convert from bytes to samples
        if self.sample_format == 0x100:
            sample.loop_length /= 2
        elif self.sample_format == 0x200:
            sample.loop_length *= 2
        sample.envelope_on = self.envelope > 0
        table_to_use = VOLUME_ENVELOPE_TABLE_32BIT if self.envelope_multiplier == 0 else VOLUME_ENVELOPE_TABLE_16BIT
        sample.attack_volume = self.attack_volume
        sample.attack = table_to_use[self.attack]
        sample.decay = table_to_use[self.decay]
        sample.sustain = self.sustain
        sample.hold = table_to_use[self.hold]
        sample.decay2 = table_to_use[self.decay2]
        sample.release = table_to_use[self.release]

        if pcmd_chunk is None:
            sample.pcm16 = None
            return sample

        sample_length = (self.loop_beginning + self.loop_length) * 4
        sample_data = pcmd_chunk.sample_data[self.sample_pos:self.sample_pos + sample_length]
        if self.sample_format == 0x100:  # is already 16 bit pcm
            dt = np.dtype(np.int16).newbyteorder("<")
            sample_data: np.ndarray = sample_data.view(dtype=dt)
            sample.pcm16 = sample_data
        elif self.sample_format == 0x200:
            sample.adpcm = sample_data
        else:
            raise NotImplementedError(f"Sample format {self.sample_format} not implemented")
        return sample


class WaviChunk:
    magic: bytes = b"wavi"
    version: int = 0x415
    chunk_beg: int = 0x10
    chunk_len: int
    wav_table: List[int]
    sample_info_table: List[SampleInfoEntry]

    def read(self, rdr: BinaryReader, wavi_slot_count: int):
        if conf.DEBUG_AUDIO:
            logging.debug("WAVIChunk")
        self.magic = rdr.read(4)
        if self.magic != b"wavi":
            raise ValueError("SWDWaviChunk does not start with magic value")
        assert rdr.read_uint16() == 0
        self.version = rdr.read_uint16()
        if self.version != 0x415:
            raise ValueError("SWDWaviChunk does not have correct version")
        self.chunk_beg = rdr.read_uint32()
        self.chunk_len = rdr.read_uint32()
        pos = rdr.c
        self.wav_table = []
        for _ in range(wavi_slot_count):
            self.wav_table.append(rdr.read_uint16())
        rdr.align(16)
        self.sample_info_table = []
        while rdr.c != pos + self.chunk_len:
            sample_info_entry = SampleInfoEntry()
            sample_info_entry.read(rdr)
            self.sample_info_table.append(sample_info_entry)


class SWDHeader:
    magic: bytes = b"swdl"
    file_length: int
    version: int = 0x415
    is_sample_bank: bool
    group: int
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    centisecond: int
    file_name: bytes
    pcmdlen: int
    wavi_slot_count: int
    prgi_slot_count: int
    unk17: int
    wavi_len: int  # len of wavi chunk

    def read(self, rdr: BinaryReader):
        if conf.DEBUG_AUDIO:
            logging.debug("SWDHeader")
        self.magic = rdr.read(4)
        if self.magic != b"swdl":
            raise ValueError("SWDHeader does not start with magic value")
        rdr.read_uint32()  # 0
        self.file_length = rdr.read_uint32()
        self.version = rdr.read_uint16()
        if self.version != 0x415:
            raise ValueError("SMDHeader does not have correct version")
        self.is_sample_bank = rdr.read_bool()
        self.group = rdr.read_uint8()
        # 8 bytes of 0
        rdr.read_uint32()
        rdr.read_uint32()
        self.year = rdr.read_uint16()
        self.month = rdr.read_uint8()
        self.day = rdr.read_uint8()
        self.hour = rdr.read_uint8()
        self.minute = rdr.read_uint8()
        self.second = rdr.read_uint8()
        self.centisecond = rdr.read_uint8()
        self.file_name = rdr.read_string(16, encoding=None, pad=b"\xAA")
        assert rdr.read_uint32() == 0xAAAAAA00
        # 8 bytes of 0
        assert rdr.read_uint32() == 0
        assert rdr.read_uint32() == 0
        assert rdr.read_uint32() == 0x10
        self.pcmdlen = rdr.read_uint32()
        assert rdr.read_uint16() == 0
        self.wavi_slot_count = rdr.read_uint16()
        self.prgi_slot_count = rdr.read_uint16()
        self.unk17 = rdr.read_uint16()
        if conf.DEBUG_AUDIO:
            logging.debug(f"    UNK17: {self.unk17}")
        self.wavi_len = rdr.read_uint32()


# TODO: Write and figure out unknowns
class SWDL(FileFormat):
    samples: Dict[int, Sample]
    key_groups: Dict[int, KeyGroup]
    programs: Dict[int, Program]

    def __init__(self, filename: str = None, file=None, compressed=None, rom: NintendoDSRom = None, **kwargs):
        self.samples = {}
        self.key_groups = {}
        self.programs = {}
        super(SWDL, self).__init__(filename=filename, file=file, compressed=compressed, rom=rom, **kwargs)

    def read_stream(self, stream):
        swd_header = SWDHeader()
        wavi_chunk: Optional[WaviChunk] = None
        prgi_chunk: Optional[PrgiChunk] = None
        pcmd_chunk: Optional[PcmdChunk] = None
        kgrp_chunk: Optional[KgrpChunk] = None
        eod_chunk = EodChunk()
        if isinstance(stream, BinaryReader):
            rdr = stream
        else:
            rdr = BinaryReader(stream)
        while True:
            rdr.align(0x10)
            pos = rdr.c
            chunk_name = rdr.read(4)
            rdr.seek(pos)
            if chunk_name == b"swdl":
                swd_header.read(rdr)
            elif chunk_name == b"wavi":
                wavi_chunk = WaviChunk()
                wavi_chunk.read(rdr, swd_header.wavi_slot_count)
            elif chunk_name == b"prgi":
                prgi_chunk = PrgiChunk()
                prgi_chunk.read(rdr, swd_header.prgi_slot_count)
            elif chunk_name == b"kgrp":
                kgrp_chunk = KgrpChunk()
                kgrp_chunk.read(rdr)
            elif chunk_name == b"pcmd":
                pcmd_chunk = PcmdChunk()
                pcmd_chunk.read(rdr)
            elif chunk_name == b"eod ":
                eod_chunk.read(rdr)
                break

        self.samples = {}
        self.key_groups = {}
        self.programs = {}
        # Construct data structures
        if wavi_chunk is not None:
            for sample_info_entry in wavi_chunk.sample_info_table:
                sample = sample_info_entry.to_sample(pcmd_chunk)
                self.samples[sample_info_entry.id_] = sample
        if kgrp_chunk is not None:
            for swd_key_group in kgrp_chunk.key_groups:
                key_group = swd_key_group.to_key_group()
                self.key_groups[swd_key_group.id_] = key_group
        if prgi_chunk is not None:
            for swd_program in prgi_chunk.program_info_table:
                program = swd_program.to_program(self.samples, self.key_groups)
                self.programs[swd_program.id_] = program

    def write_stream(self, stream):
        raise NotImplementedError('saving swd still not implemented')
