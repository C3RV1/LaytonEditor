# Ported from: https://github.com/pleonex/tinke by Cervi for Team Top Hat
from cint.cint import U16, I32
from ..Helper import Helper
from .PCM import BitConverter
import numpy as np


def binary_log2(n: int):
    scale = 12
    while n > 0:
        n = n >> 1
        scale -= 1
        if scale == 0:
            break
    return scale


def binary_log2_bytes(b: bytearray):
    c = [U16(BitConverter.from_bytes_short(b[n:n+2])) for n in range(0, len(b), 2)]
    return binary_log2(int(sum(c)/len(c)))


class Procyon:
    PROC_COEF = [[0, 0],
                 [0x3c, 0],
                 [115, -52],
                 [98, -55],
                 [122, -60]]

    def __init__(self):
        self.hist = [I32(0), I32(0)]

    def reset(self):
        self.hist = [I32(0), I32(0)]

    def decode_sample(self, sample, coef1, coef2, scale):
        # error = sample - 0x10 if sample >> 3 == 1 else sample
        error = sample
        error <<= (6 + scale)

        pred = (self.hist[0] * coef1 + self.hist[1] * coef2 + 32) >> 6

        sample = pred + error

        self.hist[1] = self.hist[0]
        self.hist[0] = sample

        clamp = Helper.clamp16((sample + 32) >> 6) >> 6 << 6

        return clamp

    def encode_sample(self, sample, coef1, coef2, scale):
        value = sample << 6
        pred = (self.hist[0]*coef1 + self.hist[1]*coef2 + 32) >> 6
        error = value - pred
        error_scaled = error >> (scale + 6)

        result = error_scaled & 0xF
        result = (result + 8) % 16 - 8

        error_approx = result
        error_approx <<= (scale + 6)

        self.hist[1] = self.hist[0]
        self.hist[0] = pred + error_approx

        sample_approx = pred + error_approx
        clamp = Helper.clamp16((sample_approx + 32) >> 6) >> 6 << 6

        diff = abs(sample - clamp)
        return result, diff

    def decode_block(self, block: bytearray, samples_to_do: int) -> np.ndarray:
        buffer = np.zeros(shape=(samples_to_do,), dtype=np.int32)

        header = block[0xF] ^ 0x80
        scale = header & 0xf
        coef_index = header >> 4

        coef1 = Procyon.PROC_COEF[coef_index][0]
        coef2 = Procyon.PROC_COEF[coef_index][1]

        for i in range(samples_to_do):
            sample_byte = block[int(i // 2)] ^ 0x80

            if i & 1 == 1:
                sample = Helper.get_high_nibble_signed(sample_byte)
            else:
                sample = Helper.get_low_nibble_signed(sample_byte)
            buffer[i] = self.decode_sample(sample, coef1, coef2, scale)

        return buffer

    def encode_block(self, block: list):
        # TODO: Encoding improve performance
        if len(block) < 30:
            block.extend([0]*(30 - len(block)))
        best_encoded, scale, coef_index = self.search_best_encode(block)

        result = bytearray(b"\x00" * 16)
        current_value = 0
        for i, sample in enumerate(best_encoded):
            sample = (sample + 16) % 16  # Make positive
            if i % 2 == 0:  # low nibble
                current_value = sample
            else:  # high nibble
                current_value |= sample << 4
                result[i//2] = current_value ^ 0x80
        header = (coef_index << 4) | scale
        current_value = header
        result[-1] = current_value ^ 0x80
        return result

    def search_best_encode(self, block: list):
        coef_index = 0
        scale = 0

        current_hist = [0, 0]
        current_hist[0] = self.hist[0]
        current_hist[1] = self.hist[1]
        new_hist = [0, 0]

        num_coef = 5
        num_scales = 12

        best_encoded = None
        min_difference = -1
        for temp_coef in range(num_coef):
            for temp_scale in range(num_scales):
                self.hist[0] = current_hist[0]
                self.hist[1] = current_hist[1]
                encoded, difference = self.get_encoding_difference(block, temp_coef, temp_scale, min_difference)

                if difference < min_difference or best_encoded is None:
                    min_difference = difference
                    best_encoded = encoded
                    coef_index = temp_coef
                    scale = temp_scale
                    new_hist[0] = self.hist[0]
                    new_hist[1] = self.hist[1]
                    if difference == 0:
                        return best_encoded, scale, coef_index
        self.hist = new_hist
        return best_encoded, scale, coef_index

    def get_encoding_difference(self, block: list, coef_index, scale, min_difference):
        coef1 = self.PROC_COEF[coef_index][0]
        coef2 = self.PROC_COEF[coef_index][1]

        result = [0]*len(block)

        total_difference = 0

        for i, sample in enumerate(block):
            r, diff = self.encode_sample(sample, coef1, coef2, scale)
            result[i] = r
            total_difference += diff
            if total_difference > min_difference and min_difference >= 0:
                # if we already know that this can't possibly be the best combination, we return
                return result, total_difference

        return result, total_difference
