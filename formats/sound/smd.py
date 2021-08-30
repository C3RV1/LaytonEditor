from typing import BinaryIO

from formats.binary import BinaryReader, BinaryWriter
from formats.filesystem import FileFormat
import io


class SMDLHeader:
    magic: bytes = b"smdl"
    file_length: int
    version: int = 0x1504
    unk1: int
    unk2: int
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    centisecond: int
    file_name: bytes

    def read(self, br: BinaryReader):
        br.seek(0, io.SEEK_SET)
        self.magic = br.read_string(4, encoding=None)
        if self.magic != b"smdl":
            raise ValueError("SMDHeader does not start with magic value")
        br.read_uint32()  # 0
        self.file_length = br.read_uint32()
        self.version = br.read_uint16()
        self.unk1 = br.read_uint8()
        self.unk2 = br.read_uint8()
        # 8 bytes of 0
        br.read_uint32()
        br.read_uint32()
        self.year = br.read_uint16()
        self.month = br.read_uint8()
        self.day = br.read_uint8()
        self.hour = br.read_uint8()
        self.minute = br.read_uint8()
        self.second = br.read_uint8()
        self.centisecond = br.read_uint8()
        self.file_name = br.read_string(16, encoding=None, pad=b"\xFF")
        br.read_uint32()  # 0x1
        br.read_uint32()  # 0x1
        br.read_uint32()  # 0xFFFFFFFF
        br.read_uint32()  # 0xFFFFFFFF

    def write(self, bw: BinaryWriter):
        bw.seek(0, io.SEEK_SET)
        bw.write_string(self.magic)
        bw.write_uint32(0)
        bw.write_uint32(self.file_length)
        bw.write_uint16(self.version)
        bw.write_uint8(self.unk1)
        bw.write_uint8(self.unk2)
        bw.write_uint32(0)
        bw.write_uint32(0)
        bw.write_uint16(self.year)
        bw.write_uint8(self.month)
        bw.write_uint8(self.day)
        bw.write_uint8(self.hour)
        bw.write_uint8(self.minute)
        bw.write_uint8(self.second)
        bw.write_uint8(self.centisecond)
        if self.file_name[-1] != 0:
            self.file_name += b"\0"
        bw.write_string(self.file_name, size=16, encoding=None, pad=b"\xFF")
        bw.write_uint32(0x1)
        bw.write_uint32(0x1)
        bw.write_uint32(0xFFFFFFFF)
        bw.write_uint32(0xFFFFFFFF)


class SongChunk:
    label: bytes = b"song"
    unk1: int
    tpqn: int = 0x30  # Ticks per quarter note
    unk5: int
    num_tracks: int
    num_channels: int
    unk6: int
    unk7: int
    unk8: int
    unk9: int
    unk10: int
    unk11: int
    unk12: int

    def read(self, br: BinaryReader):
        br.seek(0x40, io.SEEK_SET)
        self.label = br.read_string(4, encoding=None)
        if self.label != b"song":
            raise ValueError("SongChunk does not start with magic value")
        self.unk1 = br.read_uint32()
        br.read_uint32()  # 0xFF10
        br.read_uint32()  # 0xFFFFFFB0
        br.read_uint16()  # 0x1
        self.tpqn = br.read_uint16()
        br.read_uint16()  # 0xFF10
        self.num_tracks = br.read_uint8()
        self.num_channels = br.read_uint8()
        br.read_uint32()  # 0x0F000000
        br.read_uint32()  # 0xFFFFFFFF
        br.read_uint32()  # 0x40000000
        br.read_uint32()  # 0x00404000
        br.read_uint16()  # 0x0200
        br.read_uint16()  # 0x0800
        br.read_uint32()  # 0xFFFFFF00
        br.read_string(16, encoding=None)  # 16 0xFF Padding

    def write(self, bw: BinaryWriter):
        bw.seek(0x40, io.SEEK_SET)
        bw.write_string(self.label)
        bw.write_uint32(self.unk1)
        bw.write_uint32(0xFF10)
        bw.write_uint32(0xFFFFFFB0)
        bw.write_uint16(0x1)
        bw.write_uint16(self.tpqn)
        bw.write_uint16(0xFF01)
        bw.write_uint8(self.num_tracks)
        bw.write_uint8(self.num_channels)
        bw.write_uint32(0x0F000000)
        bw.write_uint32(0xFFFFFFFF)
        bw.write_uint32(0x40000000)
        bw.write_uint32(0x00404000)
        bw.write_uint16(0x0200)
        bw.write_uint16(0x0800)
        bw.write_uint32(0xFFFFFF00)
        bw.write_string(b"\xFF"*16)


