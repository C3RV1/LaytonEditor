import os
import sys

# PyFluidSynth does not currently detect libfluidsynth-3.dll, but it can load it
# therefore before importing we briefly rename it to libfluidsynth-2.dll
# and then rename if back

directory = os.path.join(os.path.dirname(__file__), '../data_permanent/fluidsynth')

os.environ['PATH'] += ";" + directory

renamed = False
if os.path.isfile(os.path.join(directory, "libfluidsynth-3.dll")):
    renamed = True
    # Rename fluidsynth, otherwise pyfluidsynth won't be able to find it
    os.rename(os.path.join(directory, "libfluidsynth-3.dll"), os.path.join(directory, "libfluidsynth-2.dll"))

from fluidsynth import *

if renamed:
    os.rename(os.path.join(directory, "libfluidsynth-2.dll"), os.path.join(directory, "libfluidsynth-3.dll"))


def fluid_synth_write_s16_stereo_custom(synth, length):
    """Return generated samples in stereo 16-bit format

    Return value is a Numpy array of samples.

    """
    import numpy
    buf_left = create_string_buffer(length * 2)
    buf_right = create_string_buffer(length * 2)
    fluid_synth_write_s16(synth, length, buf_left, 0, 1, buf_right, 0, 1)
    return numpy.frombuffer(buf_left[:], dtype=numpy.int16), numpy.frombuffer(buf_right[:], dtype=numpy.int16)


class ModifiedSynth(Synth):
    def get_samples(self, length=1024):
        # Write samples into 2 buffers instead of 1
        return fluid_synth_write_s16_stereo_custom(self.synth, length)
