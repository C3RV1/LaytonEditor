import cython
import numpy as np
cimport numpy as np
np.import_array()


ctypedef np.uint8_t TYPE_8_BIT
ctypedef np.int16_t TYPE_16_BIT

cdef int[5][2] PROC_COEF = [
    [0, 0],
    [0x3c, 0],
    [115, -52],
    [98, -55],
    [122, -60]
]

cdef class Procyon:
    cdef int[2] hist
    cdef np.ndarray tmp_array

    def __init__(self):
        self.hist = [0, 0]
        self.tmp_array = np.zeros((0x10,), dtype=np.uint8)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.exceptval(False)
    cdef int decode_sample(self, int sample, int coef1, int coef2, int scale):
        cdef int error = sample
        error <<= (6 + scale)

        cdef int pred = (self.hist[0] * coef1 + self.hist[1] * coef2 + 32) >> 6

        sample = pred + error

        self.hist[1] = self.hist[0]
        self.hist[0] = sample

        cdef short clamp = (sample + 32) >> 6
        clamp = clamp >> 6 << 6

        return clamp

    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.exceptval(False)
    cdef (int, int) encode_sample(self, int sample, int coef1, int coef2, int scale):
        cdef int value = sample << 6
        cdef int pred = (self.hist[0] * coef1 + self.hist[1] * coef2 + 32) >> 6
        cdef int error = value - pred
        cdef int error_scaled = error >> (scale + 6)

        cdef int result = error_scaled % 16
        result = (result + 8) % 16 - 8

        cdef int error_approx = result
        error_approx <<= (scale + 6)

        self.hist[1] = self.hist[0]
        self.hist[0] = pred + error_approx

        cdef int sample_approx = pred + error_approx

        cdef short clamp = (sample_approx + 32) >> 6
        clamp = clamp >> 6 << 6

        cdef int diff = abs(sample - clamp)
        return result, diff

    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.exceptval(False)
    cpdef decode_block(self, TYPE_8_BIT[:] block,
                       TYPE_16_BIT[:] destination):
        cdef int header = block[0xF] ^ 0x80
        cdef int scale = header & 0xf
        cdef int coef_index = header >> 4

        cdef int coef1 = PROC_COEF[coef_index][0]
        cdef int coef2 = PROC_COEF[coef_index][1]

        cdef int sample_byte, i, sample
        for i in range(30):
            sample_byte = block[i // 2] ^ 0x80

            if i & 1 == 1:
                sample = (sample_byte & 0xf0) >> 4
            else:
                sample = sample_byte & 0x0f
            sample = ((sample + 8) % 16) - 8
            destination[i] = self.decode_sample(sample, coef1, coef2, scale)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.exceptval(False)
    cpdef encode_block(self, TYPE_16_BIT[:] block,
                       TYPE_8_BIT[:] destination):
        # TODO: Encoding improve performance (currently it's brute force)
        if len(block) < 30:
            append_block = np.zeros((30 - len(block),), np.int16)
            block = np.append(block, append_block)
        cdef int scale, coef_index
        cdef (int, int) best_encoding = self.search_best_encode(block, destination)
        scale = best_encoding[0]
        coef_index = best_encoding[1]

        header = (coef_index << 4) | scale
        destination[0xF] = header ^ 0x80

    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.exceptval(False)
    cdef (int, int) search_best_encode(self, TYPE_16_BIT[:] block,
                                       TYPE_8_BIT[:] destination):
        cdef int coef_index = 0
        cdef int scale = 0

        cdef int[2] current_hist = [self.hist[0], self.hist[1]]
        cdef int[2] new_hist = [0, 0]

        cdef np.ndarray tmp_array = self.tmp_array
        cdef int min_difference = -1
        cdef int temp_coef, temp_scale
        cdef int difference

        for temp_coef in range(5):
            for temp_scale in range(12):
                self.hist[0] = current_hist[0]
                self.hist[1] = current_hist[1]
                difference = self.get_encoding_difference(block, temp_coef, temp_scale, min_difference,
                                                          tmp_array, destination)

                if difference < min_difference or min_difference == -1:
                    min_difference = difference
                    coef_index = temp_coef
                    scale = temp_scale
                    new_hist[0] = self.hist[0]
                    new_hist[1] = self.hist[1]
                    if difference == 0:
                        break
            if min_difference == 0:
                break
        self.hist = new_hist
        return scale, coef_index

    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.exceptval(False)
    cdef int get_encoding_difference(self, TYPE_16_BIT[:] block, int coef_index, int scale,
                                     int min_difference, TYPE_8_BIT[:] tmp_array,
                                     TYPE_8_BIT[:] destination):
        cdef int coef1 = PROC_COEF[coef_index][0]
        cdef int coef2 = PROC_COEF[coef_index][1]

        cdef int total_difference = 0

        cdef int i, sample, r, diff
        cdef int block_len = block.shape[0]
        cdef (int, int) encode_result
        for i in range(block_len):
            sample = block[i]
            encode_result = self.encode_sample(sample, coef1, coef2, scale)
            r = encode_result[0]
            diff = encode_result[1]
            r = (r + 16) % 16  # Make positive
            if i % 2 == 0:
                tmp_array[i//2] = r
            else:
                tmp_array[i//2] |= r << 4
                tmp_array[i//2] ^= 0x80
            total_difference += diff
            if total_difference >= min_difference >= 0:
                # if we already know that this can't possibly be the best combination, we return
                return total_difference

        destination[:15] = tmp_array[:15]
        return total_difference

