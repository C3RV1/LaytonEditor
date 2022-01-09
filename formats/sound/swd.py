from .soundtypes import *
from formats.binary import BinaryReader, BinaryWriter, SEEK_CUR
from formats.filesystem import FileFormat


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

    def read(self, br: BinaryReader):
        br.seek(0)
        self.magic = br.read(4)
        if self.magic != b"swdl":
            raise ValueError("SWDHeader does not start with magic value")
        br.read_uint32()  # 0
        self.file_length = br.read_uint32()
        self.version = br.read_uint16()
        if self.version != 0x415:
            raise ValueError("SMDHeader does not have correct version")
        self.is_sample_bank = br.read_bool()
        self.group = br.read_uint8()
        # 8 bytes of 0
        br.read_uint32()
        br.read_uint32()
        self.year = br.read_uint16()
        self.month = br.read_uint8()
        self.day = br.read_uint8()
        self.hour = br.read_uint8()
        self.minute = br.read_uint8()
        self.second = br.read_uint8()
        self.centisecond = br.read_uint8()
        self.file_name = br.read_string(16, encoding=None, pad=b"\xAA")
        self.unk10 = br.read_uint32()
        # 8 bytes of 0
        br.read_uint32()
        br.read_uint32()
        self.unk13 = br.read_uint32()


class SWDSections:
    pass


class SWDL(FileFormat):
    swd_header: SWDHeader

    def read_stream(self, stream):
        if isinstance(stream, BinaryReader):
            rdr = stream
        else:
            rdr = BinaryReader(stream)
        self.swd_header = SWDHeader()
        self.swd_header.read(rdr)

    def write_stream(self, stream):
        if isinstance(stream, BinaryWriter):
            wtr = stream
        else:
            wtr = BinaryWriter(stream)


def swd_read_sections(stream) -> Dict[str, Tuple[int, int]]:
    rdr = stream if isinstance(stream, BinaryReader) else BinaryReader(stream)
    rdr.seek(0x50)  # goto the start of the sections
    sections: Dict[str, Tuple[int, int]] = {}  # dict of the name of the section and then the start and length.
    while rdr.tell() < len(rdr):
        header_start = rdr.tell()
        name = rdr.read_string(4)
        rdr.seek(4, SEEK_CUR)
        header_length = rdr.read_uint32()
        start = header_start + header_length
        length = rdr.read_uint32()
        sections[name] = (start, length)
        rdr.seek(start + length)
        rdr.align(0x10)
    return sections


def swd_read_samples(stream) -> Dict[int, Sample]:
    rdr = stream if isinstance(stream, BinaryReader) else BinaryReader(stream)
    rdr.seek(0x46)
    n_wavi_slots = rdr.read_uint16()
    sections = swd_read_sections(stream)
    wavi_offset, wavi_len = sections["wavi"]
    pcmd_offset, pcmd_len = sections["pcmd"]
    samples: Dict[int, Sample] = {}
    rdr.seek(wavi_offset)
    for sample_index, sample_info_offset in enumerate(rdr.read_uint16_array(n_wavi_slots)):
        if not sample_info_offset:
            continue
        rdr.seek(wavi_offset + sample_info_offset + 0x20)
        samplerate = rdr.read_uint32()
        adpcm_pos = rdr.read_uint32()
        adpcm_loop_position = rdr.read_uint32() * 4
        adpcm_loop_lenght = rdr.read_uint32() * 4
        adpcm_lenght = (adpcm_loop_position + adpcm_loop_lenght)

        rdr.seek(pcmd_offset + adpcm_pos)
        samples[sample_index] = Sample(samplerate, rdr.read(adpcm_lenght))

    return samples


