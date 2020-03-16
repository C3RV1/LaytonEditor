import numpy as np
from LaytonLib.binary import BinaryWriter

index_table = [-1, -1, -1, -1, 2, 4, 6, 8] * 2
step_table = [7, 8, 9, 10, 11, 12, 13, 14,
              16, 17, 19, 21, 23, 25, 28, 31,
              34, 37, 41, 45, 50, 55, 60, 66,
              73, 80, 88, 97, 107, 118, 130, 143,
              157, 173, 190, 209, 230, 253, 279, 307,
              337, 371, 408, 449, 494, 544, 598, 658,
              724, 796, 876, 963, 1060, 1166, 1282, 1411,
              1552, 1707, 1878, 2066, 2272, 2499, 2749, 3024,
              3327, 3660, 4026, 4428, 4871, 5358, 5894, 6484,
              7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899,
              15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794,
              32767]


# More direct decoding, based on vgmstudio but without the class
def ADPCMtoPCM16(data):
    pcm16_len = (len(data) - 4) * 2
    buffer = np.zeros(pcm16_len, np.int16)
    last_sample = data[0] | data[1] << 8
    step_index = (data[2] | data[3] << 8) & 0x7f

    data_offset = 4
    on_second_nibble = False

    for i in range(pcm16_len):
        val = (data[data_offset] >> (4 if on_second_nibble else 0)) & 0xf
        step = step_table[step_index]
        diff = (step // 8) + \
               (step // 4 * (val & 1)) + \
               (step // 2 * ((val >> 1) & 1)) + \
               (step * ((val >> 2) & 1))
        a = (diff * (-1 if (((val >> 3) & 1) == 1) else 1)) + last_sample
        if a < -32768:
            a = -32768
        if a > 32767:
            a = 32767
        last_sample = a
        b = step_index + index_table[val]
        if b < 0:
            b = 0
        elif b > 88:
            b = 88
        step_index = b

        if on_second_nibble:
            data_offset += 1
        on_second_nibble = not on_second_nibble
        buffer[i] = last_sample
    return buffer


# Code below is copied and modified from pyima

"""
The MIT License (MIT)

Copyright (c) 2016 acida

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

_encoder_predicted = 0
_encoder_index = 0


def encode_sample(sample):
    global _encoder_index, _encoder_predicted

    delta = sample - _encoder_predicted

    if delta >= 0:
        value = 0
    else:
        value = 8
        delta = -delta

    step = step_table[_encoder_index]

    diff = step >> 3

    if delta > step:
        value |= 4
        delta -= step
        diff += step
    step >>= 1

    if delta > step:
        value |= 2
        delta -= step
        diff += step
    step >>= 1

    if delta > step:
        value |= 1
        diff += step

    if value & 8:
        _encoder_predicted -= diff
    else:
        _encoder_predicted += diff

    if _encoder_predicted < - 0x8000:
        _encoder_predicted = -0x8000
    elif _encoder_predicted > 0x7fff:
        _encoder_predicted = 0x7fff

    _encoder_index += index_table[value & 7]

    if _encoder_index < 0:
        _encoder_index = 0
    elif _encoder_index > 88:
        _encoder_index = 88

    return value

def PCM16toADPCM(pcm16: np.ndarray):
    global _encoder_index, _encoder_predicted
    _encoder_index = 0
    _encoder_predicted = 0
    wtr = BinaryWriter()

    # header calculation
    wtr.writeU16(pcm16[0])
    encode_sample(pcm16[0])
    wtr.writeU16(_encoder_index)
    sample = 0

    for i in range(1, len(pcm16)):
        if not sample is None:
            sample2 = encode_sample(pcm16[i])
            wtr.writeU8(sample2 << 4 | sample)
            sample = None
        else:
            sample = encode_sample(pcm16[i])
    if not sample is None:
        wtr.writeU8(sample)
    return wtr.data


