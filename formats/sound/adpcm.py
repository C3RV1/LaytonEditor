import numpy as np

from formats.binary import BinaryWriter

index_table = [-1, -1, -1, -1, 2, 4, 6, 8] * 2
step_table = [7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25,
              28, 31, 34, 37, 41, 45, 50, 55, 60, 66, 73, 80, 88,
              97, 107, 118, 130, 143, 157, 173, 190, 209, 230, 253,
              279, 307, 337, 371, 408, 449, 494, 544, 598, 658, 724,
              796, 876, 963, 1060, 1166, 1282, 1411, 1552, 1707,
              1878, 2066, 2272, 2499, 2749, 3024, 3327, 3660, 4026,
              4428, 4871, 5358, 5894, 6484, 7132, 7845, 8630, 9493,
              10442, 11487, 12635, 13899, 15289, 16818, 18500,
              20350, 22385, 24623, 27086, 29794, 32767]


def adpcm_to_pcm16(adpcm: bytes):
    pcm16_len = (len(adpcm) - 4) * 2
    buffer = np.zeros(pcm16_len, np.int16)
    last_sample = adpcm[0] | adpcm[1] << 8
    step_index = (adpcm[2] | adpcm[3] << 8) & 0x7f

    data_offset = 4
    on_second_nibble = False

    for i in range(pcm16_len):
        val = (adpcm[data_offset]
               >> (4 if on_second_nibble else 0)) & 0xf
        step = step_table[step_index]
        diff = (step // 8) + \
               (step // 4 * (val & 1)) + \
               (step // 2 * ((val >> 1) & 1)) + \
               (step * ((val >> 2) & 1))
        a = (diff * (-1 if (((val >> 3) & 1) == 1)
                     else 1)) + last_sample
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


def pcm16_to_adpcm_encode_sample(sample, encoder_index,
                                 encoder_predicted):
    delta = sample - encoder_predicted
    value = 8 if delta < 0 else 0
    delta = abs(delta)

    step = step_table[encoder_index]
    diff = step >> 3

    for i in range(2):
        if delta > step:
            value |= 4 >> i
            delta -= step
            diff += step
        step >>= 1

    if delta > step:
        value |= 1
        diff += step

    if value & 8:
        encoder_predicted -= diff
    else:
        encoder_predicted += diff

    if encoder_predicted < - 0x8000:
        encoder_predicted = -0x8000
    elif encoder_predicted > 0x7fff:
        encoder_predicted = 0x7fff

    encoder_index += index_table[value & 7]

    encoder_index = max(0, min(88, encoder_index))

    return value, encoder_index, encoder_predicted


def pcm16_to_adpcm(pcm16: np.ndarray):
    enc_sample = pcm16_to_adpcm_encode_sample

    # Uses BytesIO which is faster then concatination.
    wtr = BinaryWriter()

    wtr.write_uint16(pcm16[0])
    sample, enc_index, enc_pred = enc_sample(pcm16[0], 0, 0)
    wtr.write_uint16(enc_index)

    for i in range(1, len(pcm16)):
        if sample is None:
            sample, enc_index, enc_pred = \
                enc_sample(pcm16[0], enc_index, enc_pred)
        else:
            sample2, enc_index, enc_pred = \
                enc_sample(pcm16[0], enc_index, enc_pred)
            wtr.write_byte(sample2 << 4 | sample)
            sample = None

    if sample is not None:
        wtr.write_uint8(sample)
    return wtr.data
