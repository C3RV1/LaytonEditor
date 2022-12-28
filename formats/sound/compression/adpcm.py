import numpy as np


class Adpcm:
    def __init__(self):
        self.index = 0
        self.new_sample = 0

        self.predicted_sample = 0

    def reset(self):
        self.index = 0
        self.new_sample = 0

        self.predicted_sample = 0

    def decompress(self, data: np.ndarray) -> np.ndarray:
        step_size_table = Adpcm.STEP_SIZE_TABLE
        index_table = Adpcm.INDEX_TABLE
        iter_len = data.shape[0] * 2
        result = np.zeros((iter_len,), dtype=np.int16)
        result[::2] = data[:] & 0x0f
        result[1::2] = data[:] >> 4
        index = self.index
        new_sample = self.new_sample
        for i in range(iter_len):
            d = int(result[i])
            step = step_size_table[index]
            difference = step >> 3
            if d & 4:
                difference += step
            if d & 2:
                difference += step >> 1
            if d & 1:
                difference += step >> 2

            if d & 8 != 0:
                difference = -difference
            new_sample += difference
            if new_sample > 32767:
                new_sample = 32767
            elif new_sample < -32768:
                new_sample = -32768

            result[i] = new_sample
            index += index_table[d]
            if index < 0:
                index = 0
            elif index > 88:
                index = 88
        self.index = index
        self.new_sample = new_sample

        return result

    def compress(self, data: np.ndarray) -> np.ndarray:
        # (v + 1) // 2 = ceil(v / 2)
        result = np.ndarray(((len(data) + 1) // 2,), dtype=np.uint8)

        index = self.index
        predicted_sample = self.predicted_sample
        for i in range(0, len(data)):
            step = Adpcm.STEP_SIZE_TABLE[index]
            original_sample = data[i]
            different = original_sample - predicted_sample

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
            predicted_sample += different

            if predicted_sample > 32767:
                predicted_sample = 32767
            elif predicted_sample < -32768:
                predicted_sample = -32768

            if i % 2 == 0:
                result[i // 2] = new_sample & 0xF
            else:
                result[i // 2] += new_sample & 0xF << 4

            index += Adpcm.INDEX_TABLE[new_sample]
            if index < 0:
                index = 0
            elif index > 88:
                index = 88
        self.index = index
        self.predicted_sample = predicted_sample

        return result

    INDEX_TABLE = [-1, -1, -1, -1, 2, 4, 6, 8,
                   -1, -1, -1, -1, 2, 4, 6, 8]

    STEP_SIZE_TABLE = [7, 8, 9, 10, 11, 12, 13, 14,
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
