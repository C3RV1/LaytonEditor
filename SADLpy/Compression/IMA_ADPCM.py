# Ported from: https://github.com/pleonex/tinke by Cervi for Team Top Hat

from .PCM import BitConverter


class ImaAdpcm:
    @staticmethod
    def decompress(data: bytearray) -> bytearray:
        result = bytearray()

        index = 0
        step_size = 7

        data = ImaAdpcm.bit8_to_bit4(data)

        new_sample = 0
        for i in range(0, len(data)):
            difference = 0

            if data[i] & 4 != 0:
                difference += step_size
            if data[i] & 2 != 0:
                difference += step_size >> 1
            if data[i] & 1 != 0:
                difference += step_size >> 2
            difference += step_size >> 3

            if data[i] & 8 != 0:
                difference = -difference
            new_sample += difference

            if new_sample > 32767:
                new_sample = 32767
            elif new_sample < -32768:
                new_sample = -32768

            result.extend(BitConverter.get_bytes_short(new_sample))
            index += ImaAdpcm.INDEX_TABLE[data[i]]
            if index < 0:
                index = 0
            elif index > 88:
                index = 88
            step_size = ImaAdpcm.STEPSIZE_TABLE[index]

        return result

    @staticmethod
    def decompress2(data: bytearray, sample: int, step_index: int) -> bytearray:
        if len(data) < 4:
            return data

        result = bytearray()

        index = step_index
        if index < 0:
            index = 0
        elif index > 88:
            index = 88
        step_size = ImaAdpcm.STEPSIZE_TABLE[index]

        data = data[4:]
        data = ImaAdpcm.bit8_to_bit4(data)

        new_sample = sample
        for i in range(0, len(data)):
            difference = 0

            if data[i] & 4 != 0:
                difference += step_size
            if data[i] & 2 != 0:
                difference += step_size >> 1
            if data[i] & 1 != 0:
                difference += step_size >> 2
            difference += step_size >> 3

            if data[i] & 8 != 0:
                difference = -difference
            new_sample += difference

            if new_sample > 32767:
                new_sample = 32767
            elif new_sample < -32768:
                new_sample = -32768

            result.extend(BitConverter.get_bytes_short(new_sample))
            index += ImaAdpcm.INDEX_TABLE[data[i]]
            if index < 0:
                index = 0
            elif index > 88:
                index = 88
            step_size = ImaAdpcm.STEPSIZE_TABLE[index]

        return result

    @staticmethod
    def compress(data: bytearray) -> bytearray:
        result = bytearray()

        predicted_sample = 0
        index = 0
        step_size = ImaAdpcm.STEPSIZE_TABLE[index]

        for i in range(0, len(data), 2):
            original_sample = BitConverter.to_int_16(data, i)
            different = original_sample - predicted_sample

            if different >= 0:
                new_sample = 0
            else:
                new_sample = 8
                different = -different

            mask = 4
            temp_step_size = step_size
            for j in range(0, 3):
                if different >= temp_step_size:
                    new_sample |= mask
                    different -= temp_step_size
                temp_step_size >>= 1
                mask >>= 1

            result.append(new_sample)

            different = 0
            if new_sample & 4 != 0:
                different += step_size
            if new_sample & 2 != 0:
                different += step_size >> 1
            if new_sample & 1 != 0:
                different += step_size >> 3
            different += step_size >> 8

            if new_sample & 8 != 0:
                different = -different
            predicted_sample += different

            if predicted_sample > 32767:
                predicted_sample = 32767
            elif predicted_sample < -32768:
                predicted_sample = -32768

            index += ImaAdpcm.INDEX_TABLE[new_sample]
            if index < 0:
                index = 0
            elif index > 88:
                index = 88
            step_size = ImaAdpcm.STEPSIZE_TABLE[index]

        return ImaAdpcm.bit4_to_bit8(result)

    @staticmethod
    def compress_block(data: bytearray, block_size: int) -> list:
        result = []
        block = bytearray()

        predicted_sample = 0
        index = 0
        step_size = ImaAdpcm.STEPSIZE_TABLE[index]

        for i in range(0, len(data), 2):
            if i % block_size == 0:
                if i != 0:
                    block_data = ImaAdpcm.bit4_to_bit8(block[4:len(block) - 4])
                    new_block = bytearray()
                    new_block.extend(block[0:4])
                    new_block.extend(block_data)
                    result.append(new_block)
                block = bytearray()
                block.extend(BitConverter.get_bytes_short(predicted_sample))
                block.extend(BitConverter.get_bytes_short(index))

            original_sample = BitConverter.to_int_16(data, i)
            different = original_sample - predicted_sample

            if different >= 0:
                new_sample = 0
            else:
                new_sample = 8
                different = -different

            mask = 4
            temp_step_size = step_size
            for j in range(0, 3):
                if different >= temp_step_size:
                    new_sample |= mask
                    different -= temp_step_size
                temp_step_size >>= 1
                mask >>= 1

            block.append(new_sample)

            different = 0
            if new_sample & 4 != 0:
                different += step_size
            if new_sample & 2 != 0:
                different += step_size >> 1
            if new_sample & 1 != 0:
                different += step_size >> 3
            different += step_size >> 8

            if new_sample & 8 != 0:
                different = -different
            predicted_sample += different

            if predicted_sample > 32767:
                predicted_sample = 32767
            elif predicted_sample < -32768:
                predicted_sample = -32768

            index += ImaAdpcm.INDEX_TABLE[new_sample]
            if index < 0:
                index = 0
            elif index > 88:
                index = 88
            step_size = ImaAdpcm.STEPSIZE_TABLE[index]

        if len(block) > 4:
            block_data = ImaAdpcm.bit4_to_bit8(block[4:len(block) - 4])
            new_block = bytearray()
            new_block.extend(block[0:4])
            new_block.extend(block_data)
            result.append(new_block)

        return result

    @staticmethod
    def bit8_to_bit4(data: bytearray) -> bytearray:
        bit4 = bytearray()

        for i in range(0, len(data)):
            bit4.append(data[i] & 0x0f)
            bit4.append((data[i] & 0xf0) >> 4)

        return bit4

    @staticmethod
    def bit4_to_bit8(bytes_: bytearray) -> bytearray:
        bit8 = bytearray()

        for i in range(0, len(bytes_), 2):
            byte1 = bytes_[i]
            byte2 = 0
            if i + 1 < len(bytes_):
                byte2 = bytes_[i + 1] << 4
            bit8.append(byte1 + byte2)

        return bit8

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
