import io
import logging
import math
import re
import typing
from enum import IntEnum
from typing import Union, Optional, List, Dict

import numpy as np

from formats.binary import BinaryReader, BinaryWriter
from formats.sound.sound_types import Sample, Program, Split


def ms_to_timecent(ms: int):
    if ms == 0:
        return -32768
    return int(1200 * math.log2(ms / 1000))


class IfilChunk:
    def __init__(self, major=2, minor=4):
        self.major = major
        self.minor = minor

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"ifil":
            raise ValueError("Invalid ifil header")
        _chunk_size = rdr.read_uint32()
        self.major = rdr.read_uint16()
        self.minor = rdr.read_uint16()

    def write(self, wtr: BinaryWriter):
        wtr.write(b"ifil")
        wtr.write_uint32(4)
        wtr.write_uint16(self.major)
        wtr.write_uint16(self.minor)


class IsngChunk:
    def __init__(self, sound_engine="EMU8000"):
        self.sound_engine = sound_engine

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"isng":
            raise ValueError("Invalid isng header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.sound_engine = rdr.read_string(encoding="ascii")
        rdr.seek(end_pos)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"isng")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place-holder chunk size
        wtr.write_string(self.sound_engine[:255], encoding="ascii")
        wtr.align(2)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class INAMChunk:
    def __init__(self, name="General Midi"):
        self.name = name

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"INAM":
            raise ValueError("Invalid INAM header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.name = rdr.read_string(encoding="ascii")
        rdr.seek(end_pos)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"INAM")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place-holder chunk size
        wtr.write_string(self.name[:255], encoding="ascii")
        wtr.align(2)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class IromChunk:
    def __init__(self, rom=""):
        self.rom = rom

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"irom":
            raise ValueError("Invalid irom header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.rom = rdr.read_string(encoding="ascii")
        rdr.seek(end_pos)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"irom")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place-holder chunk size
        wtr.write_string(self.rom[:255], encoding="ascii")
        wtr.align(2)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class IverChunk:
    def __init__(self, major=0, minor=0):
        self.major = major
        self.minor = minor

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"iver":
            raise ValueError("Invalid iver header")
        _chunk_size = rdr.read_uint32()
        self.major = rdr.read_uint16()
        self.minor = rdr.read_uint16()

    def write(self, wtr: BinaryWriter):
        wtr.write(b"iver")
        wtr.write_uint32(4)
        wtr.write_uint16(self.major)
        wtr.write_uint16(self.minor)


