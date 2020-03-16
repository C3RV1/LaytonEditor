from LaytonLib.binary import *
from LaytonLib.sound.vars import *


def SWD_FindChunck(rdr: BinaryReader, chunk):
    c = rdr.c
    rdr.c = 0
    while rdr.c < len(rdr.data):
        string = rdr.readChars(4)
        if string == chunk:
            offset = rdr.c - 4
            rdr.c = c
            return offset
    return -1


class SWD_SplitEntry:
    def __init__(self):
        self.ID = 0
        self.Unk0x2 = 2
        self.Unk0x3 = 0
        self.LowKey = 0
        self.HighKey = 0
        self.LowKey2 = 0
        self.HighKey2 = 0
        self.LowVelocity = 0
        self.HighVelocity = 127
        self.LowVelocity2 = 0
        self.HighVelocity2 = 127
        self.SampleID = 0
        self.FineTuning = 0
        self.CourseTuning = 0
        self.SampleRootKey = 0
        self.SampleTranspose = 0
        self.SampleVolume = 127
        self.SamplePanpot = 64
        self.KeyGroupID = 0
        self.EnvelopeOn = 1
        self.EnvelopeMultiplier = 1
        self.Unk0x22 = 1
        self.Unk0x23 = 3
        self.Unk0x24 = 65283
        self.Unk0x26 = 65535
        self.AttackVolume = 0
        self.Attack = 0
        self.Decay = 0
        self.Sustain = 127
        self.Hold = 0
        self.Decay2 = 127
        self.Release = 40

    def from_reader(self, rdr: BinaryReader):
        rdr.c += 1
        self.ID = rdr.readU8()
        self.Unk0x2 = rdr.readU8()
        self.Unk0x3 = rdr.readU8()
        self.LowKey = rdr.readS8()
        self.HighKey = rdr.readS8()
        self.LowKey2 = rdr.readS8()
        self.HighKey2 = rdr.readS8()
        self.LowVelocity = rdr.readS8()
        self.HighVelocity = rdr.readS8()
        self.LowVelocity2 = rdr.readS8()
        self.HighVelocity2 = rdr.readS8()
        rdr.c += 4 + 2
        self.SampleID = rdr.readU16()
        self.FineTuning = rdr.readS8()
        self.CourseTuning = rdr.readS8()
        self.SampleRootKey = rdr.readS8()
        self.SampleTranspose = rdr.readS8()
        self.SampleVolume = rdr.readS8()
        self.SamplePanpot = rdr.readS8()
        self.KeyGroupID = rdr.readU8()
        rdr.c += 1 + 2 + 2
        self.EnvelopeOn = rdr.readU8()
        self.EnvelopeMultiplier = rdr.readU8()
        self.Unk0x22 = rdr.readU8()
        self.Unk0x23 = rdr.readU8()
        self.Unk0x24 = rdr.readU16()
        self.Unk0x26 = rdr.readU16()
        self.AttackVolume = rdr.readS8()
        self.Attack = rdr.readS8()
        self.Decay = rdr.readS8()
        self.Sustain = rdr.readS8()
        self.Hold = rdr.readS8()
        self.Decay2 = rdr.readS8()
        self.Release = rdr.readS8()
        rdr.c += 1

    def to_writer(self, wtr: BinaryWriter):
        wtr.writeU8(0)
        wtr.writeU8(self.ID)
        wtr.writeU8(self.Unk0x2)
        wtr.writeU8(self.Unk0x3)
        wtr.writeS8(self.LowKey)
        wtr.writeS8(self.HighKey)
        wtr.writeS8(self.LowKey2)
        wtr.writeS8(self.HighKey2)
        wtr.writeS8(self.LowVelocity)
        wtr.writeS8(self.HighVelocity)
        wtr.writeS8(self.LowVelocity2)
        wtr.writeS8(self.HighVelocity2)
        wtr.writeU32(0)
        wtr.writeU16(0)
        wtr.writeU16(self.SampleID)
        wtr.writeS8(self.FineTuning)
        wtr.writeS8(self.CourseTuning)
        wtr.writeS8(self.SampleRootKey)
        wtr.writeS8(self.SampleTranspose)
        wtr.writeS8(self.SampleVolume)
        wtr.writeS8(self.SamplePanpot)
        wtr.writeU8(self.KeyGroupID)
        wtr.writeU8(0x02)
        wtr.writeU16(0x0000)
        wtr.writeU16(0)
        wtr.writeU8(self.EnvelopeOn)
        wtr.writeU8(self.EnvelopeMultiplier)
        wtr.writeU8(self.Unk0x22)
        wtr.writeU8(self.Unk0x23)
        wtr.writeU16(self.Unk0x24)
        wtr.writeU16(self.Unk0x26)
        wtr.writeS8(self.AttackVolume)
        wtr.writeS8(self.Attack)
        wtr.writeS8(self.Decay)
        wtr.writeS8(self.Sustain)
        wtr.writeS8(self.Hold)
        wtr.writeS8(self.Decay2)
        wtr.writeS8(self.Release)
        wtr.writeU8(0xff)


