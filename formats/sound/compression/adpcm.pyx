import numpy as np
cimport numpy as np
np.import_array()


cdef int[16] INDEX_TABLE = [-1, -1, -1, -1, 2, 4, 6, 8,
                            -1, -1, -1, -1, 2, 4, 6, 8]

cdef int[89] STEP_SIZE_TABLE = [
    7, 8, 9, 10, 11, 12, 13, 14,
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
    18500, 20350, 22385, 24623, 27086, 29794, 32767
]

ctypedef np.uint8_t TYPE_8_BIT
ctypedef np.int16_t TYPE_16_BIT


cdef class Adpcm:
    cdef int index, new_sample, predicted_sample
    cdef bint first

    def __init__(self, bint do_first):
        self.index = 0
        self.new_sample = 0
        self.first = do_first

        self.predicted_sample = 0

    cpdef np.ndarray[TYPE_16_BIT, ndim=1] decompress(self, np.ndarray[TYPE_8_BIT, ndim=1] data):
        cdef int* step_size_table = STEP_SIZE_TABLE
        cdef int* index_table = INDEX_TABLE
        cdef int iter_len, iter_start, index
        cdef short new_sample
        cdef np.ndarray[TYPE_16_BIT, ndim=1] result

        if self.first:  # First time we load new_sample and index from the preamble
            iter_len = (data.shape[0] - 4) * 2
            iter_start = 1
            result = np.zeros((iter_len + 1,), dtype=np.int16)
            result[1::2] = data[4:] & 0x0f
            result[2::2] = data[4:] >> 4

            new_sample = data[0] | data[1] << 8
            result[0] = new_sample
            index = (data[2] | data[3] << 8) & 0x7f
            self.first = False
        else:
            iter_len = data.shape[0] * 2
            iter_start = 0

            result = np.zeros((iter_len,), dtype=np.int16)
            result[::2] = data[:] & 0x0f
            result[1::2] = data[:] >> 4

            index = self.index
            new_sample = self.new_sample

        cdef int i, d, step, difference
        for i in range(iter_start, iter_len + iter_start):
            d = result[i]
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

    cpdef np.ndarray[TYPE_8_BIT, ndim=1] compress(self, np.ndarray[TYPE_16_BIT, ndim=1] data):
        # (v + 1) // 2 = ceil(v / 2)
        cdef np.ndarray[TYPE_8_BIT, ndim=1] result = np.ndarray(((len(data) + 1) // 2,), dtype=np.uint8)

        cdef int index = self.index
        cdef short original_sample, predicted_sample, new_sample = self.predicted_sample
        cdef int i, step, different, mask, temp_step_size
        for i in range(0, len(data)):
            step = STEP_SIZE_TABLE[index]
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

            if i % 2 == 0:
                result[i // 2] = new_sample & 0xF
            else:
                result[i // 2] += new_sample & 0xF << 4

            index += INDEX_TABLE[new_sample]
            if index < 0:
                index = 0
            elif index > 88:
                index = 88
        self.index = index
        self.predicted_sample = predicted_sample

        return result


