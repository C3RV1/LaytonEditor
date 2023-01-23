from dataclasses import *
from typing import *

from formats.binary import *
from formats.filesystem import FileFormat


@dataclass
class PlaceHintcoin:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0


@dataclass
class PlaceExit:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    image_index: int = 0
    unk0: int = 0
    unk1: int = 0
    unk2: int = 0
    next_map_x: int = 0
    next_map_y: int = 0
    event_or_place_index: int = 0


@dataclass
class PlaceComment:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    character_index: int = 0
    text_index: int = 0


@dataclass
class PlaceSprite:
    x: int = 0
    y: int = 0
    filename: str = ""


@dataclass
class PlaceObject:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    character_index: int = 0
    event_index: int = 0
    unk: int = 0
    # Unk: 4 means it is a puzzle that is activated through the camera
    #      1 has something to do with the torn out photo pieces


class Place(FileFormat):
    index: int = 0
    map_x: int = 0
    map_y: int = 0
    background_image_index: int = 0
    map_image_index: int = 0
    sound_profile: int = 0
    hintcoins: List[PlaceHintcoin] = [PlaceHintcoin() for _ in range(4)]
    sprites: List[PlaceSprite] = [PlaceSprite() for _ in range(12)]
    objects: List[PlaceObject] = [PlaceObject() for _ in range(16)]
    comments: List[PlaceComment] = [PlaceComment() for _ in range(16)]
    exits: List[PlaceExit] = [PlaceExit() for _ in range(12)]

    _compressed_default = 0

    def read_stream(self, stream):
        # TODO: Polish
        rdr = stream if isinstance(stream, BinaryReader) else BinaryReader(stream)
        self.index = rdr.read_uint16()  # what does index represent?
        # missing data?
        rdr.seek(0x18)
        self.map_x = rdr.read_uint8()
        self.map_y = rdr.read_uint8()
        self.background_image_index = rdr.read_uint8()
        self.map_image_index = rdr.read_uint8()

        self.hintcoins: List[PlaceHintcoin] = [PlaceHintcoin() for _ in range(4)]
        self.sprites: List[PlaceSprite] = [PlaceSprite() for _ in range(12)]
        self.objects: List[PlaceObject] = [PlaceObject() for _ in range(16)]
        self.comments: List[PlaceComment] = [PlaceComment() for _ in range(16)]
        self.exits: List[PlaceExit] = [PlaceExit() for _ in range(12)]  # maybe it's 16 exits

        for hintcoin in self.hintcoins:
            hintcoin.x = rdr.read_uint8()
            hintcoin.y = rdr.read_uint8()
            hintcoin.width = rdr.read_uint8()
            hintcoin.height = rdr.read_uint8()
        # pos: 0x2c
        for comment in self.comments:
            comment.x = rdr.read_uint8()
            comment.y = rdr.read_uint8()
            comment.width = rdr.read_uint8()
            comment.height = rdr.read_uint8()
            comment.character_index = rdr.read_uint16()
            comment.text_index = rdr.read_uint16()
            rdr.read_uint16()  # 0
        # pos: 0xcc
        for sprite in self.sprites:
            sprite.x = rdr.read_uint8()
            sprite.y = rdr.read_uint8()
            sprite.filename = rdr.read_string(0x1e)
        # pos: 0x24c
        for plc_object in self.objects:
            plc_object.x = rdr.read_uint8()
            plc_object.y = rdr.read_uint8()
            plc_object.width = rdr.read_uint8()
            plc_object.height = rdr.read_uint8()
            plc_object.character_index = rdr.read_uint8()
            plc_object.unk = rdr.read_uint8()
            plc_object.event_index = rdr.read_uint16()
        # pos: 0x2cc
        for plc_exit in self.exits:
            plc_exit.x = rdr.read_uint8()
            plc_exit.y = rdr.read_uint8()
            plc_exit.width = rdr.read_uint8()
            plc_exit.height = rdr.read_uint8()
            plc_exit.image_index = rdr.read_uint8()
            plc_exit.unk0 = rdr.read_uint8()
            plc_exit.unk1 = rdr.read_uint8()
            plc_exit.unk2 = rdr.read_uint8()
            plc_exit.next_map_x = rdr.read_uint8()
            plc_exit.next_map_y = rdr.read_uint8()
            plc_exit.event_or_place_index = rdr.read_uint16()
        # pos: 0x35c (if we make 16 exits it lines up so...?)
        rdr.seek(0x38c)
        self.sound_profile = rdr.read_uint16()

    def write_stream(self, stream):
        wtr = BinaryWriter(stream)
        wtr.write_uint16(self.index)
        wtr.seek(0x18)
        wtr.write_uint8(self.map_x)
        wtr.write_uint8(self.map_y)
        wtr.write_uint8(self.background_image_index)
        wtr.write_uint8(self.map_image_index)
        for hintcoin in self.hintcoins:
            wtr.write_uint8(hintcoin.x)
            wtr.write_uint8(hintcoin.y)
            wtr.write_uint8(hintcoin.width)
            wtr.write_uint8(hintcoin.height)
        for comment in self.comments:
            wtr.write_uint8(comment.x)
            wtr.write_uint8(comment.y)
            wtr.write_uint8(comment.width)
            wtr.write_uint8(comment.height)
            wtr.write_uint16(comment.character_index)
            wtr.write_uint16(comment.text_index)
            wtr.write_uint16(0)
        for sprite in self.sprites:
            wtr.write_uint8(sprite.x)
            wtr.write_uint8(sprite.y)
            wtr.write_string(sprite.filename, 0x1e)
        for plc_object in self.objects:
            wtr.write_uint8(plc_object.x)
            wtr.write_uint8(plc_object.y)
            wtr.write_uint8(plc_object.width)
            wtr.write_uint8(plc_object.height)
            wtr.write_uint8(plc_object.character_index)
            wtr.write_uint8(plc_object.unk)
            wtr.write_uint16(plc_object.event_index)
        for plc_exit in self.exits:
            wtr.write_uint8(plc_exit.x)
            wtr.write_uint8(plc_exit.y)
            wtr.write_uint8(plc_exit.width)
            wtr.write_uint8(plc_exit.height)
            wtr.write_uint8(plc_exit.image_index)
            wtr.write_uint8(plc_exit.unk0)
            wtr.write_uint8(plc_exit.unk1)
            wtr.write_uint8(plc_exit.unk2)
            wtr.write_uint8(plc_exit.next_map_x)
            wtr.write_uint8(plc_exit.next_map_y)
            wtr.write_uint16(plc_exit.event_or_place_index)
        wtr.seek(0x38c)
        wtr.write_uint16(self.sound_profile)