class SWD_ProgramInfo:
    def __init__(self):
        self.ID = 0
        self.Volume = 127
        self.Panpot = 64
        self.FLOInfos = []
        self.SplitEntries = []

    def from_reader(self, rdr: BinaryReader):
        self.ID = rdr.readU16()
        nbsplits = rdr.readU16()
        self.SplitEntries = [SWD_SplitEntry() for _ in range(nbsplits)]
        self.Volume = rdr.readS8()
        self.Panpot = rdr.readS8()
        rdr.c += 1 + 1 + 2 + 1
        nblfos = rdr.readU8()
        self.FLOInfos = [SWD_LFOInfo() for _ in range(nblfos)]
        rdr.c += 1 + 1 + 1 + 1
        for flo in self.FLOInfos:
            flo.from_reader(rdr)
        rdr.c += 16
        for i in range(nbsplits):
            self.SplitEntries[i].from_reader(rdr)

    def to_writer(self, wtr):
        wtr.writeU16(self.ID)
        wtr.writeU16(len(self.SplitEntries))
        wtr.writeU8(self.Volume)
        wtr.writeU8(self.Panpot)
        wtr.writeU8(0x00)
        wtr.writeU8(0x0F)
        wtr.writeU16(0x200)
        wtr.writeU8(0x00)
        wtr.writeU8(len(self.FLOInfos))
        wtr.writeU8(0x0)
        wtr.writeU8(0x0)
        wtr.writeU8(0x0)
        wtr.writeU8(0x0)
        for flo in self.FLOInfos:
            flo.to_writer(wtr=wtr)
        for i in range(16):
            wtr.writeU8(0x0)
        for split in self.SplitEntries:
            split.to_writer(wtr)

    def isactive(self):
        return len(self.SplitEntries) != 0

    def estimate_lenght(self):
        wtr = BinaryWriter()
        self.to_writer(wtr)
        return len(wtr.data)


class SWD_LFOInfo:
    def __init__(self):
        self.data = bytes(16)
        self.unk0x0 = 0
        self.unk0x1 = 0
        self.dest = 0
        self.wschape = 0
        self.rate = 0
        self.unk0x6 = 0
        self.depth = 0
        self.delay = 0
        self.fadeout = 0
        self.unk0xe = 0

    def from_reader(self, rdr: BinaryReader):
        self.data = rdr.readBytes(16)

    def to_writer(self, wtr: BinaryWriter):
        wtr.write(self.data)


