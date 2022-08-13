import math
import numpy as np


def change_sample_rate(buffer: np.ndarray, current, target) -> np.ndarray:
    shape = [0, 0]
    shape[0] = buffer.shape[0]

    # RATEo = SAMPLESo
    # RATEm = (SAMPLESo / RATEo) * RATEm
    extend = target / current
    shape[1] = int(math.ceil(buffer.shape[1] * extend))
    converted = np.zeros(shape, dtype=buffer.dtype)

    for channel in range(shape[0]):
        for dst_i in range(shape[1]):
            converted[channel][dst_i] = buffer[channel][int(dst_i // extend)]

    return converted


def change_channels(buffer: np.ndarray, target: int) -> np.ndarray:
    converted = np.ndarray(shape=(target, buffer.shape[1]), dtype=buffer.dtype)
    for i in range(target):
        if i < buffer.shape[0]:
            converted[i] = buffer[i]
        else:
            converted[i] = buffer[-1]
    return converted
