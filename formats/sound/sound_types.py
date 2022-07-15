from typing import List

import numpy as np


class Sample:
    id_: int
    fine_tune: int
    coarse_tune: int
    root_key: int
    key_transpose: int
    volume: int
    pan: int
    pcm16: np.ndarray
    loop_enabled: bool
    sample_rate: int
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


class KeyGroup:
    id_: int
    polyphony: int
    priority: int
    voice_channel_low: int
    voice_channel_high: int


class Split:
    low_key: int
    high_key: int
    low_vel: int
    high_vel: int
    sample: 'Sample'
    fine_tune: int
    coarse_tune: int
    root_key: int
    key_transpose: int
    volume: int
    pan: int
    key_group: KeyGroup
    envelope: int
    envelope_multiplier: int
    attack_volume: int
    attack: int
    decay: int
    sustain: int
    hold: int
    decay2: int
    release: int


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
    id_: int
    volume: int
    pan: int
    lfos: List[LFO]
    splits: List[Split]
