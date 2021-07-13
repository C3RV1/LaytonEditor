# Ported from: https://github.com/pleonex/tinke by Cervi for Team Top Hat


class WaveFormat:
    EMPTY = 0
    WAVE_FORMAT_PCM = 0x0001
    IBM_FORMAT_ADPCM = 0x0002
    IBM_FORMAT_MULAW = 0x0007
    IBM_FORMAT_ALAW = 0x0006
    WAVE_FORMAT_EXTENSIBLE = 0xFFFE


class FmtChunk:
    def __init__(self):
        self.chunk_id = bytes()
        self.chunk_size = 0
        self.audio_format = WaveFormat.EMPTY
        self.num_channels = 0
        self.sample_rate = 0
        self.byte_rate = 0
        self.block_align = 0
        self.bits_per_sample = 0

    def copy(self):
        new_fmt_chunk = FmtChunk()
        new_fmt_chunk.chunk_id = self.chunk_id
        new_fmt_chunk.chunk_size = self.chunk_size
        new_fmt_chunk.audio_format = self.audio_format
        new_fmt_chunk.num_channels = self.num_channels
        new_fmt_chunk.sample_rate = self.sample_rate
        new_fmt_chunk.byte_rate = self.byte_rate
        new_fmt_chunk.block_align = self.block_align
        new_fmt_chunk.bits_per_sample = self.bits_per_sample
        return new_fmt_chunk


class DataChunk:
    def __init__(self):
        self.chunk_id = bytes()
        self.chunk_size = 0
        self.data = list()

    def copy(self):
        new_data_chunk = DataChunk()
        new_data_chunk.chunk_id = self.chunk_id
        new_data_chunk.chunk_size = self.chunk_size
        new_data_chunk.data = self.data
        return new_data_chunk


class WaveChunk:
    def __init__(self):
        self.fmt = FmtChunk()
        self.data = DataChunk()

    def copy(self):
        new_wave_chunk = WaveChunk()
        new_wave_chunk.fmt = self.fmt.copy()
        new_wave_chunk.data = self.data.copy()
        return new_wave_chunk


class sWAV:
    def __init__(self):
        self.file_id = 0
        self.chunk_id = str()
        self.chunk_size = 0
        self.format = str()
        self.wave = WaveChunk()
        self.loop_flag = 0
        self.loop_offset = 0

    def copy(self):
        new_wav = sWAV()
        new_wav.file_id = self.file_id
        new_wav.chunk_id = self.chunk_id
        new_wav.chunk_size = self.chunk_size
        new_wav.format = self.format
        new_wav.wave = self.wave.copy()
        new_wav.loop_flag = self.loop_flag
        new_wav.loop_offset = self.loop_offset
        return new_wav