class ICRDChunk:
    def __init__(self, date=""):
        self.date = date

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"ICRD":
            raise ValueError("Invalid ICRD header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.date = rdr.read_string(encoding="ascii")
        rdr.seek(end_pos)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"ICRD")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place-holder chunk size
        wtr.write_string(self.date[:255], encoding="ascii")
        wtr.align(2)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class IENGChunk:
    def __init__(self, authors=""):
        self.authors = authors

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"IENG":
            raise ValueError("Invalid IENG header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.authors = rdr.read_string(encoding="ascii")
        rdr.seek(end_pos)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"IENG")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place-holder chunk size
        wtr.write_string(self.authors[:255], encoding="ascii")
        wtr.align(2)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class IPRDChunk:
    def __init__(self, product=""):
        self.product = product

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"IPRD":
            raise ValueError("Invalid IPRD header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.product = rdr.read_string(encoding="ascii")
        rdr.seek(end_pos)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"IPRD")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place-holder chunk size
        wtr.write_string(self.product[:255], encoding="ascii")
        wtr.align(2)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class ICOPChunk:
    def __init__(self, copyright_=""):
        self.copyright = copyright_

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"ICOP":
            raise ValueError("Invalid ICOP header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.copyright = rdr.read_string(encoding="ascii")
        rdr.seek(end_pos)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"ICOP")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place-holder chunk size
        wtr.write_string(self.copyright[:255], encoding="ascii")
        wtr.align(2)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class ICMTChunk:
    def __init__(self, comment=""):
        self.comment = comment

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"ICMT":
            raise ValueError("Invalid ICMT header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.comment = rdr.read_string(encoding="ascii")
        rdr.seek(end_pos)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"ICMT")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place-holder chunk size
        wtr.write_string(self.comment[:255], encoding="ascii")
        wtr.align(2)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class ISFTChunk:
    def __init__(self, sound_font_tool=""):
        self.sound_font_tool = sound_font_tool

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"ISFT":
            raise ValueError("Invalid ISFT header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.sound_font_tool = rdr.read_string(encoding="ascii")
        rdr.seek(end_pos)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"ISFT")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place-holder chunk size
        wtr.write_string(self.sound_font_tool[:255], encoding="ascii")
        wtr.align(2)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class InfoChunk:
    def __init__(self):
        self.ifil_chunk = IfilChunk()
        self.isng_chunk = IsngChunk()
        self.inam_chunk = INAMChunk()
        self.irom_chunk: Optional[IromChunk] = None
        self.iver_chunk: Optional[IverChunk] = None
        self.icrd_chunk: Optional[ICRDChunk] = None
        self.ieng_chunk: Optional[IENGChunk] = None
        self.iprd_chunk: Optional[IPRDChunk] = None
        self.icop_chunk: Optional[ICOPChunk] = None
        self.icmt_chunk: Optional[ICMTChunk] = None
        self.isft_chunk: Optional[ISFTChunk] = None

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"LIST":
            raise ValueError("Invalid INFO header")

        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size

        if rdr.read(4) != b"INFO":
            raise ValueError("Invalid INFO header")

        self.ifil_chunk = None
        self.isng_chunk = None
        self.inam_chunk = None
        self.irom_chunk = None
        self.iver_chunk = None
        self.icrd_chunk = None
        self.ieng_chunk = None
        self.iprd_chunk = None
        self.icop_chunk = None
        self.icmt_chunk = None
        self.isft_chunk = None
        while rdr.tell() < end_pos:
            chunk_name = rdr.read(4)
            rdr.seek(rdr.tell() - 4)
            if chunk_name == b"ifil":
                self.ifil_chunk = IfilChunk()
                self.ifil_chunk.read(rdr)
            elif chunk_name == b"isng":
                self.isng_chunk = IsngChunk()
                self.isng_chunk.read(rdr)
            elif chunk_name == b"INAM":
                self.inam_chunk = INAMChunk()
                self.inam_chunk.read(rdr)
            elif chunk_name == b"irom":
                self.irom_chunk = IromChunk()
                self.irom_chunk.read(rdr)
            elif chunk_name == b"iver":
                self.iver_chunk = IverChunk()
                self.iver_chunk.read(rdr)
            elif chunk_name == b"ICRD":
                self.icrd_chunk = ICRDChunk()
                self.icrd_chunk.read(rdr)
            elif chunk_name == b"IENG":
                self.ieng_chunk = IENGChunk()
                self.ieng_chunk.read(rdr)
            elif chunk_name == b"IPRD":
                self.iprd_chunk = IPRDChunk()
                self.iprd_chunk.read(rdr)
            elif chunk_name == b"ICOP":
                self.icop_chunk = ICOPChunk()
                self.icop_chunk.read(rdr)
            elif chunk_name == b"ICMT":
                self.icmt_chunk = ICMTChunk()
                self.icmt_chunk.read(rdr)
            elif chunk_name == b"ISFT":
                self.isft_chunk = ISFTChunk()
                self.isft_chunk.read(rdr)
            else:
                raise ValueError(f"Invalid INFO sub-chunk: {chunk_name}")

        if self.ifil_chunk is None or self.isng_chunk is None or self.inam_chunk is None:
            raise ValueError("INFO chunk missing one of the required sub-chunks")

    def write(self, wtr: BinaryWriter):
        wtr.write(b"LIST")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place holder chunk size
        wtr.write(b"INFO")
        if self.ifil_chunk is not None:
            self.ifil_chunk.write(wtr)
        if self.isng_chunk is not None:
            self.isng_chunk.write(wtr)
        if self.inam_chunk is not None:
            self.inam_chunk.write(wtr)
        if self.irom_chunk is not None:
            self.irom_chunk.write(wtr)
        if self.iver_chunk is not None:
            self.iver_chunk.write(wtr)
        if self.icrd_chunk is not None:
            self.icrd_chunk.write(wtr)
        if self.ieng_chunk is not None:
            self.ieng_chunk.write(wtr)
        if self.iprd_chunk is not None:
            self.iprd_chunk.write(wtr)
        if self.icop_chunk is not None:
            self.icop_chunk.write(wtr)
        if self.icmt_chunk is not None:
            self.icmt_chunk.write(wtr)
        if self.isft_chunk is not None:
            self.isft_chunk.write(wtr)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class SmplChunk:
    def __init__(self, data: Optional[np.ndarray] = None):
        self.data: np.ndarray = data
        self.position = 0  # Used for writing
    
    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"smpl":
            raise ValueError("Invalid smpl header")
        chunk_size = rdr.read_uint32()
        self.data = np.frombuffer(rdr.read(chunk_size), dtype=np.dtype(np.int16).newbyteorder('<'))

    def write(self, wtr: BinaryWriter):
        wtr.write(b"smpl")
        data_bin = self.data.tobytes()
        wtr.write_uint32(len(data_bin))  # chunk size
        wtr.write(data_bin)


class Sm24Chunk:
    def __init__(self, data: Optional[np.ndarray] = None):
        self.data: np.ndarray = data
        
    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"sm24":
            raise ValueError("Invalid sm24 header")
        chunk_size = rdr.read_uint32()
        self.data = np.frombuffer(rdr.read(chunk_size), dtype=np.uint8)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"sm24")
        data_bin = self.data.tobytes()
        wtr.write_uint32(len(data_bin))  # chunk size
        wtr.write(data_bin)


