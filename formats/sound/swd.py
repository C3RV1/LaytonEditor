# Thanks to https://projectpokemon.org/docs/mystery-dungeon-nds/dse-swdl-format-r14/
from typing import List, Optional

import numpy as np

from formats.binary import BinaryReader
from formats.filesystem import FileFormat
from formats.sound.sadl_compression.ima_adpcm import ImaAdpcm


class EodChunk:
    magic: bytes = b"eod "
    unk1: int = 0
    version: int = 0x415
    chunk_beg: int = 0x10
    chunk_len: int = 0

    def read(self, rdr: BinaryReader):
        self.magic = rdr.read(4)
        if self.magic != b"eod ":
            raise ValueError("SWDEodChunk does not start with magic value")
        self.unk1 = rdr.read_uint16()
        self.version = rdr.read_uint16()
        if self.version != 0x415:
            raise ValueError("SWDEodChunk does not have correct version")
        self.chunk_beg = rdr.read_uint32()
        self.chunk_len = rdr.read_uint32()


class PcmdChunk:
    magic: bytes = b"pcmd"
    unk1: int = 0x0
    version: int = 0x415
    chunk_beg: int = 0x10
    chunk_len: int
    sample_data: np.ndarray

    def read(self, rdr: BinaryReader):
        self.magic = rdr.read(4)
        if self.magic != b"pcmd":
            raise ValueError("SWDPcmdChunk does not start with magic value")
        self.unk1 = rdr.read_uint16()
        self.version = rdr.read_uint16()
        if self.version != 0x415:
            raise ValueError("SWDPcmdChunk does not have correct version")
        self.chunk_beg = rdr.read_uint32()
        self.chunk_len = rdr.read_uint32()
        self.sample_data = np.frombuffer(rdr.read(self.chunk_len), dtype=np.uint8)


class KeyGroup:
    key_group_id: int
    polyphony: int
    priority: int
    voice_channel_low: int
    voice_channel_hi: int
    unk50: int
    unk51: int

    def read(self, rdr: BinaryReader):
        self.key_group_id = rdr.read_uint16()
        self.polyphony = rdr.read_uint8()
        self.priority = rdr.read_uint8()
        self.voice_channel_low = rdr.read_uint8()
        self.voice_channel_hi = rdr.read_uint8()
        self.unk50 = rdr.read_uint8()
        self.unk51 = rdr.read_uint8()


class KgrpChunk:
    magic: bytes = b"kgrp"
    unk1: int
    version: int = 0x415
    chunk_beg: int = 0x10
    chunk_len: int
    key_groups: List[KeyGroup]

    def read(self, rdr: BinaryReader):
        self.magic = rdr.read(4)
        if self.magic != b"kgrp":
            raise ValueError("SWDKgprChunk does not start with magic value")
        self.unk1 = rdr.read_uint16()
        self.version = rdr.read_uint16()
        if self.version != 0x415:
            raise ValueError("SWDKgprChunk does not have correct version")
        self.chunk_beg = rdr.read_uint32()
        self.chunk_len = rdr.read_uint32()
        pos = rdr.c
        self.key_groups = []
        while rdr.c < pos + self.chunk_len:
            key_group = KeyGroup()
            key_group.read(rdr)
            self.key_groups.append(key_group)


class LFOEntry:
    unk34: int = 0x0
    unk52: int = 0x0
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
    unk32: int = 0x0  # possible fadeout
    unk33: int = 0x0

    def read(self, rdr: BinaryReader):
        self.unk34 = rdr.read_uint8()
        self.unk52 = rdr.read_uint8()
        self.destination = rdr.read_uint8()
        self.wshape = rdr.read_uint8()
        self.rate = rdr.read_uint16()
        self.unk29 = rdr.read_uint16()
        self.depth = rdr.read_uint16()
        self.delay = rdr.read_uint16()
        self.unk32 = rdr.read_uint16()
        self.unk33 = rdr.read_uint16()


