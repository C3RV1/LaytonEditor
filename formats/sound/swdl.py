# Thanks to https://projectpokemon.org/docs/mystery-dungeon-nds/dse-swdl-format-r14/
from typing import List, Dict, Optional

import numpy as np

from formats.binary import BinaryReader
from formats.filesystem import FileFormat, NintendoDSRom
from formats.sound.compression.adpcm import Adpcm
from formats.sound.sound_types import Sample, KeyGroup, Split, LFO, Program


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
        print(f"    KeyGroup: {self.id_}")
        self.polyphony = rdr.read_uint8()
        self.priority = rdr.read_uint8()
        self.voice_channel_low = rdr.read_uint8()
        self.voice_channel_hi = rdr.read_uint8()
        self.unk50 = rdr.read_uint8()  # 0xAA if key_group_id == 0xAAAA else 0
        self.unk51 = rdr.read_uint8()  # 0xAA if key_group_id == 0xAAAA else 0
        print(f"        UNK50: {self.unk50}")
        print(f"        UNK51: {self.unk51}")

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
        print("KGPRChunk")
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
        print("        LFOEntry")
        assert rdr.read_uint8() == 0
        self.unk1 = rdr.read_uint8()  # bool? GE_003.SWD/SI_012.SWD is 1 (mostly 0)
        self.destination = rdr.read_uint8()
        self.wshape = rdr.read_uint8()
        self.rate = rdr.read_uint16()
        self.unk29 = rdr.read_uint16()
        print(f"            UNK29: {self.unk29}")
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
    low_key2: int  # a copy of low_key?
    hi_key2: int  # a copy of hi_key?
    low_vel: int
    hi_vel: int
    low_vel2: int  # a copy of low_vel?
    hi_vel2: int  # a copy of hi_vel?
    unk16: int  # pad_byte?
    unk17: int  # pad_byte?
    sample_id: int  # sample_info in the wavi chunk
    fine_tune: int  # in cents
    coarse_tune: int = -7
    root_key: int
    key_transpose: int  # diff between root key and 60?
    sample_volume: int
    sample_pan: int
    key_group_id: int
    unk22: int = 0x02
    unk24: int  # pad_byte?
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
        print(f"        Split Entry {self.splits_table_id}")
        assert rdr.read_uint8() == 2
        self.unk25 = rdr.read_uint8()  # 1 or 0 (bool)
        print(f"            UNK25: {self.unk25}")
        self.low_key = rdr.read_int8()
        self.hi_key = rdr.read_int8()
        self.low_key2 = rdr.read_int8()
        self.hi_key2 = rdr.read_int8()
        self.low_vel = rdr.read_int8()
        self.hi_vel = rdr.read_int8()
        self.low_vel2 = rdr.read_int8()
        self.hi_vel2 = rdr.read_int8()
        self.unk16 = rdr.read_uint32()  # 0xAAAAAAAA or 0
        self.unk17 = rdr.read_uint16()  # 0xAAAA or 0
        print(f"            UNK16: {self.unk16}")
        print(f"            UNK17: {self.unk17}")
        self.sample_id = rdr.read_uint16()
        self.fine_tune = rdr.read_int8()
        self.coarse_tune = rdr.read_int8()
        self.root_key = rdr.read_int8()
        self.key_transpose = rdr.read_int8()  # difference between root key and 60
        self.sample_volume = rdr.read_int8()
        self.sample_pan = rdr.read_int8()
        self.key_group_id = rdr.read_uint8()
        self.unk22 = rdr.read_uint8()  # 0 or 2
        assert rdr.read_uint16() == 0
        self.unk24 = rdr.read_uint16()  # pad byte? 0xAAAA or 0xFFFF
        print(f"            KEY_GROUP_ID: {self.key_group_id}")
        print(f"            UNK22: {self.unk22}")
        print(f"            UNK22: {self.unk24}")
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
        split.envelope_multiplier = self.envelope_multiplier
        split.attack_volume = self.attack_volume
        split.attack = self.attack
        split.decay = self.decay
        split.sustain = self.sustain
        split.hold = self.hold
        split.decay2 = self.decay2
        split.release = self.release
        return split


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
        print(f"    Program {self.id_}")
        self.splits_count = rdr.read_uint16()
        self.program_volume = rdr.read_int8()
        self.program_pan = rdr.read_int8()
        assert rdr.read_uint8() == 0
        assert rdr.read_uint8() == 0xF
        assert rdr.read_uint16() == 0x200
        assert rdr.read_uint8() == 0
        self.lfo_count = rdr.read_uint8()
        self.pad_byte = rdr.read_uint8()
        print(f"        Pad Byte {self.pad_byte}")
        assert rdr.read_uint8() == 0
        assert rdr.read_uint8() == 0
        assert rdr.read_uint8() == 0
        self.lfo_table = []
        for _ in range(self.lfo_count):
            lfo_entry = SWDLFOEntry()
            lfo_entry.read(rdr)
            self.lfo_table.append(lfo_entry)
        rdr.read(16)
        self.splits_table = []
        for _ in range(self.splits_count):
            split_entry = SWDSplitEntry()
            split_entry.read(rdr)
            self.splits_table.append(split_entry)

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
        print("PRGIChunk")
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
        sample.loop_beginning = self.loop_beginning
        sample.loop_length = self.loop_length
        sample.envelope_on = self.envelope > 0
        sample.envelope_multiplier = self.envelope_multiplier
        sample.attack_volume = self.attack_volume
        sample.attack = self.attack
        sample.decay = self.decay
        sample.sustain = self.sustain
        sample.hold = self.hold
        sample.decay2 = self.decay2
        sample.release = self.release

        if pcmd_chunk is None:
            sample.pcm16 = None
            return sample

        sample_length = (self.loop_beginning + self.loop_length) * 4
        sample_data = pcmd_chunk.sample_data[self.sample_pos:self.sample_pos + sample_length]
        if self.sample_format == 0x100:  # is already 16 bit pcm
            dt = np.dtype(np.int16).newbyteorder("<")
            sample_data: np.ndarray = sample_data.view(dtype=dt)
        elif self.sample_format == 0x200:
            sample_data = Adpcm().decompress(sample_data)
        else:
            raise NotImplementedError(f"Sample format {self.sample_format} not implemented")
        sample.pcm16 = sample_data.reshape((sample_data.shape[0], 1))
        return sample


class WaviChunk:
    magic: bytes = b"wavi"
    version: int = 0x415
    chunk_beg: int = 0x10
    chunk_len: int
    wav_table: List[int]
    sample_info_table: List[SampleInfoEntry]

    def read(self, rdr: BinaryReader, wavi_slot_count: int):
        print("WAVIChunk")
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
        print("SWDHeader")
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
        print(f"    UNK17: {self.unk17}")
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
