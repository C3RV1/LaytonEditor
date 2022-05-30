import logging
from dataclasses import dataclass
from enum import IntEnum
from typing import *

import numpy as np

from formats.sound.adpcm import adpcm_to_pcm16, pcm16_to_adpcm


class Sample:
    samplerate: int
    _pcm: Optional[np.ndarray] = None
    _adpcm: Optional[bytearray] = None

    def __init__(self, samplerate, data):
        self.samplerate = samplerate
        if type(data) == np.ndarray:
            self._pcm = data
        elif type(data) == bytes:
            self._adpcm = data
        else:
            logging.error(f"Unknown format of Sample ({type(data)})")

    def __repr__(self):
        if self._pcm:
            return f"Sample({self.samplerate}, {self._pcm})"
        else:
            return f"Sample({self.samplerate}, {self._adpcm})"

    @property
    def pcm(self):
        if self._pcm is not None:
            return self._pcm
        elif self._adpcm is not None:
            self._pcm = adpcm_to_pcm16(self._adpcm)
            return self._pcm
        else:
            return None

    @pcm.setter
    def pcm(self, value):
        self._pcm = value
        self._adpcm = None

    @property
    def adpcm(self):
        if self._adpcm:
            return self._adpcm
        elif self._pcm:
            self._adpcm = pcm16_to_adpcm(self._pcm)
            return self._adpcm
        else:
            return None

    @adpcm.setter
    def adpcm(self, value):
        self._adpcm = value
        self._pcm = None


@dataclass
class SampleInfo:
    sample_index: int
    # the sample loops
    loop_enabled: bool
    # number of pcm samples before the loop point
    loop: int
    # tuning in semitones
    tuning: float


@dataclass
class SplitEntry:
    highkey: int
    lowkey: int
    sample_info: SampleInfo
    tuning: float
    rootkey: int

    def __contains__(self, item):
        return isinstance(item, int) and self.lowkey <= item <= self.highkey

    @property
    def range(self):
        return self.highkey - self.lowkey


class LFODestination(IntEnum):
    none = 0
    pitch = 1
    volume = 2
    pan = 3
    lowpass_filter = 4


class LFOWaveShape(IntEnum):
    square = 0
    disabled = 1
    triangle = 2
    sinus = 3
    _unk = 4
    saw = 5
    _noise = 6
    _random = 7


@dataclass
class LFO:
    destination: LFODestination
    wave_shape: LFOWaveShape
    rate: int
    depth: int
    delay: int


@dataclass
class Preset:
    split_entries: List[SplitEntry]
    lfos: List[LFO]

    @property
    def lowkey(self):
        return min(split.lowkey for split in self.split_entries)

    @property
    def highkey(self):
        return max(split.highkey for split in self.split_entries)

    def __contains__(self, item):
        return isinstance(item, int) and self.lowkey <= item <= self.highkey

    @property
    def range(self):
        return self.highkey - self.lowkey


@dataclass
class SampleBank:
    label: str
    group: int
    samples: Dict[int, Sample]


@dataclass
class PresetBank:
    label: str
    group: int
    presets: Dict[int, Preset]
    samples_info: Dict[int, SampleInfo]
