import logging
import struct
from typing import BinaryIO, Dict

from formats.binary import BinaryReader, BinaryWriter
from formats.filesystem import FileFormat


class Dlz(FileFormat):
    """
    DLZ file format on the Layton ROM.

    Each DLZ file consists of a binary structure repeated over and over.
    """
    _entries = list[bytes]

    _compressed_default = 1

    def read_stream(self, stream: BinaryIO):
        if isinstance(stream, BinaryReader):
            rdr = stream
        else:
            rdr = BinaryReader(stream)

        n_entries = rdr.read_uint16()
        header_length = rdr.read_uint16()
        entry_length = rdr.read_uint16()
        rdr.seek(header_length)

        self._entries = []

        for i in range(n_entries):
            self._entries.append(rdr.read(entry_length))

    def write_stream(self, stream: BinaryIO):
        if isinstance(stream, BinaryWriter):
            wtr = stream
        else:
            wtr = BinaryWriter(stream)

        wtr.write_uint16(len(self._entries))
        wtr.write_uint16(8)
        wtr.write_uint16(len(self._entries[0]))
        wtr.write_uint16(0)

        for entry in self._entries:
            wtr.write(entry)

    def unpack(self, __format: str):
        """
        Unpack the entries in the DLZ file according to a struct format.

        Parameters
        ----------
        __format : str
            The format of each entry as a `struct` module format.

        Returns
        -------
        List[Tuple]
            A list containing all the unpacked entries.
        """
        return [struct.unpack(__format, entry) for entry in self._entries]

    def pack(self, fmt, data: list):
        """
        Pack the supplied data entries according to a struct format.

        Parameters
        ----------
        fmt : str
            The format of each entry as a `struct` module format.
        data : List[Tuple]
            A list of the entries.

            Is entry is a structure following the format specified in the fmt parameter.
        """
        self._entries = [struct.pack(fmt, *entry_dat) for entry_dat in data]


class NazoListDlz(Dlz):
    def __init__(self, *args, **kwargs):
        self.nazo_lst = []
        super(NazoListDlz, self).__init__(*args, **kwargs)

    def __getitem__(self, item):
        for puz in self.nazo_lst:
            if puz[0] == item:
                return puz[2]
        raise IndexError()

    def __setitem__(self, key, value):
        for puz in self.nazo_lst:
            if puz[0] == key:
                puz[2] = value
                break
        else:
            logging.warning(f"Puzzle {key} not in NazoListDlz")

    def read_stream(self, stream: BinaryIO):
        super(NazoListDlz, self).read_stream(stream)
        self.nazo_lst = self.unpack("<hh48sh")
        
    def write_stream(self, stream: BinaryIO):
        self.pack("<hh48sh", self.nazo_lst)
        super(NazoListDlz, self).write_stream(stream)


class SoundProfile:
    def __init__(self, bg_music_id, unk0, unk1):
        self.bg_music_id = bg_music_id
        self.unk0 = unk0
        self.unk1 = unk1

    @classmethod
    def from_list(cls, lst):
        return cls(lst[0], lst[1], lst[2])

    def to_list(self):
        return [self.bg_music_id, self.unk0, self.unk1]


class SoundProfileDlz(Dlz):
    def __init__(self, *args, **kwargs):
        self.sound_profiles: Dict[int, SoundProfile] = {}
        super(SoundProfileDlz, self).__init__(*args, **kwargs)

    def __getitem__(self, item):
        return self.sound_profiles[item]

    def __setitem__(self, key, value):
        self.sound_profiles[key] = value

    def pop(self, key, default=None):
        return self.sound_profiles.pop(key, default)

    def index_key(self, i):
        keys = self.sound_profiles.keys()
        return list(keys)[i]

    def __len__(self):
        return len(self.sound_profiles)

    def read_stream(self, stream: BinaryIO):
        super(SoundProfileDlz, self).read_stream(stream)
        unpacked_data = self.unpack("<HHHH")
        for snd_profile in unpacked_data:
            self.sound_profiles[snd_profile[0]] = SoundProfile.from_list(snd_profile[1:])

    def write_stream(self, stream: BinaryIO):
        constructed = []
        for snd_id, snd_profile in self.sound_profiles.items():
            constructed.append([snd_id] + snd_profile.to_list())
        constructed.sort(key=lambda x: x[0])
        self.pack("<HHHH", constructed)
        super(SoundProfileDlz, self).write_stream(stream)


class EventLchDlz(Dlz):
    def __init__(self, *args, **kwargs):
        self.event_names: Dict[int, str] = {}
        super(EventLchDlz, self).__init__(*args, **kwargs)

    def __getitem__(self, item):
        return self.event_names[item]

    def __setitem__(self, key, value):
        self.event_names[key] = value

    def pop(self, key, default=None):
        return self.event_names.pop(key, default)

    def get(self, key, default=None):
        return self.event_names.get(key, default)

    def read_stream(self, stream: BinaryIO):
        super(EventLchDlz, self).read_stream(stream)
        unpacked_data = self.unpack("<I48s")
        for ev_data in unpacked_data:
            self.event_names[ev_data[0]] = ev_data[1].split(b'\0')[0].decode("shift-jis")

    def write_stream(self, stream: BinaryIO):
        constructed = []
        for ev_id, ev_name in self.event_names.items():
            constructed.append([ev_id, ev_name.encode("shift-jis").ljust(48, b'\0')])
        constructed.sort(key=lambda x: x[0])
        self.pack("<I48s", constructed)
        super(EventLchDlz, self).write_stream(stream)