class SdtaChunk:
    def __init__(self):
        self.smpl_chunk: Optional[SmplChunk] = None
        self.sm24_chunk: Optional[Sm24Chunk] = None
    
    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"LIST":
            raise ValueError("Invalid sdta header")

        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size

        if rdr.read(4) != b"sdta":
            raise ValueError("Invalid sdta header")

        self.smpl_chunk = None
        self.sm24_chunk = None
        while rdr.tell() < end_pos:
            chunk_name = rdr.read(4)
            rdr.seek(rdr.tell() - 4)
            if chunk_name == b"smpl":
                self.smpl_chunk = SmplChunk()
                self.smpl_chunk.read(rdr)
            elif chunk_name == b"sm24":
                self.sm24_chunk = Sm24Chunk()
                self.sm24_chunk.read(rdr)
                raise NotImplementedError("LaytonEditor does not support 24-bit samples")
            else:
                raise ValueError(f"Invalid sdta sub-chunk: {chunk_name}")

    def write(self, wtr: BinaryWriter):
        wtr.write(b"LIST")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place holder chunk size
        wtr.write(b"sdta")

        if self.smpl_chunk is not None:
            self.smpl_chunk.write(wtr)
        if self.sm24_chunk is not None:
            self.sm24_chunk.write(wtr)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class SFGeneratorEnumerator(IntEnum):
    START_ADDRESS_OFFSET = 0
    END_ADDRESS_OFFSET = 1
    START_LOOP_ADDRESS_OFFSET = 2
    END_LOOP_ADDRESS_OFFSET = 3
    START_ADDRESS_COARSE_OFFSET = 4
    MOD_LFO_TO_PITCH = 5
    VIB_LFO_TO_PITCH = 6
    MOD_ENV_TO_PITCH = 7
    INITIAL_FILTER_FC = 8
    INITIAL_FILTER_Q = 9
    MOD_LFO_TO_FILTER_FC = 10
    MOD_ENV_TO_FILTER_FC = 11
    END_ADDRESS_COARSE_OFFSET = 12
    MOD_LFO_TO_VOLUME = 13
    CHORUS_EFFECTS_SEND = 15
    REVERB_EFFECTS_SEND = 16
    PAN = 17
    DELAY_MOD_LFO = 21
    FREQ_MOD_LFO = 22
    DELAY_VIB_LFO = 23
    FREQ_VIB_LFO = 24
    DELAY_MOD_ENV = 25
    ATTACK_MOD_ENV = 26
    HOLD_MOD_ENV = 27
    DECAY_MOD_ENV = 28
    SUSTAIN_MOD_ENV = 29
    RELEASE_MOD_ENV = 30
    KEYNUM_TO_MOD_ENV_HOLD = 31
    KEYNUM_TO_MOD_ENV_DECAY = 32
    DELAY_VOL_ENV = 33
    ATTACK_VOL_ENV = 34
    HOLD_VOL_ENV = 35
    DECAY_VOL_ENV = 36
    SUSTAIN_VOL_ENV = 37
    RELEASE_VOL_ENV = 38
    KEYNUM_TO_VOL_ENV_HOLD = 39
    KEYNUM_TO_VOL_ENV_DECAY = 40
    INSTRUMENT = 41
    KEY_RANGE = 43
    VEL_RANGE = 44
    START_LOOP_ADDRESS_COARSE_OFFSET = 45
    KEYNUM = 46
    VELOCITY = 47
    INITIAL_ATTENUATION = 48
    END_LOOP_ADDRESS_COARSE_OFFSET = 50
    COARSE_TUNE = 51
    FINE_TUNE = 52
    SAMPLE_ID = 53
    SAMPLE_MODES = 54
    SCALE_TUNING = 56
    EXCLUSIVE_CLASS = 57
    OVERRIDING_ROOT_KEY = 58


