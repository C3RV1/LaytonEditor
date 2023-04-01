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
        self.nazo_lst = {}
        super(NazoListDlz, self).__init__(*args, **kwargs)

    def __getitem__(self, item):
        if item in self.nazo_lst:
            return self.nazo_lst[item][1]
        raise IndexError()

    def __setitem__(self, key, value):
        self.nazo_lst[key][1] = value

    def read_stream(self, stream: BinaryIO):
        super(NazoListDlz, self).read_stream(stream)
        unpacked_data = self.unpack("<hh48sh")
        for id_, *values in unpacked_data:
            self.nazo_lst[id_] = list(values)
        
    def write_stream(self, stream: BinaryIO):
        packed_data = []
        for key, values in self.nazo_lst.items():
            packed_data.append([key] + values)
        self.pack("<hh48sh", packed_data)
        super(NazoListDlz, self).write_stream(stream)


class SoundProfile:
    def __init__(self, music_id, unk0, unk1):
        self.music_id = music_id
        self.unk0 = unk0
        self.unk1 = unk1

    @classmethod
    def from_list(cls, lst):
        return cls(lst[0], lst[1], lst[2])

    def to_list(self):
        return [self.music_id, self.unk0, self.unk1]


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


class EventInf2Dlz(Dlz):
    def __init__(self, *args, **kwargs):
        self.event_inf: Dict[int, list] = {}
        super(EventInf2Dlz, self).__init__(*args, **kwargs)

    def __getitem__(self, item):
        if item not in self.event_inf:
            logging.warning(f"Event {item} not found in ev_inf2.dlz")
            return 0
        return self.event_inf[item][1]

    def __setitem__(self, key, value):
        if key not in self.event_inf:
            self.event_inf[key] = [0, 0, "\xff" * 6]
        self.event_inf[key][1] = value

    def pop(self, key, default=None):
        return self.event_inf.pop(key, default)

    def get(self, key, default=None):
        return self.event_inf.get(key, default)

    def read_stream(self, stream: BinaryIO):
        super(EventInf2Dlz, self).read_stream(stream)
        unpacked_data = self.unpack("<HHH6s")  # e_id, unk0, snd_profile, unk1...6 TODO: figure out other
        for ev_data in unpacked_data:
            self.event_inf[ev_data[0]] = list(ev_data[1:])

    def write_stream(self, stream: BinaryIO):
        constructed = []
        for ev_id, sound_id in self.event_inf.items():
            constructed.append([ev_id] + sound_id)
        constructed.sort(key=lambda x: x[0])
        self.pack("<HHH6s", constructed)
        super(EventInf2Dlz, self).write_stream(stream)


class TimeDefinitionsDlz(Dlz):  # tm_def.dlz
    def __init__(self, *args, **kwargs):
        self.time_definitions = {}
        super().__init__(*args, **kwargs)

    def __len__(self):
        return len(self.time_definitions)

    def __getitem__(self, item):
        if item not in self.time_definitions:
            logging.warning(f"Time definition {item} not found in tm_def.dlz")
            return 0
        return self.time_definitions[item]

    def __setitem__(self, key, value):
        self.time_definitions[key] = value

    def index_key(self, i):
        keys = self.time_definitions.keys()
        return list(keys)[i]

    def read_stream(self, stream: BinaryIO):
        super().read_stream(stream)
        unpacked_data = self.unpack("<HH")  # e_id, id, time_frames TODO: figure out other
        for tm_def in unpacked_data:
            self.time_definitions[tm_def[0]] = tm_def[1]

    def write_stream(self, stream: BinaryIO):
        constructed = []
        for tm_def_id, frames in self.time_definitions.items():
            constructed.append([tm_def_id, frames])
        constructed.sort(key=lambda x: x[0])
        self.pack("<HH", constructed)
        super().write_stream(stream)
