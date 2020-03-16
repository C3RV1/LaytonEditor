from LaytonLib.binary import *
from LaytonLib.sound.vars import *

class SMD_Event:
    def __init__(self):
        self.opp = 0
        self.vars = []

    @classmethod
    def from_reader(cls, rdr: BinaryReader, opp):
        self = cls()
        self.opp = opp
        self.vars = rdr.readU8List(n_vars[opp])
        return self

class SMD_PlayNoteEvent(SMD_Event):
    @classmethod
    def from_reader(cls, rdr: BinaryReader, opp):
        self = cls()
        self.opp = opp
        note_dat = rdr.readU8()
        nb_params = (note_dat & 0b11000000) >> 6
        self.vars = [note_dat, *rdr.readU8List(nb_params)]
        return self


class SMD_Track:
    def __init__(self):
        self.ID = 0
        self.ChannelID = 0
        self.Events = []

    def from_reader(self, global_reader: BinaryReader):
        global_reader.c += 12
        c_len = global_reader.readU32()
        chunk = global_reader.readBytes(c_len)
        global_reader.c += 4 - (global_reader.c % 4) if global_reader.c % 4 else 0

        rdr = BinaryReader(chunk)
        self.ID = rdr.readU8()
        self.ChannelID = rdr.readU8()
        rdr.c += 0x2

        while rdr.c < len(chunk):
            opp = rdr.readU8()
            if opp < 0x80:
                self.Events.append(SMD_PlayNoteEvent.from_reader(rdr, opp))
            else:
                self.Events.append(SMD_Event.from_reader(rdr, opp))
            if opp == 0x98:
                break
        else:
            raise Exception("Track did not finish on 0x98")

class SMD_Parser:
    def __init__(self):
        self.Unk0xE = 0
        self.Unk0xF = 0
        self.Year = 0
        self.Month = 0
        self.Day = 0
        self.Hour = 0
        self.Minute = 0
        self.Second = 0
        self.Label = ""

        self.TicksPerQuarterNote = 48
        self.n_channels = 0

        self.Tracks = []

    @classmethod
    def from_data(cls, data):
        self = cls()
        rdr = BinaryReader(data)
        rdr.c += 0xE
        self.Unk0xE = rdr.readU8()
        self.Unk0xF = rdr.readU8()
        rdr.c += 0x8
        self.Year = rdr.readU16()
        self.Month = rdr.readU8()
        self.Day = rdr.readU8()
        self.Hour = rdr.readU8()
        self.Minute = rdr.readU8()
        self.Second = rdr.readU8()
        rdr.c += 1
        self.Label = rdr.readChars(16)
        rdr.c += 0x10

        # Song Data
        rdr.c += 0x12
        self.TicksPerQuarterNote = rdr.readU16()
        rdr.c += 0x2
        nb_tracks = rdr.readU8()
        self.n_channels = rdr.readU8()
        rdr.c += 0x40 - 0x18

        for i in range(nb_tracks):
            track = SMD_Track()
            track.from_reader(rdr)
            self.Tracks.append(track)

    def to_data(self):
        wtr = BinaryWriter()
        wtr.write("smdl")
        wtr.writeZeros(4)
        wtr.writeU32(0) # TODO: Calculate File Lenght
        wtr.writeU8(self.Unk0xE)
        wtr.writeU8(self.Unk0xF)
        wtr.writeZeros(8)
        wtr.writeU16(self.Year)
        wtr.writeU8(self.Month)
        wtr.writeU8(self.Day)
        wtr.writeU8(self.Hour)
        wtr.writeU8(self.Minute)
        wtr.writeU8(self.Second)
        wtr.writeU8(0)
        wtr.writeChars(self.Label, 16, 0xaa)
        wtr.writeU32(1)
        wtr.writeU32(1)
        wtr.writeU32(0xFFFFFFFF)
        wtr.writeU32(0xFFFFFFFF)
        wtr.write("song")
        wtr.writeU32(1)
        wtr.writeU32(0xFF10)
        wtr.writeU32(0xFFFFFFB0)
        wtr.writeU16(0x1)
        