class SWD_WavInfo:
    def __init__(self):
        self.ID = 0
        self.FineTuning = 0
        self.CourseTuning = 0
        self.RootKey = 60
        self.Transpose = 0
        self.Volume = 127
        self.Panpot = 64
        self.Version = 1024
        self.Sampleformat = "ADPCM"
        self.Loop = 0
        self.SamplesPer32Bits = 8
        self.BitDepth = 4
        self.Unk0 = 1
        self.SampleRate = 0
        self.SampleOffset = 0
        self.LoopStart = 0
        self.LoopEnd = 0
        self.EnvOn = 1
        self.EnvMult = 1
        self.AttackVolume = 0
        self.Attack = 0
        self.Decay = 0
        self.Sustain = 127
        self.Hold = 0
        self.Decay2 = 127
        self.Release = 40

    def from_reader(self, rdr: BinaryReader):
        rdr.c += 2
        self.ID = rdr.readU16()
        self.FineTuning = rdr.readS8()
        self.CourseTuning = rdr.readS8()
        self.RootKey = rdr.readU8()
        self.Transpose = rdr.readS8()
        self.Volume = rdr.readU8()
        self.Panpot = rdr.readS8()
        rdr.c += 6
        self.Version = rdr.readU16()
        self.Sampleformat = SampleFormats[rdr.readU16()]
        rdr.c += 1
        self.Loop = rdr.readU8()
        rdr.c += 1
        self.SamplesPer32Bits = rdr.readU8()
        rdr.c += 1
        self.BitDepth = rdr.readU8()
        rdr.c += 2
        self.Unk0 = rdr.readU32()
        self.SampleRate = rdr.readU32()
        self.SampleOffset = rdr.readU32()
        self.LoopStart = rdr.readU32()
        self.LoopEnd = rdr.readU32()
        self.EnvOn = rdr.readU8()
        self.EnvMult = rdr.readU8()
        rdr.c += 6
        self.AttackVolume = rdr.readU8()
        self.Attack = rdr.readU8()
        self.Decay = rdr.readU8()
        self.Sustain = rdr.readU8()
        self.Hold = rdr.readU8()
        self.Decay2 = rdr.readU8()
        self.Release = rdr.readU8()
        rdr.c += 1

    def to_writer(self, wtr: BinaryWriter):
        wtr.writeU16(0xAA01)
        wtr.writeU16(self.ID)
        wtr.writeS8(self.FineTuning)
        wtr.writeS8(self.CourseTuning)
        wtr.writeS8(self.RootKey)
        wtr.writeS8(self.Transpose)
        wtr.writeS8(self.Volume)
        wtr.writeS8(self.Panpot)
        wtr.writeU8(0)
        wtr.writeU8(2)
        wtr.writeU16(0)
        wtr.writeU16(0xaaaa)
        wtr.writeU16(0x415)
        wtr.writeU16(0x0200)
        wtr.writeU8(9)
        wtr.writeU8(self.Loop)
        wtr.writeU16(0x0801)
        wtr.writeU16(0x0400)
        wtr.writeU16(0x0101)
        wtr.writeU32(self.Unk0)
        wtr.writeU32(self.SampleRate)
        wtr.writeU32(self.SampleOffset)
        wtr.writeU32(self.LoopStart)
        wtr.writeU32(self.LoopEnd)
        wtr.writeU8(self.EnvOn)
        wtr.writeU8(self.EnvMult)
        wtr.writeU8(1)
        wtr.writeU8(3)
        wtr.writeU16(0xff03)
        wtr.writeU16(0xffff)
        wtr.writeS8(self.AttackVolume)
        wtr.writeS8(self.Attack)
        wtr.writeS8(self.Decay)
        wtr.writeS8(self.Sustain)
        wtr.writeS8(self.Hold)
        wtr.writeS8(self.Decay2)
        wtr.writeS8(self.Release)
        wtr.writeU8(0xff)


class SWD_SampleBlock:
    def __init__(self):
        self.WavInfo = SWD_WavInfo()
        self.Data = b""