class SFPresetHeader:
    def __init__(self):
        self.preset_name = ""
        self.preset_id = 0
        self.preset_bank = 0
        self.preset_bag_ndx = 0
        self.library = 0
        self.genre = 0
        self.morphology = 0

    def read(self, rdr: BinaryReader):
        self.preset_name = rdr.read_string(size=20, encoding="ascii")
        self.preset_id = rdr.read_uint16()
        self.preset_bank = rdr.read_uint16()
        self.preset_bag_ndx = rdr.read_uint16()
        self.library = rdr.read_uint32()
        self.genre = rdr.read_uint32()
        self.morphology = rdr.read_uint32()

    def write(self, wtr: BinaryWriter):
        wtr.write_string(self.preset_name, size=20, encoding="ascii")
        wtr.write_uint16(self.preset_id)
        wtr.write_uint16(self.preset_bank)
        wtr.write_uint16(self.preset_bag_ndx)
        wtr.write_uint32(self.library)
        wtr.write_uint32(self.genre)
        wtr.write_uint32(self.morphology)

    def to_program(self, pdta_chunk: 'PdtaChunk', next_preset_header: 'SFPresetHeader',
                   samples: List[Sample]) -> Program:
        program = Program()
        program.id_ = self.preset_id
        program.name = self.preset_name
        program.lfos = []
        program.splits = []
        # Get the next instrument bag
        instrument_last_bag = pdta_chunk.pbag_chunk.preset_bags[self.preset_bag_ndx]
        instrument_next_bag = pdta_chunk.pbag_chunk.preset_bags[next_preset_header.preset_bag_ndx]
        instrument_id = None
        for gen_ndx in range(instrument_last_bag.gen_ndx, instrument_next_bag.gen_ndx):
            instrument_gen = pdta_chunk.pgen_chunk.gen_list[gen_ndx]
            if instrument_gen.operation == SFGeneratorEnumerator.INSTRUMENT:
                instrument_id = instrument_gen.amount
                break
            elif instrument_gen.operation == SFGeneratorEnumerator.PAN:
                program.pan = round((instrument_gen.amount_signed * 127) / (10 * 100))
        # Get the generator for the instrument (last gen in current bag)
        assert instrument_id is not None
        instrument = pdta_chunk.inst_chunk.instruments[instrument_id]
        instrument_next = pdta_chunk.inst_chunk.instruments[instrument_id + 1]

        for ibag_idx in range(instrument.inst_bag_ndx + 1, instrument_next.inst_bag_ndx):
            ibag = pdta_chunk.ibag_chunk.instrument_bags[ibag_idx]
            ibag_next = pdta_chunk.ibag_chunk.instrument_bags[ibag_idx + 1]
            split = Split()
            set_sample = False
            set_root_key = False
            for gen_idx in range(ibag.gen_ndx, ibag_next.gen_ndx):
                igen = pdta_chunk.igen_chunk.gen_list[gen_idx]
                if igen.operation == SFGeneratorEnumerator.SAMPLE_ID:
                    split.sample = samples[igen.amount]
                    set_sample = True
                elif igen.operation == SFGeneratorEnumerator.KEY_RANGE:
                    split.low_key, split.high_key = igen.amount_range
                elif igen.operation == SFGeneratorEnumerator.VEL_RANGE:
                    split.low_vel, split.high_vel = igen.amount_range
                elif igen.operation == SFGeneratorEnumerator.FINE_TUNE:
                    split.fine_tune = igen.amount_signed
                elif igen.operation == SFGeneratorEnumerator.COARSE_TUNE:
                    split.coarse_tune = igen.amount_signed
                elif igen.operation == SFGeneratorEnumerator.OVERRIDING_ROOT_KEY:
                    split.root_key = igen.amount
                    set_root_key = True
                elif igen.operation == SFGeneratorEnumerator.PAN:
                    # amount is in increments of 0.1%, from 0% to 100% (1000)
                    # in splits is -500 to 500
                    split.pan = round(((igen.amount_signed + 500.0) * 127) / (10 * 100))
                # TODO: Add envelope, attack, decay, sustain...
            if set_sample:  # only add zone if it has a sample associated (else is a global zone)
                if not set_root_key:
                    split.root_key = split.sample.root_key
                program.splits.append(split)
        return program

    def from_program(self, program: Program, pdta_chunk: 'PdtaChunk',
                     samples: List[Sample]):
        if program.name is None:
            self.preset_name = f"preset {program.id_}"
        else:
            self.preset_name = program.name
        self.preset_id = program.id_
        # When we create a preset, we must map it to an instrument which will be mapped to the samples
        # A preset consists of preset bags, each pointing to a generator list and a modifier list
        # We must create an instrument generator for this preset on its final bag,
        # and then create a bag for the next preset, or a final bag in case there are no more presets

        # Add a bag for the next preset (or final)
        next_bag = SFBag()
        pdta_chunk.pbag_chunk.preset_bags.append(next_bag)

        # We must set the next preset bag_ndx (preset bag count - 1 at the moment) to the terminal record
        next_preset_header = SFPresetHeader()
        pdta_chunk.phdr_chunk.preset_headers.append(next_preset_header)
        next_preset_header.preset_bag_ndx = len(pdta_chunk.pbag_chunk.preset_bags) - 1

        # Add the instrument generator for the preset
        generator = SFGenEntry(operation=SFGeneratorEnumerator.INSTRUMENT,
                               # Last instrument (currently terminal)
                               amount=len(pdta_chunk.inst_chunk.instruments) - 1)
        pdta_chunk.pgen_chunk.gen_list.insert(-1, generator)

        # The next gen ndx is the index of the terminal record for now
        next_bag.gen_ndx = len(pdta_chunk.pgen_chunk.gen_list) - 1

        # Get the last instrument (currently terminal)
        instrument = pdta_chunk.inst_chunk.instruments[-1]

        # Add the next instrument (maybe terminal)
        next_instrument = SFInst()
        pdta_chunk.inst_chunk.instruments.append(next_instrument)

        instrument.name = f"inst {program.id_}"
        for split in program.splits:
            next_instrument_bag = SFBag()
            pdta_chunk.ibag_chunk.instrument_bags.append(next_instrument_bag)

            # Add key range
            pdta_chunk.igen_chunk.gen_list.insert(-1, SFGenEntry(operation=SFGeneratorEnumerator.KEY_RANGE,
                                                                 amount_range=[split.low_key, split.high_key]))

            # Add vel range
            pdta_chunk.igen_chunk.gen_list.insert(-1, SFGenEntry(operation=SFGeneratorEnumerator.VEL_RANGE,
                                                                 amount_range=[split.low_vel, split.high_vel]))

            # Add override root key
            if split.sample.root_key != split.root_key:
                pdta_chunk.igen_chunk.gen_list.insert(-1,
                                                      SFGenEntry(operation=SFGeneratorEnumerator.OVERRIDING_ROOT_KEY,
                                                                 amount=split.root_key))

            pdta_chunk.igen_chunk.gen_list.insert(-1, SFGenEntry(operation=SFGeneratorEnumerator.SAMPLE_MODES,
                                                                 amount=1 if split.sample.loop_enabled else 0))

            """
            Ignore tuning for now (doesn't seem to work)
            # Add fine tune
            if split.fine_tune != 0:
                pdta_chunk.igen_chunk.gen_list.insert(-1, SFGenEntry(operation=SFGeneratorEnumerator.FINE_TUNE,
                                                                     amount_signed=split.fine_tune))

            # Add coarse tune
            if split.coarse_tune != 0:
                pdta_chunk.igen_chunk.gen_list.insert(-1, SFGenEntry(operation=SFGeneratorEnumerator.COARSE_TUNE,
                                                                     amount_signed=split.coarse_tune))
            """

            # Add pan
            if split.pan != 64:
                # Convert pan
                pan = round(split.pan * 1000 / 127)
                pdta_chunk.igen_chunk.gen_list.insert(-1, SFGenEntry(operation=SFGeneratorEnumerator.PAN,
                                                                     amount=pan))

            if split.envelope_on:
                # Can't use attack as we cannot simulate split.attack_volume
                # SF2 always starts at volume 0, but SWDL does not
                # if split.attack != 0:
                #     pdta_chunk.igen_chunk.gen_list.insert(-1,
                #                                           SFGenEntry(operation=SFGeneratorEnumerator.ATTACK_VOL_ENV,
                #                                                      amount_signed=ms_to_timecent(split.attack)))

                if split.decay != 0:
                    pdta_chunk.igen_chunk.gen_list.insert(-1, SFGenEntry(operation=SFGeneratorEnumerator.DECAY_VOL_ENV,
                                                                         amount_signed=ms_to_timecent(split.decay)))

                # if split.sustain != 0:
                #     pdta_chunk.igen_chunk.gen_list.insert(-1,
                #                                           SFGenEntry(operation=SFGeneratorEnumerator.SUSTAIN_VOL_ENV,
                #                                                      amount=int(1000 * (split.sustain / 0x7f))))

                if split.hold != 0:
                    pdta_chunk.igen_chunk.gen_list.insert(-1, SFGenEntry(operation=SFGeneratorEnumerator.HOLD_VOL_ENV,
                                                                         amount_signed=ms_to_timecent(split.hold)))

                if split.release != 0:
                    pdta_chunk.igen_chunk.gen_list.insert(-1,
                                                          SFGenEntry(operation=SFGeneratorEnumerator.RELEASE_VOL_ENV,
                                                                     amount_signed=ms_to_timecent(split.release)))

            # TODO: Add envelope, attack, decay, sustain

            # Add sample
            pdta_chunk.igen_chunk.gen_list.insert(-1, SFGenEntry(operation=SFGeneratorEnumerator.SAMPLE_ID,
                                                                 amount=samples.index(split.sample)))

            # Set next bag gen_ndx (maybe terminal) to the current terminal
            next_instrument_bag.gen_ndx = len(pdta_chunk.igen_chunk.gen_list) - 1

        next_instrument.inst_bag_ndx = len(pdta_chunk.ibag_chunk.instrument_bags) - 1


