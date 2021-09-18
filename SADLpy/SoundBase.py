# Ported from: https://github.com/pleonex/tinke by Cervi for Team Top Hat

from .WAV import *
from .binaryedit.binreader import *
from .binaryedit.binwriter import *
from .Compression import PCM
from .Helper import Helper
from .Compression.PCM import BitConverter
from io import BytesIO
from typing import Union


class SoundBase:
    def __init__(self, sound_file: str, id_: int, format_: str, copyright_: str, editable: bool):
        self._sound_file = sound_file
        self._id = id_
        self._format = format_
        self._copyright = copyright_
        self._editable = editable

        self._pcm16 = []

        self._loop_enabled = True
        self._loop_begin_sample = 0
        self._loop_end_sample = 0

        self._total_samples = 0
        self._sample_rate = 0
        self._channels = 0
        self._block_size = 0
        self._sample_bit_depth = 0
        self._ignore_loop = False  # Ignore the loop if it does not need to be re-decoded

    def create_objects(self):
        pass

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

    def initialize(self, decode_all=False):
        self.read_file()

        if not decode_all:
            return

        # Automatically copies to pcm16
        return self.decode()

    # Abstract
    def read_file(self, br: BinaryReader = None) -> bytearray:
        raise NotImplementedError("read_file not implemented")

    # Abstract
    def decode(self, sample_steps=-1) -> bytearray:
        raise NotImplementedError("decode not implemented")

    def import_(self, file_in: str):
        wav = self.read_wav(file_in)
        self._channels = wav.wave.fmt.num_channels
        self.create_objects()
        self._pcm16 = wav.wave.data.data

        self._total_samples = int(len(wav.wave.data.data[0]))
        self._sample_rate = wav.wave.fmt.sample_rate
        self._block_size = wav.wave.fmt.block_align
        self._sample_bit_depth = wav.wave.fmt.bits_per_sample

        self._loop_enabled = False
        self._loop_begin_sample = 0
        self._loop_end_sample = self._total_samples

    def write_file(self, file_out: Union[str, BytesIO], data: bytearray):
        raise NotImplementedError("write_file not implemented")

    def encode(self) -> bytearray:
        raise NotImplementedError("encode not implemented")

    @staticmethod
    def read_wav(file_in: str) -> sWAV:
        wav = sWAV()

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
        sample_rate = wav.wave.fmt.sample_rate
        wav.wave.fmt.byte_rate = br.read_uint32()
        wav.wave.fmt.block_align = br.read_uint16()
        wav.wave.fmt.bits_per_sample = br.read_uint16()
        br.seek(0x14 + wav.wave.fmt.chunk_size)
        data_id = br.read_chars(4)
        while data_id != b"data":
            offset = br.read_uint32()
            br.seek(br.tell() + offset)
            data_id = br.read_chars(4)

        # data sub-chunk
        br.seek(br.tell() - 4)
        wav.wave.data.chunk_id = br.read_chars(4)
        wav.wave.data.chunk_size = br.read_uint32()

        wav_data = br.read_bytearray(wav.wave.data.chunk_size)

        if wav.wave.fmt.num_channels == 2:
            print("Dividing stereo channels")
            wav_data = Helper.divide_channels(wav_data)
        else:
            print("Mono channel -> no division needed")
            wav_data = [wav_data]

        wav_data_lists = []
        convert_sample_rate = False
        target_sample_rate = sample_rate
        if sample_rate != 32728 and sample_rate != 16364:
            convert_sample_rate = True
            if sample_rate > 32728:
                target_sample_rate = 32728
            elif sample_rate > 16364:
                target_sample_rate = 16364
            else:
                raise ValueError(f"Cannot transform sample rate of {sample_rate} to an accepted sample rate")
        if convert_sample_rate:
            print(f"Reducing sample rate from {sample_rate} to {target_sample_rate}")
        print("Converting bytearrays to lists")
        for channel in wav_data:
            parsed = []
            for i in range(0, len(channel), 2):
                parsed.append(BitConverter.to_int_16(channel, i))
            if convert_sample_rate:
                parsed = Helper.reduce_sample_rate(parsed, sample_rate, target_sample_rate)
            wav_data_lists.append(parsed)
        wav.wave.fmt.sample_rate = target_sample_rate
        wav.wave.data.data = wav_data_lists

        br.close()

        if wav.wave.fmt.audio_format != WaveFormat.WAVE_FORMAT_PCM:
            raise NotImplementedError()

        if wav.wave.fmt.audio_format == WaveFormat.WAVE_FORMAT_PCM and wav.wave.fmt.bits_per_sample == 0x08:
            raise NotImplementedError()
            wav.wave.fmt.bits_per_sample = 0x10
            wav.wave.fmt.block_align = wav.wave.fmt.num_channels * wav.wave.fmt.bits_per_sample / 8
            wav.wave.fmt.byte_rate = wav.wave.fmt.sample_rate * wav.wave.fmt.bits_per_sample * \
                                     wav.wave.fmt.num_channels / 8
            wav.wave.data.data = PCM.PCM.pcm8unsigned_to_pcm16(wav.wave.data.data)

        return wav

    def save_wav(self, file_out: str):
        def convert_channel_to_bytearray(channel):
            converted = bytearray()
            for sample in channel:
                converted += BitConverter.get_bytes_short(int(sample))
            return converted

        byte_rate = int(self._sample_rate * 0x10 * self._channels / 8)
        block_align = int(self._channels * 0x10 / 8)

        bw = None
        try:
            bytearray_channel = list(map(lambda x: convert_channel_to_bytearray(x), self._pcm16))
            if self._channels == 2:
                bytearray_channel = Helper.merge_channels(bytearray_channel[0], bytearray_channel[1])
            else:
                bytearray_channel = bytearray_channel[0]

            bw = BinaryWriter(open(file_out, "wb"))

            bw.write_bytearray(bytearray(b"RIFF"))
            bw.write_uint32(0x28 + len(bytearray_channel))

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
            bw.write_uint32(len(bytearray_channel))
            bw.write_bytearray(bytearray_channel)
        except Exception as e:
            print("Exception (SoundBase) saving wav to: {}".format(file_out))
            print(str(e))
        finally:
            if bw:
                bw.close()

    # TODO: public Stream Get_Stream()