class SWD_ProgramBank:
    def __init__(self):
        self.ProgramInfos = []
        self.Keygroups = []

    def ReadPrograms(self, rdr: BinaryReader, n_prgi_slots):
        chunckoffset = SWD_FindChunck(rdr, "prgi")
        if chunckoffset == -1:
            return
        else:
            chunckoffset += 0x10
            programInfos = [SWD_ProgramInfo() for _ in range(n_prgi_slots)]
            for i in range(n_prgi_slots):
                offset = rdr.readU16at(chunckoffset + (2 * i))
                if offset != 0:
                    rdr.c = offset + chunckoffset
                    programInfos[i].from_reader(rdr)
            self.ProgramInfos = programInfos

        chunckoffset = SWD_FindChunck(rdr, "kgrp")
        if chunckoffset == -1:
            return
        rdr.c = chunckoffset + 0xC
        chunklenght = rdr.readU32()
        self.Keygroups = [SWD_KeyGroup() for _ in range(chunklenght // 8)]
        for i in range(chunklenght // 8):
            self.Keygroups[i].from_reader(rdr)

    def WritePrgiChunk(self, wtr: BinaryWriter):
        if len(self.ProgramInfos) == 0:
            return
        chunk = BinaryWriter()
        offset = len(self.ProgramInfos) * 2
        if offset % 16 != 0:
            offset += 16 - (offset % 16)
        for programinfo in self.ProgramInfos:
            programinfo: SWD_ProgramInfo
            if programinfo.isactive():
                chunk.writeU16(offset)
                offset += programinfo.estimate_lenght()
            else:
                chunk.writeU16(0)
                pass
        chunk.align(16)
        for programinfo in self.ProgramInfos:
            if programinfo.isactive():
                programinfo: SWD_ProgramInfo
                programinfo.to_writer(chunk)

        wtr.write("prgi")
        wtr.writeU16(0)
        wtr.writeU16(0x415)
        wtr.writeU32(0x10)
        wtr.writeU32(len(chunk.data))
        wtr.write(chunk.data)

    def WriteKrgpChunk(self, wtr: BinaryWriter):
        if len(self.Keygroups) == 0:
            return

        chunk = BinaryWriter()
        for (keygroup) in self.Keygroups:
            keygroup: SWD_KeyGroup
            keygroup.to_writer(chunk)
        if len(chunk.data) % 16 != 0:
            for i in range(8):
                chunk.writeU8(0)

        wtr.write("kgrp")
        wtr.writeU16(0)
        wtr.writeU16(0x415)
        wtr.writeU32(0x10)
        wtr.writeU32(len(chunk.data))
        wtr.write(chunk.data)


class SWD_KeyGroup:
    def __init__(self):
        self.ID = 0
        self.Poly = 0
        self.Priority = 0
        self.Low = 0
        self.High = 0
        self.Unk0x6 = 0
        self.Unk0x7 = 0

    def from_reader(self, rdr: BinaryReader):
        self.ID = rdr.readU16()
        self.Poly = rdr.readU8()
        self.Priority = rdr.readU8()
        self.Low = rdr.readU8()
        self.High = rdr.readU8()
        self.Unk0x6 = rdr.readU8()
        self.Unk0x7 = rdr.readU8()

    def to_writer(self, wtr: BinaryWriter):
        wtr.writeU16(self.ID)
        wtr.writeU8(self.Poly)
        wtr.writeU8(self.Priority)
        wtr.writeU8(self.Low)
        wtr.writeU8(self.High)
        wtr.writeU8(self.Unk0x6)
        wtr.writeU8(self.Unk0x7)


class SWD_Parser:
    def __init__(self):
        self.Programs = SWD_ProgramBank()
        self.Samples = []
        self.is_mainbank = 0
        self.group = 0
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.centisecond = 0
        self.label = ""
        self.len_pcmd = 0
        self.n_wavi_slots = 0
        self.n_pgri_slots = 0
        self.unk0x4a = 0
        self.len_wavi = 0

    def from_data(self, data: bytes):
        self.__init__()  # Reset
        rdr = BinaryReader(data)
        MagicN = rdr.readChars(4)
        if MagicN != "swdl":
            raise Exception("Tried to parse a non-swdl file as swdl")
        rdr.c += 4 + 4  # Zeros and Filelenght
        Version = rdr.readU16()
        if Version != 0x415:
            raise NotImplementedError("Version ID {Version} not implemented")

        # Header
        self.is_mainbank = rdr.readU8()
        self.group = rdr.readU8()
        rdr.c += 4 + 4
        self.year = rdr.readU16()
        self.month = rdr.readU8()
        self.day = rdr.readU8()
        self.hour = rdr.readU8()
        self.minute = rdr.readU8()
        self.second = rdr.readU8()
        self.centisecond = rdr.readU8()
        self.label = rdr.readChars(16)
        rdr.c += 4 + 4 + 4 + 4
        self.len_pcmd = rdr.readU32()
        rdr.c += 2
        self.n_wavi_slots = rdr.readU16()
        self.n_pgri_slots = rdr.readU16()
        self.unk0x4a = rdr.readU16()
        self.len_wavi = rdr.readU32()

        self.Programs.ReadPrograms(rdr, self.n_pgri_slots)
        # if self.len_pcmd != 0 and (self.len_pcmd & 0xFFFF0000) != 0xAAAA0000:
        self.read_samples(rdr)

    def to_data(self):
        header = BinaryWriter()
        header.writeU8(self.is_mainbank)
        header.writeU8(self.group)
        header.writeU32(0)
        header.writeU32(0)
        header.writeU16(self.year)
        header.writeU8(self.month)
        header.writeU8(self.day)
        header.writeU8(self.hour)
        header.writeU8(self.minute)
        header.writeU8(self.second)
        header.writeU8(self.centisecond)
        header.writeChars(self.label, 16, pad=0xAA)
        header.writeU32(0xaaaaaa00)
        header.writeZeros(8)
        header.writeU32(0x10)
        header.writeU32(self.len_pcmd)
        header.writeZeros(2)
        header.writeU16(self.n_wavi_slots)
        header.writeU16(self.n_pgri_slots)
        header.writeU16(self.unk0x4a)
        header.writeU32(self.len_wavi)
        wavi = BinaryWriter()
        if self.Samples:
            self.write_samples_wavi(wavi)
        prgi = BinaryWriter()
        if self.Programs.ProgramInfos:
            self.Programs.WritePrgiChunk(prgi)
        kgrp = BinaryWriter()
        if self.Programs.Keygroups:
            self.Programs.WriteKrgpChunk(kgrp)
        pcmd = BinaryWriter()
        if self.len_pcmd != 0 and (self.len_pcmd & 0xFFFF0000) != 0xAAAA0000:
            self.write_samples_pcmd(pcmd)

        eod = BinaryWriter()
        eod.write("eod\x20")
        eod.writeU16(0)
        eod.writeU16(0x415)
        eod.writeU32(0x10)
        eod.writeU32(0)

        filelen = len(header) + len(wavi) + len(prgi) + len(kgrp) + len(pcmd) + len(eod) + 0xe

        wtr = BinaryWriter()
        wtr.write("swdl")
        wtr.writeZeros(4)
        wtr.writeU32(filelen)
        wtr.writeU16(0x415)
        wtr.write(header.data)
        wtr.write(wavi.data)
        wtr.write(prgi.data)
        wtr.write(kgrp.data)
        wtr.write(pcmd.data)
        wtr.write(eod.data)
        return wtr.data

    def read_samples(self, rdr: BinaryReader):
        wavioffset = SWD_FindChunck(rdr, "wavi")
        pcmdoffset = SWD_FindChunck(rdr, "pcmd")
        if wavioffset == -1:
            raise Exception("Invalid data: WAVI chunck not found")
        wavioffset += 0x10
        if pcmdoffset == -1:
            self.is_mainbank = False
            samples = [SWD_SampleBlock() for _ in range(self.n_wavi_slots)]
            for i in range(self.n_wavi_slots):
                offset = rdr.readU16at(wavioffset + (2 * i))
                if offset != 0:
                    rdr.c = offset + wavioffset
                    wavInfo = SWD_WavInfo()
                    wavInfo.from_reader(rdr)
                    samples[i].WavInfo = wavInfo
            self.Samples = samples
            return
        pcmdoffset += 0x10
        samples = [SWD_SampleBlock() for _ in range(self.n_wavi_slots)]
        for i in range(self.n_wavi_slots):
            offset = rdr.readU16at(wavioffset + (2 * i))
            if offset != 0:
                rdr.c = offset + wavioffset
                wavInfo = SWD_WavInfo()
                wavInfo.from_reader(rdr)
                samples[i].WavInfo = wavInfo
                samples[i].Data = rdr.readBytesat((wavInfo.LoopStart + wavInfo.LoopEnd) * 4,
                                                  pcmdoffset + wavInfo.SampleOffset)
        self.Samples = samples

    def write_samples_wavi(self, wtr: BinaryWriter):
        chunk = BinaryWriter()
        offset = 2 * len(self.Samples)
        if offset % 16 != 0:
            offset += 16 - (offset % 16)
        for wav in self.Samples:
            if wav.WavInfo.SampleRate:
                chunk.writeU16(offset)
                offset += 0x40
            else:
                chunk.writeS16(0)
        chunk.align(16, pad=0xaa)
        for wav in self.Samples:
            wav: SWD_SampleBlock
            if wav.WavInfo.SampleRate:
                wav.WavInfo.to_writer(chunk)

        wtr.write("wavi")
        wtr.writeU16(0)
        wtr.writeU16(0x415)
        wtr.writeU32(0x10)
        wtr.writeU32(len(chunk.data))
        wtr.write(chunk.data)

    def write_samples_pcmd(self, wtr: BinaryWriter):
        chunk = BinaryWriter()
        for wav in self.Samples:
            wav: SWD_SampleBlock
            chunk.write(wav.Data)

        wtr.write("pcmd")
        wtr.writeU16(0)
        wtr.writeU16(0x415)
        wtr.writeU32(0x10)
        wtr.writeU32(len(chunk.data))
        wtr.write(chunk.data)
        wtr.align(16)

    @classmethod
    def new_from_data(cls, data):
        self = cls()
        self.from_data(data)
        return self