class PhdrChunk:
    preset_headers: List[SFPresetHeader]

    def __init__(self):
        self.preset_headers = [SFPresetHeader()]  # Terminal record

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"phdr":
            raise ValueError("Invalid phdr header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.preset_headers = []
        while rdr.tell() < end_pos:
            preset_header = SFPresetHeader()
            preset_header.read(rdr)
            self.preset_headers.append(preset_header)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"phdr")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place holder chunk size
        for preset_header in self.preset_headers:
            preset_header.write(wtr)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class SFBag:
    def __init__(self):
        self.gen_ndx = 0
        self.mod_ndx = 0

    def read(self, rdr: BinaryReader):
        self.gen_ndx = rdr.read_uint16()
        self.mod_ndx = rdr.read_uint16()

    def write(self, wtr: BinaryWriter):
        wtr.write_uint16(self.gen_ndx)
        wtr.write_uint16(self.mod_ndx)


class PbagChunk:
    preset_bags: List[SFBag]

    def __init__(self):
        self.preset_bags = [SFBag()]  # Terminal record

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"pbag":
            raise ValueError("Invalid pbag header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.preset_bags = []
        while rdr.tell() < end_pos:
            preset_bag = SFBag()
            preset_bag.read(rdr)
            self.preset_bags.append(preset_bag)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"pbag")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place holder chunk size
        for preset_bag in self.preset_bags:
            preset_bag.write(wtr)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class SFModEntry:
    def __init__(self):
        self.source = 0
        self.destination = 0
        self.amount = 0
        self.amt_source = 0
        self.transform = 0

    def read(self, rdr: BinaryReader):
        self.source = rdr.read_uint16()
        self.destination = rdr.read_uint16()
        self.amount = rdr.read_int16()
        self.amt_source = rdr.read_uint16()
        self.transform = rdr.read_uint16()

    def write(self, wtr: BinaryWriter):
        wtr.write_uint16(self.source)
        wtr.write_uint16(self.destination)
        wtr.write_uint16(self.amount)
        wtr.write_uint16(self.amt_source)
        wtr.write_uint16(self.transform)


