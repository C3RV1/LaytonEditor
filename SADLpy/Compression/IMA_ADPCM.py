# Ported from: https://github.com/pleonex/tinke by Cervi for Team Top Hat

from .PCM import BitConverter
from ..Helper import Helper
import numpy as np


class ImaAdpcm:
    def __init__(self):
        self.index = 0
        self.step_size = 7
        self.new_sample = 0

        self.predicted_sample = 0

    def reset(self):
        self.index = 0
        self.step_size = 7
        self.new_sample = 0

        self.predicted_sample = 0

    def decompress(self, data: bytearray) -> np.ndarray:
        data = Helper.bit8_to_bit4(data)
        result = np.zeros((len(data),))

        for i in range(0, len(data)):
            step = ImaAdpcm.STEPSIZE_TABLE[self.index]
            difference = step >> 3
            if data[i] & 4:
                difference += step
            if data[i] & 2:
                difference += step >> 1
            if data[i] & 1:
                difference += step >> 2

            if data[i] & 8 != 0:
                difference = -difference
            self.new_sample += difference

            if self.new_sample > 32767:
                self.new_sample = 32767
            elif self.new_sample < -32768:
                self.new_sample = -32768

            # print(BitConverter.get_bytes_short(self.new_sample))
            result[i] = self.new_sample
            # result += BitConverter.get_bytes_short(self.new_sample)

            # result += BitConverter.get_bytes_short(self.new_sample)
            self.index += ImaAdpcm.INDEX_TABLE[data[i]]
            if self.index < 0:
                self.index = 0
            elif self.index > 88:
                self.index = 88

        return result

    def compress(self, data: list) -> bytearray:
        result = bytearray()

        # for i in range(0, len(data), 2):
        for i in range(0, len(data)):
            step = ImaAdpcm.STEPSIZE_TABLE[self.index]
            # original_sample = BitConverter.to_int_16(data, i)
            original_sample = int(data[i])
            different = original_sample - self.predicted_sample

            if different >= 0:
                new_sample = 0
            else:
                new_sample = 8
                different = -different

            mask = 4
            temp_step_size = step
            for j in range(0, 3):
                if different >= temp_step_size:
                    new_sample |= mask
                    different -= temp_step_size
                temp_step_size >>= 1
                mask >>= 1

            different = step >> 3
            if new_sample & 4:
                different += step
            if new_sample & 2:
                different += step >> 1
            if new_sample & 1:
                different += step >> 2

            if new_sample & 8:
                different = -different
            self.predicted_sample += different

            if self.predicted_sample > 32767:
                self.predicted_sample = 32767
            elif self.predicted_sample < -32768:
                self.predicted_sample = -32768

            result.append(new_sample & 0xF)

            self.index += ImaAdpcm.INDEX_TABLE[new_sample]
            if self.index < 0:
                self.index = 0
            elif self.index > 88:
                self.index = 88

        result = Helper.bit4_to_bit8(result)

        return result

    INDEX_TABLE = [-1, -1, -1, -1, 2, 4, 6, 8,
                   -1, -1, -1, -1, 2, 4, 6, 8]

    STEPSIZE_TABLE = [7, 8, 9, 10, 11, 12, 13, 14,
                      16, 17, 19, 21, 23, 25, 28,
                      31, 34, 37, 41, 45, 50, 55,
                      60, 66, 73, 80, 88, 97, 107,
                      118, 130, 143, 157, 173, 190, 209,
                      230, 253, 279, 307, 337, 371, 408,
                      449, 494, 544, 598, 658, 724, 796,
                      876, 963, 1060, 1166, 1282, 1411, 1552,
                      1707, 1878, 2066, 2272, 2499, 2749, 3024, 3327, 3660, 4026,
                      4428, 4871, 5358, 5894, 6484, 7132, 7845, 8630,
                      9493, 10442, 11487, 12635, 13899, 15289, 16818,
                      18500, 20350, 22385, 24623, 27086, 29794, 32767]
