# Ported from: https://github.com/pleonex/tinke by Cervi for Team Top Hat

from cint.cint import I16, I32, I8, U8, U16
from ..Helper import Helper
from .PCM import BitConverter


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


def get_coef(d: bytearray):
    best_coef = 0
    coef_rating = 1000000000
    for coef in range(1, 5):
        tcoef = 0
        for v in range(len(d)):
            e = (v // BitConverter.from_bytes_short(Procyon.PROC_COEF[coef])) * BitConverter.from_bytes_short(Procyon.PROC_COEF[coef])
            tcoef += abs(v - e)
        if tcoef < coef_rating:
            best_coef = coef
            coef_rating = tcoef
    return best_coef


class Procyon:
    PROC_COEF = [bytearray(b"\x00\x00"),
                 bytearray(b"\x3c\x00"),
                 bytearray(b"\x73\xcc"),
                 bytearray(b"\x62\xc9"),
                 bytearray(b"\x7a\xc4")]

    @staticmethod
    def decode(encoded: bytearray, offset: int, samples_to_do: int, hist: list) -> bytearray:
        buffer = []

        pos = offset + 15
        header = I32(encoded[pos])
        header = header ^ 0x80
        scale = 12 - (header & 0xf)
        coef_index = (header >> 4) & 0xf

        if coef_index > 4:
            coef_index = 0
        coef1 = I8(Procyon.PROC_COEF[coef_index][0])
        coef2 = I8(Procyon.PROC_COEF[coef_index][1])

        for i in range(samples_to_do):
            pos = I32(offset + i // 2)
            sample_byte = I8(encoded[int(pos)] ^ 0x80)

            if i & 1 != 0:
                sample = I32(Helper.get_high_nibble_signed(int(sample_byte))) << 12
            else:
                sample = I32(Helper.get_low_nibble_signed(int(sample_byte))) << 12

            if scale < 0:
                sample <<= -scale
            else:
                sample >>= scale

            sample = I32((((hist[0] * coef1 + hist[1] * coef2) + 32) >> 6) + (sample << 6))
            hist[1] = hist[0]
            hist[0] = sample
            # print("{} {}".format(hist[0], hist[1]))

            # clamp = I16(Helper.clamp16((sample + 32) >> 6) >> 6 << 6)
            clamp = I16(Helper.clamp16((sample + 32) >> 6) >> 6 << 6)

            # buffer.append(BitConverter.get_bytes_short(clamp))
            buffer.append(int(clamp))

        return buffer

    @staticmethod
    def encode(decoded: bytearray, offset: int, hist: list, samples_to_do: int = 30,
               coef_index: int = 0, scale: int = 0):

        pos = offset
        buffer = bytearray()
        scale = 7
        # print(scale)
        # scale = 4
        # coef_index = sum(I8(BitConverter.from_bytes_short(decoded[n:n+2])) for n in range(pos, pos + samples_to_do, 2)) % 5
        coef_index = 0

        coef1 = I8(Procyon.PROC_COEF[coef_index][0])
        coef2 = I8(Procyon.PROC_COEF[coef_index][1])

        samp1 = 0

        # Encode wave data
        for i in range(samples_to_do):
            pos = offset + i * 2  # Every short
            clamp = I32(BitConverter.from_bytes_short(decoded[pos:pos+2]))
            sample = ((clamp >> 6 << 6) << 6) - 32

            hist1 = hist[0]
            hist0 = sample

            sample = (sample - (((hist[0] * coef1 + hist[1] * coef2) + 32) >> 6)) << 6

            hist[1] = hist1
            hist[0] = hist0

            if scale < 0:
                sample >>= -scale
            else:
                sample <<= scale

            if i & 1 == 0:  # Should pass to low nibble
                sample = Helper.from_low_nibble_signed((sample >> 12))
                samp1 = sample
            else:  # Should pass to high nibble
                sample = Helper.from_high_nibble_signed((sample >> 12))

                buffer.append(U8(samp1 + sample + 1) ^ 0x80)

        # add header
        header = (12 - scale) & 0xf
        header += coef_index << 4
        buffer.append(int(U8(header ^ 0x80)))
        return buffer