class PmodChunk:
    mod_list: List[SFModEntry]

    def __init__(self):
        self.mod_list = [SFModEntry()]  # Terminal record

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"pmod":
            raise ValueError("Invalid pmod header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.mod_list = []
        while rdr.tell() < end_pos:
            mod_list = SFModEntry()
            mod_list.read(rdr)
            self.mod_list.append(mod_list)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"pmod")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place holder chunk size
        for mod in self.mod_list:
            mod.write(wtr)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class SFGenEntry:
    def __init__(self, operation=0, amount=0, amount_signed=None, amount_range=None):
        self.operation = operation
        self.amount = amount
        if amount_signed is not None:
            self.amount_signed = amount_signed
        if amount_range is not None:
            self.amount_range = amount_range

    @property
    def amount_signed(self):
        return (self.amount ^ 0x8000) - 0x8000

    @amount_signed.setter
    def amount_signed(self, v: int):
        self.amount = (v + 0x8000) ^ 0x8000

    @property
    def amount_range(self):
        # amount is little endian
        return self.amount & 0xFF, self.amount >> 8

    @amount_range.setter
    def amount_range(self, v: tuple):
        # amount is little endian
        self.amount = (v[0] & 0xFF) + (v[1] << 8)

    def read(self, rdr: BinaryReader):
        self.operation = rdr.read_uint16()
        self.amount = rdr.read_uint16()

    def write(self, wtr: BinaryWriter):
        wtr.write_uint16(self.operation)
        wtr.write_uint16(self.amount)


class PgenChunk:
    gen_list: List[SFGenEntry]

    def __init__(self):
        self.gen_list = [SFGenEntry()]

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"pgen":
            raise ValueError("Invalid pgen header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.gen_list = []
        while rdr.tell() < end_pos:
            gen_list = SFGenEntry()
            gen_list.read(rdr)
            self.gen_list.append(gen_list)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"pgen")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place holder chunk size
        for gen in self.gen_list:
            gen.write(wtr)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class SFInst:
    def __init__(self):
        self.name = ""
        self.inst_bag_ndx = 0

    def read(self, rdr: BinaryReader):
        self.name = rdr.read_string(size=20, encoding="ascii")
        self.inst_bag_ndx = rdr.read_uint16()

    def write(self, wtr: BinaryWriter):
        wtr.write_string(self.name, size=20, encoding="ascii")
        wtr.write_uint16(self.inst_bag_ndx)


class InstChunk:
    instruments: List[SFInst]

    def __init__(self):
        self.instruments = [SFInst()]  # Terminal record

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"inst":
            raise ValueError("Invalid inst header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.instruments = []
        while rdr.tell() < end_pos:
            instrument = SFInst()
            instrument.read(rdr)
            self.instruments.append(instrument)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"inst")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place holder chunk size
        for instrument in self.instruments:
            instrument.write(wtr)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class IbagChunk:
    instrument_bags: List[SFBag]

    def __init__(self):
        self.instrument_bags = [SFBag()]  # Terminal record

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"ibag":
            raise ValueError("Invalid ibag header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.instrument_bags = []
        while rdr.tell() < end_pos:
            instrument_bag = SFBag()
            instrument_bag.read(rdr)
            self.instrument_bags.append(instrument_bag)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"ibag")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place holder chunk size
        for inst_bag in self.instrument_bags:
            inst_bag.write(wtr)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class ImodChunk:
    mod_list: List[SFModEntry]

    def __init__(self):
        self.mod_list = []

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"imod":
            raise ValueError("Invalid imod header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.mod_list = []
        while rdr.tell() < end_pos:
            mod_list = SFModEntry()
            mod_list.read(rdr)
            self.mod_list.append(mod_list)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"imod")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place holder chunk size
        for mod in self.mod_list:
            mod.write(wtr)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class IgenChunk:
    gen_list: List[SFGenEntry]

    def __init__(self):
        self.gen_list = [SFGenEntry()]  # Terminal record

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"igen":
            raise ValueError("Invalid igen header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.gen_list = []
        while rdr.tell() < end_pos:
            gen_list = SFGenEntry()
            gen_list.read(rdr)
            self.gen_list.append(gen_list)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"igen")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place holder chunk size
        for gen in self.gen_list:
            gen.write(wtr)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)