class TrackChunkHeader:
    label: bytes = b"trk\x20"
    param1: int
    param2: int
    chunk_length = int

    def read(self, br: BinaryReader):
        self.label = br.read_string(4, encoding=None)
        if self.label != b"trk\x20":
            raise ValueError("TrackChunkHeader does not start with magic value")
        self.param1 = br.read_uint32()
        self.param2 = br.read_uint32()
        self.chunk_length = br.read_uint32()

    def write(self, bw: BinaryWriter):
        bw.write_string(self.label)
        bw.write_uint32(self.param1)
        bw.write_uint32(self.param2)
        bw.write_uint32(self.chunk_length)


class TrackPreamble:
    track_id: int
    channel_id: int
    unk1: int
    unk2: int

    def read(self, br: BinaryReader):
        self.track_id = br.read_uint8()
        self.channel_id = br.read_uint8()
        self.unk1 = br.read_uint8()
        self.unk2 = br.read_uint8()

    def write(self, bw: BinaryWriter):
        bw.write_uint8(self.track_id)
        bw.write_uint8(self.channel_id)
        bw.write_uint8(self.unk1)
        bw.write_uint8(self.unk2)


class TrackContent:
    event_bytes: bytes

    def read(self, br: BinaryReader, track_header: TrackChunkHeader):
        eb = br.read_char_array(track_header.chunk_length - 4)
        self.event_bytes = b"".join(eb)

    def write(self, bw: BinaryWriter):
        bw.write_char_array([bytes([x]) for x in list(self.event_bytes)])
        if offset := bw.tell() % 4:
            bw.write_char_array([b"\x98"]*(4 - offset))


class Track:
    track_header: TrackChunkHeader
    track_preamble: TrackPreamble
    track_content: TrackContent

    def read(self, br: BinaryReader):
        self.track_header = TrackChunkHeader()
        self.track_preamble = TrackPreamble()
        self.track_content = TrackContent()

        self.track_header.read(br)
        self.track_preamble.read(br)
        self.track_content.read(br, self.track_header)
        br.align(4)

    def write(self, bw: BinaryWriter):
        self.track_header.chunk_length = len(self.track_content.event_bytes) + 4
        self.track_header.write(bw)
        self.track_preamble.write(bw)
        self.track_content.write(bw)


class EOCChunk:
    label: bytes = b"eoc\x20"
    param1: int = 0x1
    param2: int = 0x04FF0000

    def read(self, br: BinaryReader):
        self.label = br.read_string(4, encoding=None)
        if self.label != b"eoc\x20":
            raise ValueError(f"EOCChunk does not start with magic value ({repr(self.label)}")
        self.param1 = br.read_uint32()
        self.param2 = br.read_uint32()
        br.read_uint32()  # 0

    def write(self, bw: BinaryWriter):
        bw.write_string(self.label)
        bw.write_uint32(self.param1)
        bw.write_uint32(self.param2)
        bw.write_uint32(0)


class SMDL(FileFormat):
    smdl_header: SMDLHeader
    song_chunk: SongChunk
    tracks = []
    eoc_chunk: EOCChunk

    def read_stream(self, stream: BinaryIO):
        if isinstance(stream, BinaryReader):
            rdr = stream
        else:
            rdr = BinaryReader(stream)
        self.smdl_header = SMDLHeader()
        self.song_chunk = SongChunk()
        self.tracks = []
        self.eoc_chunk = EOCChunk()

        self.smdl_header.read(rdr)
        self.song_chunk.read(rdr)
        for i in range(self.song_chunk.num_tracks):
            new_track = Track()
            new_track.read(rdr)
            self.tracks.append(new_track)
        self.eoc_chunk.read(rdr)

    def write_stream(self, stream):
        if isinstance(stream, BinaryWriter):
            wtr = stream
        else:
            wtr = BinaryWriter(stream)
        self.song_chunk.num_tracks = len(self.tracks)
        self.song_chunk.write(wtr)
        for track in self.tracks:
            track: Track
            track.write(wtr)
        self.eoc_chunk.write(wtr)
        self.smdl_header.file_length = wtr.tell()
        self.smdl_header.write(wtr)
        wtr.seek(0, io.SEEK_END)

    def write(self):
        pass