class SplitEntry:
    unk10: int = 0
    splits_table_id: int
    unk11: int
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
    unk17: int  # pad_byte?
    sample_info: 'SampleInfoEntry'  # id/index in the wavi chunk
    fine_tune: int  # in cents
    coarse_tune: int = -7
    root_key: int
    key_transpose: int  # diff between root key and 60?
    sample_volume: int
    sample_pan: int
    key_group_id: int
    unk22: int = 0x02
    unk23: int = 0x0
    unk24: int  # pad_byte?
    envelope_on: int  # if is 0, envelope isn't processed
    envelope_multiplier: int
    unk37: int
    unk38: int
    unk39: int
    unk40: int
    attack_volume: int
    attack: int
    decay: int
    sustain: int
    hold: int
    decay2: int
    release: int
    unk53: int

    def read(self, rdr: BinaryReader, swdl: 'SWDL'):
        self.unk10 = rdr.read_uint8()
        self.splits_table_id = rdr.read_uint8()
        self.unk11 = rdr.read_uint8()
        self.unk25 = rdr.read_uint8()
        self.low_key = rdr.read_int8()
        self.hi_key = rdr.read_int8()
        self.low_key2 = rdr.read_int8()
        self.hi_key2 = rdr.read_int8()
        self.low_vel = rdr.read_int8()
        self.hi_vel = rdr.read_int8()
        self.low_vel2 = rdr.read_int8()
        self.hi_vel2 = rdr.read_int8()
        self.unk16 = rdr.read_uint32()
        self.unk17 = rdr.read_uint16()
        self.sample_info = swdl.get_sample_info(rdr.read_uint16())
        self.fine_tune = rdr.read_int8()
        self.coarse_tune = rdr.read_int8()
        self.root_key = rdr.read_int8()
        self.key_transpose = rdr.read_int8()
        self.sample_volume = rdr.read_int8()
        self.sample_pan = rdr.read_int8()
        self.key_group_id = rdr.read_uint8()
        self.unk22 = rdr.read_uint8()
        self.unk23 = rdr.read_uint16()
        self.unk24 = rdr.read_uint16()
        self.envelope_on = rdr.read_uint8()
        self.envelope_multiplier = rdr.read_uint8()
        self.unk37 = rdr.read_uint8()
        self.unk38 = rdr.read_uint8()
        self.unk39 = rdr.read_uint16()
        self.unk40 = rdr.read_uint16()
        self.attack_volume = rdr.read_int8()
        self.attack = rdr.read_int8()
        self.decay = rdr.read_int8()
        self.sustain = rdr.read_int8()
        self.hold = rdr.read_int8()
        self.decay2 = rdr.read_int8()
        self.release = rdr.read_int8()
        self.unk53 = rdr.read_int8()


class ProgramInfoEntry:
    program_id: int
    splits_count: int
    program_volume: int
    program_pan: int
    unk3: int = 0
    that_f_byte: int = 0x0F  # Naming at project pokemon
    unk4: int = 0x200
    unk5: int = 0x00
    lfo_count: int
    pad_byte: int  # 0xAA or 0x00
    unk7: int = 0x0
    unk8: int = 0x0
    unk9: int = 0x0
    lfo_table: List[LFOEntry]
    splits_table: List[SplitEntry]

    def read(self, rdr: BinaryReader, swdl: 'SWDL'):
        self.program_id = rdr.read_uint16()
        self.splits_count = rdr.read_uint16()
        self.program_volume = rdr.read_int8()
        self.program_pan = rdr.read_int8()
        self.unk3 = rdr.read_uint8()
        self.that_f_byte = rdr.read_uint8()
        self.unk4 = rdr.read_uint16()
        self.unk5 = rdr.read_uint8()
        self.lfo_count = rdr.read_uint8()
        self.pad_byte = rdr.read_uint8()
        self.unk7 = rdr.read_uint8()
        self.unk8 = rdr.read_uint8()
        self.unk9 = rdr.read_uint8()
        self.lfo_table = []
        for _ in range(self.lfo_count):
            lfo_entry = LFOEntry()
            lfo_entry.read(rdr)
            self.lfo_table.append(lfo_entry)
        rdr.read(16)
        self.splits_table = []
        for _ in range(self.splits_count):
            split_entry = SplitEntry()
            split_entry.read(rdr, swdl)
            self.splits_table.append(split_entry)