class SFSample:
    def __init__(self):
        self.name = ""
        self.start = 0
        self.end = 0
        self.start_loop = 0
        self.end_loop = 0
        self.rate = 0
        self.original_key = 0
        self.pitch_correction = 0
        self.link = 0
        self.type = 1

    def read(self, rdr: BinaryReader):
        self.name = rdr.read_string(size=20, encoding="ascii")
        self.start = rdr.read_uint32()
        self.end = rdr.read_uint32()
        self.start_loop = rdr.read_uint32()
        self.end_loop = rdr.read_uint32()
        self.rate = rdr.read_uint32()
        self.original_key = rdr.read_uint8()
        self.pitch_correction = rdr.read_int8()
        self.link = rdr.read_uint16()
        self.type = rdr.read_uint16()

    def write(self, wtr: BinaryWriter):
        wtr.write_string(self.name, size=20, encoding="ascii")
        wtr.write_uint32(self.start)
        wtr.write_uint32(self.end)
        wtr.write_uint32(self.start_loop)
        wtr.write_uint32(self.end_loop)
        wtr.write_uint32(self.rate)
        wtr.write_uint8(self.original_key)
        wtr.write_int8(self.pitch_correction)
        wtr.write_uint16(self.link)
        wtr.write_uint16(self.type)

    def to_sample(self, sdta_chunk: SdtaChunk) -> Sample:
        sample = Sample()
        sample.name = self.name
        if res := re.match("^sample ([0-9]+)$", self.name):
            sample.id = int(res.group(1))
        else:
            sample.id_ = None
        sample.loop_beginning = self.start_loop - self.start
        sample.loop_length = self.end_loop - self.start_loop
        sample.sample_rate = self.rate
        sample.root_key = self.original_key
        sample.fine_tune = self.pitch_correction
        pcm16 = sdta_chunk.smpl_chunk.data[self.start:self.end]
        sample.pcm16 = pcm16.reshape((pcm16.shape[0], 1))
        return sample

    def from_sample(self, sample: Sample, sdta_chunk: SdtaChunk):
        if sample.name is None:
            self.name = f"sample {sample.id_}"
        else:
            self.name = sample.name
        self.rate = sample.sample_rate
        self.original_key = sample.root_key
        # Ignore fine tune for now?
        self.pitch_correction = 0  # sample.fine_tune
        self.start = sdta_chunk.smpl_chunk.position
        self.start_loop = self.start + sample.loop_beginning
        self.end_loop = self.start_loop + sample.loop_length
        pcm16 = sample.pcm16
        pcm16 = pcm16.reshape((pcm16.shape[0],))
        self.end = self.start + len(pcm16)
        sdta_chunk.smpl_chunk.data[self.start:self.end] = pcm16
        sdta_chunk.smpl_chunk.position = self.end


class ShdrChunk:
    samples: List[SFSample]

    def __init__(self):
        self.samples = [SFSample()]  # Terminal record

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"shdr":
            raise ValueError("Invalid shdr header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.samples = []
        while rdr.tell() < end_pos:
            sample = SFSample()
            sample.read(rdr)
            self.samples.append(sample)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"shdr")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place holder chunk size
        for sample in self.samples:
            sample.write(wtr)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)

    def from_samples(self, samples: List[Sample], sdta_chunk: SdtaChunk):
        self.samples = [SFSample()]
        data_length = sum([len(sample.pcm16) for sample in samples])
        sdta_chunk.smpl_chunk = SmplChunk(np.zeros((data_length,), np.int16))
        for sample in samples:
            self.samples.insert(-1, SFSample())  # Insert before terminal record
            self.samples[-2].from_sample(sample, sdta_chunk)


