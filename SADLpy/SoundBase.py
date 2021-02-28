# Ported from: https://github.com/pleonex/tinke by Cervi for Team Top Hat

from .WAV import *
from .binaryedit.binreader import *
from .binaryedit.binwriter import *
from .Compression import PCM


class SoundBase:
    def __init__(self, sound_file: str, id_: int, format_: str, copyright_: str, editable: bool):
        self._sound_file = sound_file
        self._id = id_
        self._format = format_
        self._copyright = copyright_
        self._editable = editable

        self._pcm16 = bytearray()
        self._pcm16_loop = bytearray()

        self._loop_enabled = True
        self._loop_begin_sample = 0
        self._loop_end_sample = 0

        self._total_samples = 0
        self._sample_rate = 0
        self._channels = 0
        self._block_size = 0
        self._sample_bit_depth = 0
        self._ignore_loop = False  # Ignore the loop if it does not need to be re-decoded

    @property
    def sound_file(self):
        return self._sound_file

    @property
    def format(self):
        return self._format

    @property
    def id(self):
        return self._id

    @property
    def copyright(self):
        return self._copyright

    @property
    def can_edit(self):
        return self._editable

    @property
    def can_loop(self):
        return self._loop_enabled

    @property
    def loop_begin(self):
        return self._loop_begin_sample

    @property
    def loop_end(self):
        return self._loop_end_sample

    @property
    def number_samples(self):
        return self._total_samples

    @property
    def sample_rate(self):
        return self._sample_rate

    @property
    def channels(self):
        return self._channels

    @property
    def block_size(self):
        return self._block_size

    @property
    def sample_bit_depth(self):
        return self._sample_bit_depth

    def initialize(self):
        encoded = self.read_file()
        return

        self._pcm16 = self.decode(encoded, False)
        if self._loop_enabled and not self._ignore_loop:
            self._pcm16_loop = self.decode(encoded, True)
        else:
            self._pcm16_loop = self._pcm16.copy()

    # Abstract
    def read_file(self) -> bytearray:
        raise NotImplementedError("read_file not implemented")

    # Abstract
    def decode(self, encoded: bytearray, loop_enabled: bool) -> bytearray:
        raise NotImplementedError("decode not implemented")

    def import_(self, file_in: str):
        wav = self.read_wav(file_in)
        self._pcm16 = wav.wave.data.data
        self._pcm16_loop = bytearray()

        self._total_samples = int(len(wav.wave.data.data) /
                                   ((wav.wave.fmt.bits_per_sample / 8) * wav.wave.fmt.num_channels))
        self._sample_rate = wav.wave.fmt.sample_rate
        self._channels = wav.wave.fmt.num_channels
        self._block_size = wav.wave.fmt.block_align
        self._sample_bit_depth = wav.wave.fmt.bits_per_sample

        self._loop_enabled = False
        self._loop_begin_sample = 0
        self._loop_end_sample = self._total_samples

    def write_file(self, file_out: str, data: bytearray):
        raise NotImplementedError("write_file not implemented")

    def encode(self) -> bytearray:
        return self._encode(self._pcm16)

    def _encode(self, data: bytearray) -> bytearray:
        raise NotImplementedError("encode not implemented")

    @staticmethod
    def read_wav(file_in: str) -> sWAV:
        wav =sWAV()

        br = BinaryReader(open(file_in, "rb"))

        # RIFF header
        wav.chunk_id = br.read_chars(4)
        wav.wave.chunk_size = br.read_uint32()
        wav.format = br.read_chars(4)
        if wav.chunk_id != b"RIFF" or wav.format != b"WAVE":
            raise NotImplementedError()

        # fmt sub-chunk
        wav.wave.fmt.chunk_id = br.read_chars(4)
        wav.wave.fmt.chunk_size = br.read_uint32()
        wav.wave.fmt.audio_format = br.read_uint16()
        wav.wave.fmt.num_channels = br.read_uint16()
        wav.wave.fmt.sample_rate = br.read_uint32()
        wav.wave.fmt.byte_rate = br.read_uint32()
        wav.wave.fmt.block_align = br.read_uint16()
        wav.wave.fmt.bits_per_sample = br.read_uint16()
        br.seek(0x14 + wav.wave.fmt.chunk_size)
        data_id = br.read_chars(4)
        while data_id != b"data":
            # br.seek(br.tell() + br.read_uint32() + 0x04)
            data_id = br.read_chars(4)

        # data sub-chunk
        br.seek(br.tell() - 4)
        wav.wave.data.chunk_id = br.read_chars(4)
        wav.wave.data.chunk_size = br.read_uint32()
        wav.wave.data.data = br.read_bytearray(wav.wave.data.chunk_size - 0x08)
        br.close()

        if wav.wave.fmt.audio_format != WaveFormat.WAVE_FORMAT_PCM:
            raise NotImplementedError()

        if wav.wave.fmt.audio_format == WaveFormat.WAVE_FORMAT_PCM and wav.wave.fmt.bits_per_sample == 0x08:
            wav.wave.fmt.bits_per_sample = 0x10
            wav.wave.fmt.block_align = wav.wave.fmt.num_channels * wav.wave.fmt.bits_per_sample / 8
            wav.wave.fmt.byte_rate = wav.wave.fmt.sample_rate * wav.wave.fmt.bits_per_sample * \
                                     wav.wave.fmt.num_channels / 8
            wav.wave.data.data = PCM.PCM.pcm8unsigned_to_pcm16(wav.wave.data.data)

        return wav

    def save_wav(self, file_out: str, loop: bool):
        byte_rate = int(self._sample_rate * 0x10 * self._channels / 8)
        block_align = int(self._channels * 0x10 / 8)

        bw = None
        try:
            bw = BinaryWriter(open(file_out, "wb"))

            bw.write_bytearray(bytearray(b"RIFF"))
            if loop:
                bw.write_uint32(0x28 + len(self._pcm16_loop))
            else:
                bw.write_uint32(0x28 + len(self._pcm16))

            bw.write_bytearray(bytearray(b"WAVE"))
            bw.write_bytearray(bytearray(b"fmt\x20"))
            bw.write_uint32(0x10)
            bw.write_uint16(0x01)
            bw.write_uint16(self._channels)
            bw.write_uint32(self._sample_rate)
            bw.write_uint32(byte_rate)
            bw.write_uint16(block_align)
            bw.write_uint16(0x10)

            bw.write_bytearray(bytearray(b"data"))
            if loop:
                bw.write_uint32(len(self._pcm16_loop))
                bw.write_bytearray(self._pcm16_loop)
            else:
                bw.write_uint32(len(self._pcm16))
                bw.write_bytearray(self._pcm16)
        except Exception as e:
            print("Exception (SoundBase) saving wav to: {}".format(file_out))
            print(str(e))
        finally:
            if bw:
                bw.close()

    # TODO: public Stream Get_Stream()