class PrgiChunk:
    magic: bytes = b"prgi"
    unk1: int = 0
    version: int = 0x415
    chunk_beg: int = 0x10
    chunk_len: int
    program_ptr_table: List[int]
    program_info_table: List[ProgramInfoEntry]

    def read(self, rdr: BinaryReader, swdl: 'SWDL'):
        self.magic = rdr.read(4)
        if self.magic != b"prgi":
            raise ValueError("SWDPrgiChunk does not start with magic value")
        self.unk1 = rdr.read_uint16()
        self.version = rdr.read_uint16()
        if self.version != 0x415:
            raise ValueError("SWDPrgiChunk does not have correct version")
        self.chunk_beg = rdr.read_uint32()
        self.chunk_len = rdr.read_uint32()
        pos = rdr.c
        self.program_ptr_table = []
        for _ in range(swdl.swd_header.prgi_slot_count):
            self.program_ptr_table.append(rdr.read_uint16())
        rdr.align(16)
        self.program_info_table = []
        while rdr.c != pos + self.chunk_len:
            sample_info_entry = ProgramInfoEntry()
            sample_info_entry.read(rdr, swdl)
            self.program_info_table.append(sample_info_entry)


class SampleInfoEntry:
    unk1: int = 0x1AA
    id_: int
    fine_tune: int
    coarse_tune: int
    root_key: int
    key_transpose: int
    volume: int
    pan: int
    unk5: int = 0
    unk58: int = 0x02
    unk6: int = 0
    unk7: int = 0
    version: int = 0x415
    sample_format: int
    # 0 - 8 bits pcm?
    # 0x100 - 16 bits pcm
    # 0x200 - 4 bits adpcm
    # 0x300 - psg?
    unk9: int
    loop_enabled: bool
    unk10: int
    unk11: int
    unk12: int
    unk13: int = 0
    sample_rate: int
    sample_pos: int
    loop_beginning: int
    loop_length: int
    envelope: int
    envelope_multiplier: int
    unk19: int
    unk20: int
    unk21: int
    unk22: int
    attack_volume: int
    attack: int
    decay: int
    sustain: int
    hold: int
    decay2: int
    release: int
    unk57: int

    def read(self, rdr: BinaryReader):
        self.unk1 = rdr.read_uint16()
        self.id_ = rdr.read_uint16()
        self.fine_tune = rdr.read_int8()
        self.coarse_tune = rdr.read_int8()
        self.root_key = rdr.read_int8()
        self.key_transpose = rdr.read_int8()
        self.volume = rdr.read_int8()
        self.pan = rdr.read_int8()
        self.unk5 = rdr.read_uint8()
        self.unk58 = rdr.read_uint8()
        self.unk6 = rdr.read_uint16()
        self.unk7 = rdr.read_uint16()
        self.version = rdr.read_uint16()
        if self.version != 0x415:
            raise ValueError("SampleInfoEntry does not have correct version")
        self.sample_format = rdr.read_uint16()
        self.unk9 = rdr.read_uint8()
        self.loop_enabled = rdr.read_bool()
        self.unk10 = rdr.read_uint16()
        self.unk11 = rdr.read_uint16()
        self.unk12 = rdr.read_uint16()
        self.unk13 = rdr.read_uint32()
        self.sample_rate = rdr.read_uint32()
        self.sample_pos = rdr.read_uint32()
        self.loop_beginning = rdr.read_uint32()
        self.loop_length = rdr.read_uint32()
        self.envelope = rdr.read_uint8()
        self.envelope_multiplier = rdr.read_uint8()
        self.unk19 = rdr.read_uint8()
        self.unk20 = rdr.read_uint8()
        self.unk21 = rdr.read_uint16()
        self.unk22 = rdr.read_uint16()
        self.attack_volume = rdr.read_int8()
        self.attack = rdr.read_int8()
        self.decay = rdr.read_int8()
        self.sustain = rdr.read_int8()
        self.hold = rdr.read_int8()
        self.decay2 = rdr.read_int8()
        self.release = rdr.read_int8()
        self.unk57 = rdr.read_int8()


