import numpy as np


def clamp_unsigned(value, bytes_):
    size = 8*bytes_
    return ((value + (1 << size)) % (2 << size)) - (1 << size)


class Procyon:
    PROC_COEF = [[0, 0],
                 [0x3c, 0],
                 [115, -52],
                 [98, -55],
                 [122, -60]]

    def __init__(self):
        self.hist = [0, 0]
        self.tmp_array = np.zeros((0x10,), dtype=np.uint8)

    def reset(self):
        self.hist = [0, 0]

    def clamp_hist(self):
        self.hist[0] = clamp_unsigned(self.hist[0], 4)
        self.hist[1] = clamp_unsigned(self.hist[1], 4)

    def decode_sample(self, sample, coef1, coef2, scale):
        error = sample
        error <<= (6 + scale)

        pred = (self.hist[0] * coef1 + self.hist[1] * coef2 + 32) >> 6

        sample = pred + error

        self.hist[1] = self.hist[0]
        self.hist[0] = sample
        self.clamp_hist()

        clamp = (sample + 32) >> 6
        if clamp > 32767:
            clamp = 32767
        if clamp < -32768:
            clamp = -32768
        clamp = clamp >> 6 << 6

        return clamp

    def encode_sample(self, sample, coef1, coef2, scale):
        value = sample << 6
        pred = (self.hist[0]*coef1 + self.hist[1]*coef2 + 32) >> 6
        error = value - pred
        error_scaled = error >> (scale + 6)

        result = error_scaled % 16
        result = (result + 8) % 16 - 8

        error_approx = result
        error_approx <<= (scale + 6)

        self.hist[1] = self.hist[0]
        self.hist[0] = pred + error_approx
        self.clamp_hist()

        sample_approx = pred + error_approx

        clamp = (sample_approx + 32) >> 6
        if clamp > 32767:
            clamp = 32767
        if clamp < -32768:
            clamp = -32768
        clamp = clamp >> 6 << 6

        diff = abs(sample - clamp)
        return result, diff

    def decode_block(self, block: np.ndarray, destination: np.ndarray) -> None:
        header = block[0xF] ^ 0x80
        scale = header & 0xf
        coef_index = header >> 4

        coef1 = Procyon.PROC_COEF[coef_index][0]
        coef2 = Procyon.PROC_COEF[coef_index][1]

        for i in range(30):
            sample_byte = block[int(i // 2)] ^ 0x80

            if i & 1 == 1:
                sample = (sample_byte & 0xf0) >> 4
            else:
                sample = sample_byte & 0x0f
            sample = ((sample + 8) % 16) - 8
            destination[i] = self.decode_sample(sample, coef1, coef2, scale)

    def encode_block(self, block: np.ndarray, destination: np.ndarray):
        # TODO: Encoding improve performance (currently it's brute force)
        if len(block) < 30:
            block = np.append(block, [0]*(30 - len(block)))
        scale, coef_index = self.search_best_encode(block, destination)

        header = (coef_index << 4) | scale
        destination[0xF] = header ^ 0x80

    def search_best_encode(self, block: np.ndarray, destination: np.ndarray):
        coef_index = 0
        scale = 0

        current_hist = [0, 0]
        current_hist[0] = self.hist[0]
        current_hist[1] = self.hist[1]
        new_hist = [0, 0]

        num_coef = 5
        num_scales = 12

        tmp_array = self.tmp_array
        min_difference = -1
        for temp_coef in range(num_coef):
            for temp_scale in range(num_scales):
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

    def get_encoding_difference(self, block: np.ndarray, coef_index, scale, min_difference,
                                tmp_array: np.ndarray, destination: np.ndarray):
        coef1 = self.PROC_COEF[coef_index][0]
        coef2 = self.PROC_COEF[coef_index][1]

        total_difference = 0

        for i, sample in enumerate(block):
            r, diff = self.encode_sample(sample, coef1, coef2, scale)
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
