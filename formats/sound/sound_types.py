from typing import List, Union

import numpy as np
from formats.sound.compression.adpcm import Adpcm


class Sample:
    id_: Union[int, str]
    fine_tune: int = 0
    coarse_tune: int = 0
    root_key: int = 60
    volume: int = 0x7F
    pan: int = 64  # 0-64-127
    _pcm16: np.ndarray = None
    _adpcm: np.ndarray = None
    loop_enabled: bool = False
    sample_rate: int = 32768
    loop_beginning: int = 0
    loop_length: int = 0
    envelope_on: bool = False
    attack_volume: int = 0
    attack: int = 0
    decay: int = 0
    sustain: int = 0x7F
    hold: int = 0
    decay2: int = 0x7F
    release: int = 0x28

    @property
    def pcm16(self):
        if self._pcm16 is None and self._adpcm is not None:
            self._pcm16 = Adpcm().decompress(self._adpcm)
            self._pcm16 = self._pcm16.reshape((self._pcm16.shape[0], 1))
        return self._pcm16

    @pcm16.setter
    def pcm16(self, v: np.ndarray):
        self._pcm16 = v
        self._adpcm = None

    @property
    def adpcm(self):
        if self._adpcm is None and self._pcm16 is not None:
            self._adpcm = Adpcm().compress(self._pcm16.reshape((self._pcm16.shape[0],)))
        return self._adpcm

    @adpcm.setter
    def adpcm(self, v: np.ndarray):
        self._adpcm = v
        self._pcm16 = None


class KeyGroup:
    id_: int
    polyphony: int
    priority: int
    voice_channel_low: int
    voice_channel_high: int


class Split:
    low_key: int = 0
    high_key: int = 0x7F
    low_vel: int = 0
    high_vel: int = 0x7F
    sample: 'Sample'
    fine_tune: int = 0
    coarse_tune: int = 0
    root_key: int = 60
    volume: int = 0x7F
    pan: int = 64  # (0-64-127)
    key_group: KeyGroup = None
    envelope_on: bool = False
    attack_volume: int = 0
    attack: int = 0  # ms
    decay: int = 0  # ms
    sustain: int = 0  # volume
    hold: int = 0  # ms
    decay2: int = 0  # ms
    release: int = 0  # ms


class LFO:
    destination: int
    # Destination of the lfo output
    # 0 - none/disabled
    # 1 - pitch
    # 2 - volume
    # 3 - pan
    # 4 - low pass / cut off filter
    wshape: int
    # Shape of the waveform
    # 1 - square
    # 2 - triangle?
    # 3 - sinus?
    # 4 - ?
    # 5 - Saw?
    # 6 - Noise?
    # 7 - Random
    rate: int
    depth: int
    delay: int


class Program:
    id_: Union[int, str]
    volume: int = 0x7F
    pan: int = 64  # 0-64-127
    lfos: List[LFO]
    splits: List[Split]
