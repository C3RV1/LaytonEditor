# Ported from: https://github.com/pleonex/tinke by Cervi for Team Top Hat

from cint.cint import I32, I8, U8, U16
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
    PROC_COEF = [bytearray(b"\x00\x00"),
                 bytearray(b"\x3c\x00"),
                 bytearray(b"\x73\xcc"),
                 bytearray(b"\x62\xc9"),
                 bytearray(b"\x7a\xc4")]

    @staticmethod
    def decode(encoded: bytearray, offset: int, samples_to_do: int, hist: list) -> np.ndarray:
        buffer = np.zeros(shape=(samples_to_do,))

        pos = offset + 15
        header = encoded[pos]
        header = header ^ 0x80
        scale = 12 - (header & 0xf)
        coef_index = (header >> 4) & 0xf

        if coef_index > 4:
            coef_index = 0
        coef1 = ((Procyon.PROC_COEF[coef_index][0] + 128) % 256) - 128
        coef2 = ((Procyon.PROC_COEF[coef_index][1] + 128) % 256) - 128

        for i in range(samples_to_do):
            pos = offset + i // 2
            sample_byte = encoded[int(pos)] ^ 0x80
            sample_byte = ((sample_byte + 128) % 256) - 128

            if i & 1 != 0:
                sample = Helper.get_high_nibble_signed(int(sample_byte))
            else:
                sample = Helper.get_low_nibble_signed(int(sample_byte))

            sample <<= 12
            sample = ((sample + 65536) % (1 << 32)) - 65536

            if scale < 0:
                sample <<= -scale
            else:
                sample >>= scale

            sample = (((hist[0] * coef1 + hist[1] * coef2) + 32) >> 6) + (sample << 6)
            sample = ((sample + 65536) % (1 << 32)) - 65536

            hist[1] = hist[0]
            hist[0] = sample

            clamp = Helper.clamp16((sample + 32) >> 6) >> 6 << 6

            buffer[i] = clamp

        return buffer

    @staticmethod
    def encode(decoded: bytearray, offset: int, hist: list, samples_to_do: int = 30):

        buffer = bytearray()
        scale = 7
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
