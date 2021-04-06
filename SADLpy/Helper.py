# Ported from: https://github.com/pleonex/tinke by Cervi for Team Top Hat


def clamp_nibble(n: int):
    n += 1 << 3
    n %= 1 << 4
    n -= 1 << 3
    return int(n)


class Helper:
    @staticmethod
    def merge_channels(left: list, right: list, loop_sample: int = 0) -> list:
        result = []
        for i in range(loop_sample, len(left), 2):
            result.append(left[i])
            if i + 1 < len(left):
                result.append(left[i+1])
            result.append(right[i])
            if i + 1 < len(right):
                result.append(right[i+1])

        return result

    @staticmethod
    def divide_channels(data: bytearray) -> list:
        left = bytearray()
        right = bytearray()

        for i in range(0, int(len(data) / 4), 4):
            left.append(data[i])
            left.append(data[i+1])
            right.append(data[i])
            right.append(data[i+1])

        return [left, right]

    @staticmethod
    def bit8_to_bit4(data: bytearray) -> bytearray:
        bit4 = bytearray()

        for i in range(0, len(data)):
            bit4.append(data[i] & 0x0f)
            bit4.append((data[i] & 0xf) >> 4)

        return bit4

    NIBBLE_TO_INT = [0, 1, 2, 3, 4, 5, 6, 7, -8, -7, -6, -5, -4, -3, -2, -1]

    @staticmethod
    def get_high_nibble_signed(n: int) -> int:
        return Helper.NIBBLE_TO_INT[int(n) >> 4]

    @staticmethod
    def from_high_nibble_signed(n: int) -> int:
        return Helper.NIBBLE_TO_INT.index(clamp_nibble(n)) << 4

    @staticmethod
    def get_low_nibble_signed(n: int) -> int:
        return Helper.NIBBLE_TO_INT[int(n) & 0xf]

    @staticmethod
    def from_low_nibble_signed(n: int) -> int:
        return Helper.NIBBLE_TO_INT.index(clamp_nibble(n))

    @staticmethod
    def clamp16(val: int) -> int:
        if val > 32767:
            return 32767
        if val < -32768:
            return -32768
        return val