def swd_read_samples_info(stream) -> Dict[int, SampleInfo]:
    rdr = stream if isinstance(stream, BinaryReader) else BinaryReader(stream)
    rdr.seek(0x46)
    n_wavi_slots = rdr.read_uint16()
    sections = swd_read_sections(stream)
    wavi_offset, wavi_len = sections["wavi"]
    samples_info: Dict[int, SampleInfo] = {}
    rdr.seek(wavi_offset)
    for sample_index, sample_info_section_offset in enumerate(rdr.read_uint16_array(n_wavi_slots)):
        if not sample_info_section_offset:
            continue
        sample_info_offset = wavi_offset + sample_info_section_offset
        rdr.seek(sample_info_offset + 0x04)
        tuning = rdr.read_int8()
        rdr.seek(sample_info_offset + 0x15)
        loop_enabled = rdr.read_bool()
        rdr.seek(sample_info_offset + 0x28)
        loop = rdr.read_uint32() * 8 - 9
        samples_info[sample_index] = SampleInfo(sample_index, loop_enabled, loop, tuning)
    return samples_info


def swd_read_presets(stream, samples_info) -> Dict[int, Preset]:
    rdr = stream if isinstance(stream, BinaryReader) else BinaryReader(stream)
    rdr.seek(0x48)
    n_prgi_slots = rdr.read_uint16()
    sections = swd_read_sections(stream)
    prgi_offset, prgi_len = sections["prgi"]
    presets: Dict[int, Preset] = {}
    rdr.seek(prgi_offset)
    for preset_index, preset_section_offset in enumerate(rdr.read_uint16_array(n_prgi_slots)):
        if not preset_section_offset:
            continue
        preset_offset = prgi_offset + preset_section_offset
        rdr.seek(preset_offset)
        assert rdr.read_uint16() == preset_index
        n_splits = rdr.read_uint16()
        rdr.seek(preset_offset + 0xb)
        n_lfos = rdr.read_uint8()
        rdr.seek(preset_offset + 0x10)
        lfos = []
        for lfo_index in range(n_lfos):
            lfo_offset = rdr.tell()
            rdr.seek(lfo_offset + 2)
            destination = LFODestination(rdr.read_int8())
            wave_shape = LFOWaveShape(rdr.read_int8())
            rate = rdr.read_uint16()
            depth = rdr.read_uint16()
            delay = rdr.read_uint16()
            lfos.append(LFO(destination, wave_shape, rate, depth, delay))
        rdr.seek(preset_offset + 0x10 + 0x10 * n_lfos + 0x10)
        splits = []
        for split_index in range(n_splits):
            split_offset = rdr.tell()
            rdr.seek(split_offset + 0x04)
            lowkey = rdr.read_int8()
            highkey = rdr.read_int8()
            rdr.seek(split_offset + 0x12)
            sample_index = rdr.read_uint16()
            tuning = rdr.read_int8()
            rdr.seek(split_offset + 0x16)
            rootkey = rdr.read_int8()
            rdr.seek(split_offset + 0x30)
            splits.append(
                SplitEntry(highkey, lowkey, samples_info[sample_index], tuning, rootkey))
        presets[preset_index] = Preset(splits, lfos)
    return presets


def swd_read_samplebank(stream) -> SampleBank:
    rdr = stream if isinstance(stream, BinaryReader) else BinaryReader(stream)
    rdr.seek(0x0c)
    assert rdr.read_uint16() == 0x0415  # Correct version
    assert rdr.read_bool()  # This is a SampleBank
    group = rdr.read_uint8()
    rdr.seek(0x20)
    label = rdr.read_string(16, pad=b"\xaa")
    samples = swd_read_samples(stream)
    return SampleBank(label, group, samples)


def swd_read_presetbank(stream) -> PresetBank:
    rdr = stream if isinstance(stream, BinaryReader) else BinaryReader(stream)
    rdr.seek(0x0c)
    assert rdr.read_uint16() == 0x0415  # Correct version
    assert not rdr.read_bool()  # This is not a SampleBank
    group = rdr.read_ubyte()

    rdr.seek(0x20)
    label = rdr.read_string(16, pad=b"\xaa")

    samples_info = swd_read_samples_info(stream)
    presets = swd_read_presets(stream, samples_info)
    return PresetBank(label, group, presets, samples_info)
