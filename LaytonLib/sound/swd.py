from LaytonLib.sound.swd_parser import *
from LaytonLib.sound.adpcm import *
from scipy.io import wavfile
import os.path
from string import Template
from time import localtime
from LaytonLib.sound.vars import *


# Higher level sample class, only had that what's neccesary/used in pl2
class Sample:
    def __init__(self, index, adpcm=b"", samplerate=44100, loop=0, fine_tune=None, course_tune=None):
        self.index = index
        self.adpcm = adpcm
        self.samplerate = samplerate
        self.loop = loop  # off when 0
        self.fine_tune = fine_tune
        self.course_tune = course_tune

    @property
    def pcm16(self):
        return ADPCMtoPCM16(self.adpcm)

    @pcm16.setter
    def pcm16(self, value):
        self.adpcm = PCM16toADPCM(value)

    @property
    def tuning(self):  # tuning in simitones
        return self.course_tune + self.fine_tune / 100

    @tuning.setter
    def tuning(self, value):
        self.course_tune = int(value)
        self.fine_tune = int(value * 100 % 100)

    @property
    def samplerate_tuned(self):
        return int(self.samplerate * 2 ** ((self.tuning) / 12))

    @samplerate_tuned.setter
    def samplerate_tuned(self, value):
        self.samplerate = value / 2 ** ((self.tuning) / 12)

    def export_wav(self, filename, tuned=False):
        wavfile.write(filename, self.samplerate_tuned if tuned else self.samplerate, self.pcm16)

    def import_wav(self, filename, tuned=False, reset_tuning=False):
        wav = wavfile.read(filename)
        if wav[1].dtype != np.int16:
            raise NotImplementedError("Only PCM16 encoded wavfiles can be used")
        if tuned:
            self.samplerate_tuned, self.pcm16 = wav
        else:
            self.samplerate, self.pcm16 = wav
            if reset_tuning:
                self.fine_tune = 0
                self.course_tune = 0

    @classmethod
    def from_parsersample(cls, sample: SWD_SampleBlock):
        if not sample.Data:  # sample must have adpcm
            return None
        self = cls(sample.WavInfo.ID, sample.Data, sample.WavInfo.SampleRate,
                   sample.WavInfo.Loop * (sample.WavInfo.LoopStart * 8 - 9),
                   sample.WavInfo.FineTuning, sample.WavInfo.CourseTuning)
        return self

    def to_parsersample(self, dataoffset):
        ps = SWD_SampleBlock()
        # some values are already set to their defaults in the class
        ps.Data = self.adpcm
        ps.WavInfo.ID = self.index
        ps.WavInfo.CourseTuning = self.course_tune
        ps.WavInfo.FineTuning = self.fine_tune
        ps.WavInfo.Loop = 1 if self.loop else 0
        ps.WavInfo.SampleRate = self.samplerate
        ps.WavInfo.SampleOffset = dataoffset
        if (self.loop + 9) % 8 != 0 and self.loop:
            print(f"Warning: Loop {self.index} cannot accurately be represented and might sound off. \n",
                  "To avoid this make sure the looppoint + 1 is devisible by 8,\n" ""
                  "you can do this by inserting 0s at the beginning of the sample")
        ps.WavInfo.LoopStart = (self.loop + 9) // 8 if self.loop else 1
        ps.WavInfo.LoopEnd = (len(self.adpcm) - max(1, (self.loop + 9) // 2)) // 4
        return ps


class SplitEntry:
    def __init__(self, index, unk0x2, highkey, lowkey, sample_index, fine_tuning, course_tuning, rootkey,
                 keygroup_index, attack_volume, attack, decay, sustain, hold, decay2, release):
        self.index = index
        self.unk0x2 = unk0x2
        self.highkey = highkey
        self.lowkey = lowkey
        self.sample_index = sample_index
        self.fine_tuning = fine_tuning
        self.course_tuning = course_tuning
        self.rootkey = rootkey
        self.keygroup_index = keygroup_index

        self.attack_volume = attack_volume
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.hold = hold
        self.decay2 = decay2
        self.release = release

    @classmethod
    def from_parsersplitentry(cls, parsersplitentry: SWD_SplitEntry):
        self = cls(parsersplitentry.ID, parsersplitentry.Unk0x3,
                   parsersplitentry.HighKey, parsersplitentry.LowKey,
                   parsersplitentry.SampleID, parsersplitentry.FineTuning,
                   parsersplitentry.CourseTuning, parsersplitentry.SampleRootKey,
                   parsersplitentry.KeyGroupID, parsersplitentry.AttackVolume,
                   parsersplitentry.Attack, parsersplitentry.Decay,
                   parsersplitentry.Sustain, parsersplitentry.Hold,
                   parsersplitentry.Decay2, parsersplitentry.Release)
        return self

    def to_parsersplitentry(self):
        pse = SWD_SplitEntry()
        pse.ID = self.index
        pse.Unk0x3 = self.unk0x2
        pse.LowKey = self.lowkey
        pse.LowKey2 = self.lowkey
        pse.HighKey = self.highkey
        pse.HighKey2 = self.highkey
        pse.SampleID = self.sample_index
        pse.FineTuning = self.fine_tuning
        pse.CourseTuning = self.course_tuning
        pse.SampleRootKey = self.rootkey
        pse.SampleTranspose = 60 - self.rootkey
        pse.KeyGroupID = self.keygroup_index

        pse.AttackVolume = self.attack_volume
        pse.Attack = self.attack
        pse.Decay = self.decay
        pse.Sustain = self.sustain
        pse.Hold = self.hold
        pse.Decay2 = self.decay2
        pse.Release = self.release
        return pse

    def to_sfzregion(self, sample: Sample):
        ret = "<region>\n"
        ret += f"sample=samples\\Sample {self.sample_index}.wav\n"

        ret += f"lokey={self.lowkey - self.course_tuning} " + \
               f"hikey={self.highkey - self.course_tuning}\n"
        ret += f"pitch_keycenter={self.rootkey - self.course_tuning}\n"

        ret += f"ampeg_start={self.attack_volume / 1.27}\n"
        ret += f"ampeg_attack={Duration16[self.attack] / 1000.}\n"
        ret += f"ampeg_release={Duration16[self.release] / 1000.}\n"
        ret += f"ampeg_hold={Duration16[self.hold] / 1000.}\n"

        if self.decay != 0 and self.decay2 != 0 and self.decay2 != 127:
            if self.decay == 127:
                ret += f"ampeg_decay={Duration16[self.decay2] / 1000.}\n"
            elif self.sustain == 0:
                ret += f"ampeg_decay={Duration16[self.decay] / 1000.}\n"
            else:
                ret += f"ampeg_decay={(Duration16[self.decay] + Duration16[self.decay2]) / 1000.}\n"
            ret += f"ampeg_sustain={self.sustain / 1.27}\n"
        elif self.decay != 0:
            ret += f"ampeg_decay={Duration16[self.decay] / 1000.}\n"
            ret += f"ampeg_sustain={self.sustain / 1.27}\n"
        else:
            if self.decay2 != 127:
                ret += f"ampeg_decay={Duration16[self.decay2] / 1000.}\n"
                ret += f"ampeg_sustain={self.sustain / 1.27}\n"
            else:
                ret += f"ampeg_sustain=0\n"

        ret += f"loop_start={sample.loop}\n"
        ret += f"loop_mode=loop_continuous\n" if sample.loop else f"loop_mode=one_shot\n"
        ret += f"tune={self.fine_tuning}\n"
        print(self.rootkey, self.course_tuning, self.fine_tuning, self.unk0x2)
        ret += f"\n"
        return ret


class LFO:
    def __init__(self, data_wiparg):
        self.data = data_wiparg

    @classmethod
    def from_parserlfo(cls, parserlfo: SWD_LFOInfo):
        return cls(parserlfo.data)

    def to_parserlfo(self):
        pi = SWD_LFOInfo()
        pi.data = self.data
        return pi


class ProgramInfo:
    def __init__(self, index, splitentries, lfos):
        self.index = index
        if type(splitentries) == int:
            self.splitentries = np.ndarray((splitentries,), SplitEntry)
        else:
            self.splitentries = splitentries
        if type(lfos) == int:
            self.lfos = np.ndarray((lfos,), LFO)
        else:
            self.lfos = lfos

    @classmethod
    def from_parserprograminfo(cls, parserprograminfo: SWD_ProgramInfo):
        if len(parserprograminfo.SplitEntries) == 0:
            return None
        self = cls(parserprograminfo.ID, len(parserprograminfo.SplitEntries), len(parserprograminfo.FLOInfos))
        for i, s in enumerate(parserprograminfo.SplitEntries):
            self.splitentries[i] = SplitEntry.from_parsersplitentry(s)
        for i, l in enumerate(parserprograminfo.FLOInfos):
            self.lfos[i] = LFO.from_parserlfo(l)
        return self

    def to_parserprograminfo(self):
        pi = SWD_ProgramInfo()
        pi.ID = self.index
        pi.FLOInfos = [x.to_parserlfo() if x else SWD_LFOInfo() for x in self.lfos]
        pi.SplitEntries = [x.to_parsersplitentry() if x else SWD_SplitEntry() for x in self.splitentries]
        return pi

    @property
    def active_splitentries(self):
        return self.splitentries[self.splitentries != None]

    def to_sfz(self, filename, mainbank, expand=True):
        print(self.index)
        with open(filename, "w+") as file:
            # file.writelines(f"<group>\n")
            # TODO: Write LFO Data
            for s in self.splitentries:
                s: SplitEntry
                file.write(s.to_sfzregion(mainbank.samples[s.sample_index]))
        print()


class Keygroup:
    def __init__(self, index, poly, priority, low, high):
        self.index = index
        self.poly = poly
        self.priority = priority
        self.low = low
        self.high = high

    @classmethod
    def from_parserkeygroup(cls, parserkeygroup: SWD_KeyGroup):
        if parserkeygroup.ID == 43690:  # 0xaaaa: padding/inactive
            return None
        return cls(parserkeygroup.ID, parserkeygroup.Poly, parserkeygroup.Priority,
                   parserkeygroup.Low, parserkeygroup.High)

    def to_parserkeygroup(self):
        kg = SWD_KeyGroup()
        kg.ID = self.index
        kg.Poly = self.poly
        kg.Priority = self.priority
        kg.Low = self.low
        kg.High = self.high
        return kg


# Higher level SWD class with functions for samplebank files (nothing we don't care about) (no prgi/kgrps)
# groups: 1: BG, 10: GE, 20: SI, 30: SY
class SampleBank:
    def __init__(self, label, n_samples, group):
        self.samples = np.ndarray((n_samples,), Sample)  # None if inactive
        self.label = label
        self.group = group

    @property
    def active_samples(self):
        return self.samples[self.samples != None]

    @classmethod
    def from_parser(cls, parser: SWD_Parser):
        self = cls(parser.label, parser.n_wavi_slots, parser.group)
        for i, s in enumerate(parser.Samples):
            if s.Data:  # Sample is used
                self.samples[i] = Sample.from_parsersample(s)
        return self

    def to_parser(self):
        parser = SWD_Parser()
        parser.Samples = [SWD_SampleBlock() for _ in range(len(self.samples))]
        dataoffset = 0
        for s in self.active_samples:
            s: Sample
            parser.Samples[s.index] = s.to_parsersample(dataoffset)
            dataoffset += len(s.adpcm)
        parser.is_mainbank = True
        parser.group = self.group
        lt = localtime()
        parser.year, parser.month, parser.day, parser.hour, parser.minute, parser.second = \
            lt.tm_year, lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min, lt.tm_sec
        parser.label = self.label
        parser.len_pcmd = sum([len(x.adpcm) for x in self.active_samples])
        parser.unk0x4a = 257  # always this in mainbanks
        len_wavi = len(self.samples) * 2
        len_wavi += 16 - (len_wavi % 16) if len_wavi % 16 else 0
        len_wavi += len(self.active_samples) * 0x40
        parser.len_wavi = len_wavi
        parser.n_wavi_slots = len(self.samples)
        parser.n_pgri_slots = 0
        return parser

    @classmethod
    def from_data(cls, data):
        self = cls.from_parser(SWD_Parser.new_from_data(data))
        return self

    def to_data(self):  # if you make changes to the file, you must change the programbanks as well
        return self.to_parser().to_data()

    def export_all_samples_to_wav(self, folder, prefix="$label sample $index.wav", tuned=True):
        if not os.path.exists(folder):
            os.mkdir(folder)
        for sample in self.active_samples:
            sample: Sample
            data = {"rate": sample.samplerate,
                    "sec": len(sample.pcm16) // sample.samplerate,
                    "mili": len(sample.pcm16) * 1000 // sample.samplerate,
                    "label": self.label}
            data.update(sample.__dict__)  # $index $sample_rate $loop $fine_tune $course_tune
            template = Template(prefix)
            filename = template.safe_substitute(data)
            path = os.path.join(folder, filename)
            wavfile.write(path, sample.samplerate_tuned if tuned else sample.samplerate, sample.pcm16)


class ProgramBank:
    def __init__(self, label, programs, keygroups, samplebank: SampleBank, unk0x4a=2):
        self.samplebank = samplebank
        self.label = label
        self.samples_used = []
        self.unk0x4a = unk0x4a  # always 2 in songs, idk what it is in soundfx

        if type(programs) == int:
            self.programs = np.ndarray((programs,), ProgramInfo)
        else:
            self.programs = programs
        if type(keygroups) == int:
            self.key_groups = np.ndarray((keygroups,), Keygroup)
        else:
            self.key_groups = keygroups

    @classmethod
    def from_parser(cls, parser: SWD_Parser, samplebank: SampleBank):
        self = cls(parser.label, parser.n_pgri_slots, len(parser.Programs.Keygroups),
                   samplebank, parser.unk0x4a & 0xFF)
        for i, s in enumerate(parser.Samples):
            if s.WavInfo.SampleRate:  # quickly check if it's used
                self.samples_used.append(i)
        for i, k in enumerate(parser.Programs.Keygroups):
            self.key_groups[i] = Keygroup.from_parserkeygroup(k)
        for i, p in enumerate(parser.Programs.ProgramInfos):
            self.programs[i] = ProgramInfo.from_parserprograminfo(p)
        return self

    def to_parser(self):
        parser = SWD_Parser()
        parser.label = self.label
        parser.n_pgri_slots = len(self.programs)
        parser.Programs.ProgramInfos = [x.to_parserprograminfo() if x else SWD_ProgramInfo() for x in self.programs]
        parser.Programs.Keygroups = [x.to_parserkeygroup() if x else SWD_KeyGroup() for x in self.key_groups]
        parser.n_wavi_slots = max(self.samples_used)
        if parser.n_wavi_slots % 16:
            parser.n_wavi_slots += 16 - (parser.n_wavi_slots % 16)
        parser.Samples = [SWD_SampleBlock() for _ in range(len(self.samplebank.samples))][:parser.n_wavi_slots]
        pos = 0
        for i in self.samples_used:
            smp: SWD_SampleBlock = self.samplebank.samples[i].to_parsersample(0)
            smp.WavInfo.SampleOffset = pos
            pos += len(self.samplebank.samples[i].adpcm)
            parser.Samples[i] = smp
        lt = localtime()
        parser.year, parser.month, parser.day, parser.hour, parser.minute, parser.second = \
            lt.tm_year, lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min, lt.tm_sec
        len_wavi = parser.n_wavi_slots * 2
        len_wavi += 16 - (len_wavi % 16) if len_wavi % 16 else 0
        len_wavi += len(self.samples_used) * 0x40
        parser.len_wavi = len_wavi
        parser.is_mainbank = False
        parser.group = self.samplebank.group
        parser.unk0x4a = self.unk0x4a | (self.unk0x4a << 8)  # seems to always be the same byte
        parser.len_pcmd = 0xAAAA0000 | 1 | (self.samplebank.group << 8)
        return parser

    @classmethod
    def from_data(cls, data, mainbank):
        self = cls.from_parser(SWD_Parser.new_from_data(data), mainbank)
        return self

    def to_data(self):  # if you make changes to the file, you must change the programbanks as well
        return self.to_parser().to_data()
