import logging
import struct

from formats.binary import BinaryReader, BinaryWriter
from formats.dlz import Dlz


class SmInfEntry:
    def __init__(self, arrow_anim, arrow_x, arrow_y):
        self.arrow_anim = arrow_anim
        self.arrow_x = arrow_x
        self.arrow_y = arrow_y

    @classmethod
    def from_data(cls, data: bytes):
        arrow_anim, arrow_x, arrow_y, zero = struct.unpack("<BBBB", data)
        assert zero == 0
        return cls(arrow_anim, arrow_x, arrow_y)

    def to_data(self):
        return struct.pack("<BBBB", self.arrow_anim, self.arrow_x, self.arrow_y, 0)

    def __repr__(self):
        return f"SmInfEntry<anim={self.arrow_anim}, pos=({self.arrow_x}, {self.arrow_y})>"


class SmInfStoryStep(dict[int, SmInfEntry]):
    pass


class SmInfPlace(dict[int, SmInfStoryStep]):
    pass


class SmInfDlz(Dlz[int, SmInfPlace]):
    """
    This file contains the information about the arrows that guide you to the next
    goal. The entry id contains the information about
    - The place where the arrow should appear.
    - The story step when the arrow should appear.
    - An event viewed flag (0, 0x8a or 0x6d) for when the arrow should appear.
       (maybe through patching we can add more event viewed flags)

    To access the information about the arrow, use
    sm_inf[place_id][story_step][event_viewed_flag]
    """

    def read_entry(self, rdr: BinaryReader, entry_length):
        assert entry_length == 8
        entry_id = rdr.read_uint32()
        story_step = entry_id >> 0x10
        place_id = (entry_id >> 0x8) & 0xFF
        event_viewed_flag = entry_id & 0xFF

        if place_id not in self:
            self[place_id] = SmInfPlace()
        if story_step not in self[place_id]:
            self[place_id][story_step] = SmInfStoryStep()
        if event_viewed_flag in self[place_id][story_step]:
            logging.warning(f"Duplicate entry {story_step}, {place_id}, {event_viewed_flag} in SmInf, ignoring.")
            return
        self[place_id][story_step][event_viewed_flag] = SmInfEntry.from_data(rdr.read(4))

    def write_stream(self, stream):
        if isinstance(stream, BinaryWriter):
            wtr = stream
        else:
            wtr = BinaryWriter(stream)

        # Flatten the structure, merging all the parts down into a single entry_id
        flattened = []
        for place_id, place in self.items():
            place: SmInfPlace
            for story_step_id, story_step in place.items():
                story_step: SmInfStoryStep
                for event_viewed_flag, entry in story_step.items():
                    entry: SmInfEntry
                    entry_id = story_step_id << 0x10
                    entry_id += place_id << 0x8
                    entry_id += event_viewed_flag
                    flattened.append(
                        (entry_id, entry.to_data())
                    )

        flattened.sort(key=lambda x: x[0])

        wtr.write_uint16(len(flattened))
        wtr.write_uint16(8)
        wtr.write_uint16(8)  # Size of each entry
        wtr.write_uint16(0)
        wtr.write_uint16(0)

        for entry_id, entry_data in flattened:
            wtr.write_uint32(entry_id)
            if len(entry_data) != 4:
                raise ValueError("Entry must be 4 bytes (not counting id).")
            wtr.write(entry_data)