class WaviChunk:
    magic: bytes = b"wavi"
    unk1: int
    version: int = 0x415  # maybe
    chunk_beg: int = 0x10
    chunk_len: int
    wav_table: List[int]
    sample_info_table: List[SampleInfoEntry]

    def read(self, rdr: BinaryReader, header: 'SWDHeader'):
        self.magic = rdr.read(4)
        if self.magic != b"wavi":
            raise ValueError("SWDWaviChunk does not start with magic value")
        self.unk1 = rdr.read_uint16()
        self.version = rdr.read_uint16()
        if self.version != 0x415:
            raise ValueError("SWDWaviChunk does not have correct version")
        self.chunk_beg = rdr.read_uint32()
        self.chunk_len = rdr.read_uint32()
        pos = rdr.c
        self.wav_table = []
        for _ in range(header.wavi_slot_count):
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
    unk10: int
    unk13: int
    pcmdlen: int
    unk14: int
    wavi_slot_count: int
    prgi_slot_count: int
    unk17: int
    wavi_len: int  # len of wavi chunk

    def read(self, rdr: BinaryReader):
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
        self.unk10 = rdr.read_uint32()
        # 8 bytes of 0
        rdr.read_uint32()
        rdr.read_uint32()
        self.unk13 = rdr.read_uint32()
        self.pcmdlen = rdr.read_uint32()
        self.unk14 = rdr.read_uint16()
        self.wavi_slot_count = rdr.read_uint16()
        self.prgi_slot_count = rdr.read_uint16()
        self.unk17 = rdr.read_uint16()
        self.wavi_len = rdr.read_uint32()


# TODO: Finish new SWD format for consistency
class SWDL(FileFormat):
    swd_header: SWDHeader
    wavi_chunk: WaviChunk
    prgi_chunk: PrgiChunk
    kgrp_chunk: KgrpChunk
    pcmd_chunk: PcmdChunk = None
    eod_chunk: EodChunk

    ima_compressor: ImaAdpcm

    def read_stream(self, stream):
        self.ima_compressor = ImaAdpcm()
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
                self.swd_header = SWDHeader()
                self.swd_header.read(rdr)
            elif chunk_name == b"wavi":
                self.wavi_chunk = WaviChunk()
                self.wavi_chunk.read(rdr, self.swd_header)
            elif chunk_name == b"prgi":
                self.prgi_chunk = PrgiChunk()
                self.prgi_chunk.read(rdr, self)
            elif chunk_name == b"kgrp":
                self.kgrp_chunk = KgrpChunk()
                self.kgrp_chunk.read(rdr)
            elif chunk_name == b"pcmd":
                self.pcmd_chunk = PcmdChunk()
                self.pcmd_chunk.read(rdr)
            elif chunk_name == b"eod ":
                self.eod_chunk = EodChunk()
                self.eod_chunk.read(rdr)
                break

    def write_stream(self, stream):
        raise NotImplementedError('saving swd still not implemented')

    def get_sample_list(self):
        res = []
        for sample_entry in self.wavi_chunk.sample_info_table:
            res.append(sample_entry.id_)
        return res

    def get_sample_info(self, sample_id) -> Optional[SampleInfoEntry]:
        for sample_entry in self.wavi_chunk.sample_info_table:
            if sample_entry.id_ == sample_id:
                return sample_entry
        else:
            return None

    def get_sample(self, sample_id):
        for sample_entry in self.wavi_chunk.sample_info_table:
            if sample_entry.id_ == sample_id:
                break
        else:
            return None
        sample_entry: SampleInfoEntry
        sample_length = (sample_entry.loop_beginning + sample_entry.loop_length) * 4
        sample_data = self.pcmd_chunk.sample_data[sample_entry.sample_pos:sample_entry.sample_pos + sample_length]
        if sample_entry.sample_format == 0x100:  # is already 16 bit pcm
            dt = np.dtype(np.int16).newbyteorder("<")
            sample_data: np.ndarray = np.frombuffer(sample_data, dtype=dt)
        elif sample_entry.sample_format == 0x200:
            self.ima_compressor.reset()
            sample_data = self.ima_compressor.decompress(sample_data)
        else:
            raise NotImplementedError(f"Sample format {sample_entry.sample_format} not implemented")
        sample_data = sample_data.reshape((sample_data.shape[0], 1))
        return sample_data

    def get_program_list(self):
        res = []
        for program_entry in self.prgi_chunk.program_info_table:
            res.append(program_entry.program_id)
        return res

    def get_program(self, program_id) -> Optional[ProgramInfoEntry]:
        for program_entry in self.prgi_chunk.program_info_table:
            if program_entry.program_id == program_id:
                return program_entry
        else:
            return None
