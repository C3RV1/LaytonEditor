from formats.dlz import Dlz
import struct
from enum import IntEnum


class EventInf2Behaviour(IntEnum):
    NONE = 0  # TODO: Make sure
    HIDE_OBJECT_AFTER_EVENT_IS_PLAYED = 1
    INCREMENT_EVENT_ID_AFTER_PLAYED = 2
    UNK3 = 3  # TODO: Figure out
    HIDE_AFTER_PUZZLE_COMPLETED = 4
    PUZZLE_COUNT_BARRIER = 5
    PLAY_ON_ROOM_ENTER = 6  # TODO: Maybe?


class EventInf2Entry:
    def __init__(self, behaviour: EventInf2Behaviour, sound_fix_to_play: int,
                 puzzle_to_play: int, ev_viewed_flag: int, story_flag_to_set: int):
        self.behaviour: EventInf2Behaviour = behaviour
        self.sound_fix: int = sound_fix_to_play  # 0xFFFF means disabled TODO: Maybe?
        self.puzzle: int = puzzle_to_play  # 0xFFFF means disabled
        self.ev_viewed_flag: int = ev_viewed_flag  # TODO: Figure out
        self.story_flag: int = story_flag_to_set  # 0xFFFF means disabled

    @classmethod
    def from_data(cls, data: bytes):
        behaviour, snd_fix, pz, ev_viewed_flag, story_flag = struct.unpack(
            "<HHHHH", data
        )
        return cls(behaviour, snd_fix, pz, ev_viewed_flag, story_flag)

    def to_data(self) -> bytes:
        return struct.pack("<HHHHH", self.behaviour, self.sound_fix, self.puzzle,
                           self.ev_viewed_flag, self.story_flag)

    def __repr__(self):
        return f"EventInf2Entry<behaviour={self.behaviour}, sound_fix={self.sound_fix}, puzzle={self.puzzle}, " \
               f"ev_viewed_flag={self.ev_viewed_flag}, story_flag={self.story_flag}>"


class EventInf2Dlz(Dlz[int, EventInf2Entry]):
    def _construct_entry_object(self, entry_data: bytes) -> EventInf2Entry:
        return EventInf2Entry.from_data(entry_data)

    def _serialize_entry_object(self, entry_object: EventInf2Entry) -> bytes:
        return entry_object.to_data()
