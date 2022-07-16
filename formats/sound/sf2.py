import io
from enum import IntEnum
from typing import Union, Optional, List, Dict

import numpy as np

from formats.binary import BinaryReader
from formats.sound.sound_types import Sample, Program, Split


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


class SmplChunk:
    def __init__(self, data: Optional[np.ndarray] = None):
        self.data: np.ndarray = data
    
    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"smpl":
            raise ValueError("Invalid smpl header")
        chunk_size = rdr.read_uint32()
        self.data = np.frombuffer(rdr.read(chunk_size), dtype=np.int16)
    

class Sm24Chunk:
    def __init__(self, data: Optional[np.ndarray] = None):
        self.data: np.ndarray = data
        
    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"sm24":
            raise ValueError("Invalid sm24 header")
        chunk_size = rdr.read_uint32()
        self.data = np.frombuffer(rdr.read(chunk_size), dtype=np.uint8)


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
            else:
                raise ValueError(f"Invalid sdta sub-chunk: {chunk_name}")


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

    def to_program(self, pdta_chunk: 'PdtaChunk', next_preset_header: 'SFPresetHeader',
                   samples: List[Sample]) -> Program:
        program = Program()
        program.lfos = []
        program.splits = []
        instrument_next_bag = pdta_chunk.pbag_chunk.preset_bags[next_preset_header.preset_bag_ndx + 1]
        instrument_gen = pdta_chunk.pgen_chunk.gen_list[instrument_next_bag.gen_ndx - 1]
        assert instrument_gen.operation == SFGeneratorEnumerator.INSTRUMENT
        instrument_id = instrument_gen.amount
        instrument = pdta_chunk.inst_chunk.instruments[instrument_id]
        instrument_next = pdta_chunk.inst_chunk.instruments[instrument_id + 1]

        for ibag_idx in range(instrument.inst_bag_ndx, instrument_next.inst_bag_ndx):
            ibag = pdta_chunk.ibag_chunk.instrument_bags[ibag_idx]
            ibag_next = pdta_chunk.ibag_chunk.instrument_bags[ibag_idx + 1]
            split = Split()
            for gen_idx in range(ibag.gen_ndx, ibag_next.gen_ndx):
                igen = pdta_chunk.igen_chunk.gen_list[gen_idx]
                if igen.operation == SFGeneratorEnumerator.SAMPLE_ID:
                    split.sample = samples[igen.amount]
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
                elif igen.operation == SFGeneratorEnumerator.PAN:
                    # amount is in increments of 0.1%, from 0% to 100% (1000)
                    split.pan = round((igen.amount * 127) / (10 * 100))
                # TODO: Add envelope, attack, decay, sustain...



class PhdrChunk:
    preset_headers: List[SFPresetHeader]

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


class SFBag:
    def __init__(self):
        self.gen_ndx = 0
        self.mod_ndx = 0

    def read(self, rdr: BinaryReader):
        self.gen_ndx = rdr.read_uint16()
        self.mod_ndx = rdr.read_uint16()


class PbagChunk:
    preset_bags: List[SFBag]

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


class SFModList:
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


class PmodChunk:
    mod_list: List[SFModList]

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"pmod":
            raise ValueError("Invalid pmod header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.mod_list = []
        while rdr.tell() < end_pos:
            mod_list = SFModList()
            mod_list.read(rdr)
            self.mod_list.append(mod_list)


class SFGenList:
    def __init__(self):
        self.operation = 0
        self.amount = 0

    @property
    def amount_signed(self):
        return (self.amount ^ 0x8000) - 0x8000

    @amount_signed.setter
    def amount_signed(self, v: int):
        self.amount = (v + 0x8000) ^ 0x8000

    @property
    def amount_range(self):
        # amount is little endian
        return self.amount & 0xFF, self.amount >> 2

    @amount_range.setter
    def amount_range(self, v: tuple):
        # amount is little endian
        self.amount = v[0] & 0xFF + v[1] << 2

    def read(self, rdr: BinaryReader):
        self.operation = rdr.read_uint16()
        self.amount = rdr.read_uint16()


class PgenChunk:
    gen_list: List[SFGenList]

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"pgen":
            raise ValueError("Invalid pgen header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.gen_list = []
        while rdr.tell() < end_pos:
            gen_list = SFGenList()
            gen_list.read(rdr)
            self.gen_list.append(gen_list)


class SFInst:
    def __init__(self):
        self.name = ""
        self.inst_bag_ndx = 0

    def read(self, rdr: BinaryReader):
        self.name = rdr.read_string(size=20, encoding="ascii")
        self.inst_bag_ndx = rdr.read_uint16()


class InstChunk:
    instruments: List[SFInst]

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


class IbagChunk:
    instrument_bags: List[SFBag]

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


class ImodChunk:
    mod_list: List[SFModList]

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"imod":
            raise ValueError("Invalid imod header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.mod_list = []
        while rdr.tell() < end_pos:
            mod_list = SFModList()
            mod_list.read(rdr)
            self.mod_list.append(mod_list)


class IgenChunk:
    gen_list: List[SFGenList]

    def read(self, rdr: BinaryReader):
        if rdr.read(4) != b"igen":
            raise ValueError("Invalid igen header")
        chunk_size = rdr.read_uint32()
        end_pos = rdr.tell() + chunk_size
        self.gen_list = []
        while rdr.tell() < end_pos:
            gen_list = SFGenList()
            gen_list.read(rdr)
            self.gen_list.append(gen_list)


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
        self.type = 0

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

    def to_sample(self, sdta_chunk: SdtaChunk) -> Sample:
        sample = Sample()
        sample.id_ = self.name
        sample.loop_beginning = self.start_loop
        sample.loop_length = self.end_loop - self.start_loop
        sample.sample_rate = self.rate
        sample.root_key = self.original_key
        sample.fine_tune = self.pitch_correction
        sample.pcm16 = sdta_chunk.smpl_chunk.data[self.start:self.end]
        return sample


class ShdrChunk:
    samples: List[SFSample]

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


class SoundFont:
    info_chunk: InfoChunk
    samples: List[Sample]
    programs: Dict[str, Program]

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

        self.samples = []
        # Construct data types
        for sf_header in pdta_chunk.shdr_chunk.samples:
            self.samples.append(sf_header.to_sample(sdta_chunk))
        print("DONE")