class PdtaChunk:
    def __init__(self):
        self.phdr_chunk = PhdrChunk()
        self.pbag_chunk = PbagChunk()
        self.pmod_chunk = PmodChunk()
        self.pgen_chunk = PgenChunk()
        self.inst_chunk = InstChunk()
        self.ibag_chunk = IbagChunk()
        self.imod_chunk = ImodChunk()
        self.igen_chunk = IgenChunk()
        self.shdr_chunk = ShdrChunk()

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"LIST":
            raise ValueError("Invalid pdta header")
        _chunk_size = rdr.read_uint32()
        if rdr.read(4) != b"pdta":
            raise ValueError("Invalid pdta header")
        self.phdr_chunk.read(rdr)
        self.pbag_chunk.read(rdr)
        self.pmod_chunk.read(rdr)
        self.pgen_chunk.read(rdr)
        self.inst_chunk.read(rdr)
        self.ibag_chunk.read(rdr)
        self.imod_chunk.read(rdr)
        self.igen_chunk.read(rdr)
        self.shdr_chunk.read(rdr)

    def write(self, wtr: BinaryWriter):
        wtr.write(b"LIST")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)  # place holder chunk size
        wtr.write(b"pdta")
        self.phdr_chunk.write(wtr)
        self.pbag_chunk.write(wtr)
        self.pmod_chunk.write(wtr)
        self.pgen_chunk.write(wtr)
        self.inst_chunk.write(wtr)
        self.ibag_chunk.write(wtr)
        self.imod_chunk.write(wtr)
        self.igen_chunk.write(wtr)
        self.shdr_chunk.write(wtr)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)

    def from_samples_and_programs(self, samples: List[Sample], programs: List[Program],
                                  sdta_chunk: SdtaChunk):
        self.shdr_chunk.from_samples(samples, sdta_chunk)
        for program in programs:
            terminal_preset_header = self.phdr_chunk.preset_headers[-1]
            terminal_preset_header.from_program(program, self, samples)


class SoundFont:
    info_chunk: InfoChunk
    samples: Dict[int, Sample]
    programs: Dict[int, Program]

    def __init__(self):
        self.info_chunk = InfoChunk()

    def read_stream(self, rdr: Union[bytes, io.BytesIO, BinaryReader]):
        if not isinstance(rdr, BinaryReader):
            rdr = BinaryReader(rdr)
        rdr: BinaryReader

        if rdr.read(4) != b"RIFF":
            raise ValueError("Invalid SoundFont header")
        _chunk_size = rdr.read_uint32()
        if rdr.read(4) != b"sfbk":
            raise ValueError("Invalid SoundFont header")
        
        sdta_chunk = SdtaChunk()
        pdta_chunk = PdtaChunk()

        self.info_chunk.read(rdr)
        sdta_chunk.read(rdr)
        pdta_chunk.read(rdr)

        samples = []
        programs = []
        # Construct data types
        for sf_smpl_header in pdta_chunk.shdr_chunk.samples[:-1]:  # last is terminal record
            samples.append(sf_smpl_header.to_sample(sdta_chunk))
        for i, sf_prg_header in enumerate(pdta_chunk.phdr_chunk.preset_headers[:-1]):
            programs.append(sf_prg_header.to_program(pdta_chunk, pdta_chunk.phdr_chunk.preset_headers[i + 1],
                                                     samples))

        self.samples = {}
        samples_without_id = []
        for sample in samples:
            if sample.id_ is not None:
                self.samples[sample.id_] = sample
            else:
                samples_without_id.append(sample)
        i = 0
        for sample in samples_without_id:
            while i in self.samples:
                i += 1
            self.samples[i] = sample
            sample.id_ = i
        self.programs = {}
        programs_without_id = []
        for program in programs:
            if program.id_ is not None:
                self.programs[program.id_] = program
            else:
                programs_without_id.append(program)
        i = 0
        for program in programs_without_id:
            while i in self.programs:
                i += 1
            self.programs[i] = program
            program.id_ = i

    def write_stream(self, wtr: Union[io.BytesIO, typing.BinaryIO, BinaryWriter]):
        if not isinstance(wtr, BinaryWriter):
            wtr = BinaryWriter(wtr)
        sdta_chunk, pdta_chunk = self.construct()

        wtr.write(b"RIFF")
        chunk_size_pos = wtr.tell()
        wtr.write_uint32(0)
        wtr.write(b"sfbk")
        self.info_chunk.write(wtr)
        sdta_chunk.write(wtr)
        pdta_chunk.write(wtr)

        # write chunk_size
        end_pos = wtr.tell()
        wtr.seek(chunk_size_pos)
        wtr.write_uint32(end_pos - (chunk_size_pos + 4))
        wtr.seek(end_pos)

    def set_sample_data(self, sample_data: Dict[int, Sample]):
        for sample_id, sample in sample_data.items():
            if sample_id not in self.samples:
                continue
            self.samples[sample_id].pcm16 = sample.pcm16
        if any([s.pcm16 is None for s in self.samples.values()]):
            logging.warning("Sample data not fully set")

    def construct(self):
        sdta_chunk = SdtaChunk()
        pdta_chunk = PdtaChunk()

        pdta_chunk.from_samples_and_programs(list(self.samples.values()), list(self.programs.values()),
                                             sdta_chunk)
        return sdta_chunk, pdta_chunk
