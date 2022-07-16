from typing import List, Union

import numpy as np


class Sample:
    id_: Union[int, str]
    fine_tune: int = 0
    coarse_tune: int = 0
    root_key: int = 60
    volume: int = 0x7F
    pan: int = 64  # 0-64-127
    pcm16: np.ndarray = None
    loop_enabled: bool = False
    sample_rate: int = 32768
    loop_beginning: int = 0
    loop_length: int = 0
    envelope_on: bool = False
    envelope_multiplier: int = 0
    attack_volume: int = 0
    attack: int = 0
    decay: int = 0
    sustain: int = 0
    hold: int = 0
    decay2: int = 0
    release: int = 0


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
    pan: int = 64
    key_group: KeyGroup
    envelope_on: bool = False
    # TODO: integrate swd table # must integrate swd table (Volume Envelopes)
    envelope_multiplier: int = 0
    attack_volume: int = 0
    attack: int = 0
    decay: int = 0
    sustain: int = 0
    hold: int = 0
    decay2: int = 0
    release: int = 0


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
