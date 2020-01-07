"""
Place File Library

Used to easily make changes to the place files.

Classes:

    Place: The base class used to make changes.
        functions:
        - import_data(data: bytes)
            imports the bytes of a place file for editing
        - export_data() -> bytes
            exports data to bytes that forms a place file

        properties:
        ID: the place ID, used by the game for identifying what place you're in.
        map_x: x location of the top map
        map_y: y location of the top map
        bg_bottom: ID of the image used on the bottom screen
        bg_top: ID of the image used on the top screen
        bg_music: ID of the music in the backgrounds
        raw: The Binary Editor used by the class's functions for manual editing

        lists:
        hintcoins [4]: List of 4 hintcoins a place can have (4 is max)
        bg_objects [12]: These are animated images displayed on the screen, they are not interactable.
        event_objects [16]: These are either an eventbox or a character. They are able to start events when clicked on.
        text_objects [16]: When clicked on these, luke, layton or whoever is assigned will display a textbox about something.
        place_exits [12]: These are visible when you click on the icon to walk and can start either events or move you to a
                     different place

    PlaceFile: Child class of both the Place and the File Class for ease of use.

    BgObject: Animated image displayed in the screen, not interactable
        properties:
            x, y: Coordinates of the image
            filename [30]: The image's filename

    EventObject: eventbox or character, start events
        event_id: ID of the event to start
        x, y: Coordinates of the character or eventbox
        x, y, width, height: bbox of the eventbox
        bgcharacter: What character you want to use, 0 is to use an eventbox
        unk: Still unknown

    TextObject: when clicked on, a little box will appear with luke or layton usually saying something about the scenery
        x, y, width, height: bbox of the object
        character_id: ID of the image used as character
        text_id: ID of the text being said
        unk: Still unknown

    PlaceExit: visible when you click on the icon to move around. Can start events or move you to a different place
        x, y, width, height: bbox of the button
        img: ID of image to use as button
        action: The action that is used when clicked on: 0 and 1 is to move to place, 2 is to start event
        unk[0-3]: Still unknown
        event: ID of the event to go through
        to_place_id: ID of the place to go through

    Hintcoin: Gives you a hintcoin when clicked on
        x, y: Coordinates
        id: id of the hintcoin
        unk: Still unknown

Example:

    from ndspy.rom import NintendoDSRom
    from LaytonLib.filesystem import PlzFile
    from LaytonLib.place import PlaceFile

    rom = NintendoDSRom.fromFile("../Base File.nds")
    archive = PlzFile(rom, rom.filenames.idOf("data_lt2/place/plc_data1.plz"))
    place = PlaceFile(archive, archive.idOf("n_place1_1.dat"))

    hintcoin_0 = place.hintcoins[0]
    hintcoin_0.x, hintcoin_0.y = 155, 166
    place.bg_bottom = 12

    place.save()
    archive.save()
    rom.saveToFile("../Test File.nds")
"""

from LaytonLib.binary import BinaryEditor
import LaytonLib.filesystem


class Place:
    def __init__(self):
        self.raw = BinaryEditor(bytes(0x38e))
        self.hintcoins = [Hintcoin(self, x) for x in range(4)]
        self.bg_objects = [BgObject(self, x) for x in range(12)]
        self.event_objects = [EventObject(self, x) for x in range(16)]
        self.text_objects = [TextObject(self, x) for x in range(16)]
        self.place_exits = [PlaceExit(self, x) for x in range(12)]

    def import_data(self, data: bytes):
        self.raw = BinaryEditor(data)

    def export_data(self) -> bytes:
        return self.raw.data

    @property
    def id(self):
        return self.raw.readU8(0)

    @id.setter
    def id(self, value):
        self.raw.replU8(value, 0)

    @property
    def map_x(self):
        return self.raw.readU8(0x18)

    @map_x.setter
    def map_x(self, value):
        self.raw.replU8(value, 0x18)

    @property
    def map_y(self):
        return self.raw.readU8(0x19)

    @map_y.setter
    def map_y(self, value):
        self.raw.replU8(value, 0x19)

    @property
    def bg_bottom(self):
        return self.raw.readU8(0x1a)

    @bg_bottom.setter
    def bg_bottom(self, value):
        self.raw.replU8(value, 0x1a)

    @property
    def bg_top(self):
        return self.raw.readU8(0x1b)

    @bg_top.setter
    def bg_top(self, value):
        self.raw.replU8(value, 0x1b)

    @property
    def bg_music(self):
        return self.raw.readU8(0x38c)

    @bg_music.setter
    def bg_music(self, value):
        self.raw.replU8(value, 0x38c)

class PlaceFile(Place, LaytonLib.filesystem.File):
    def __init__(self, romOrArchive, id):
        Place.__init__(self)
        LaytonLib.filesystem.File.__init__(self, romOrArchive, id)
        self.reload()

    def save(self):
        self.write(self.export_data())

    def reload(self):
        self.import_data(self.read())


class BgObject:
    def __init__(self, placefile: Place, infile_id):
        self._infile_id = infile_id
        self._place_file = placefile

    @property
    def x(self):
        return self._place_file.raw.readU8(0xcc + self._infile_id * 0x20)

    @x.setter
    def x(self, value):
        self._place_file.raw.replU8(value, 0xcc + self._infile_id * 0x20)

    @property
    def y(self):
        return self._place_file.raw.readU8(0xcd + self._infile_id * 0x20)

    @y.setter
    def y(self, value):
        self._place_file.raw.replU8(value, 0xcd + self._infile_id * 0x20)

    @property
    def filename(self):
        return self._place_file.raw.readChars(0xce + self._infile_id * 0x20, 0x1e)

    @filename.setter
    def filename(self, value):
        self._place_file.raw.replChars(value, 0xce + self._infile_id * 0x20, 0x1e)


class EventObject:
    def __init__(self, placefile: Place, infile_id):
        self._infile_id = infile_id
        self._place_file = placefile

    @property
    def event_id(self):
        return self._place_file.raw.readU16(0x252 + self._infile_id * 8)

    @event_id.setter
    def event_id(self, value):
        self._place_file.raw.replU16(value, 0x252 + self._infile_id * 8)

    @property
    def x(self):
        return self._place_file.raw.readU8(0x24C + self._infile_id * 8)

    @x.setter
    def x(self, value):
        self._place_file.raw.replU8(value, 0x24C + self._infile_id * 8)

    @property
    def y(self):
        return self._place_file.raw.readU8(0x24D + self._infile_id * 8)

    @y.setter
    def y(self, value):
        self._place_file.raw.replU8(value, 0x24D + self._infile_id * 8)

    @property
    def width(self):
        return self._place_file.raw.readU8(0x24E + self._infile_id * 8)

    @width.setter
    def width(self, value):
        self._place_file.raw.replU8(value, 0x24E + self._infile_id * 8)

    @property
    def height(self):
        return self._place_file.raw.readU8(0x24F + self._infile_id * 8)

    @height.setter
    def height(self, value):
        self._place_file.raw.replU8(value, 0x24F + self._infile_id * 8)

    @property
    def bgcharacter(self):
        return self._place_file.raw.readU8(0x250 + self._infile_id * 8)

    @bgcharacter.setter
    def bgcharacter(self, value):
        self._place_file.raw.replU8(value, 0x250 + self._infile_id * 8)

    @property
    def unk(self):
        return self._place_file.raw.readU8(0x251 + self._infile_id * 8)

    @unk.setter
    def unk(self, value):
        self._place_file.raw.replU8(value, 0x251 + self._infile_id * 8)


class TextObject:
    def __init__(self, placefile: Place, infile_id):
        self._infile_id = infile_id
        self._place_file = placefile

    @property
    def x(self):
        return self._place_file.raw.readU8(0x2C + self._infile_id * 10)

    @x.setter
    def x(self, value):
        self._place_file.raw.replU8(value, 0x2C + self._infile_id * 10)

    @property
    def y(self):
        return self._place_file.raw.readU8(0x2D + self._infile_id * 10)

    @y.setter
    def y(self, value):
        self._place_file.raw.replU8(value, 0x2D + self._infile_id * 10)

    @property
    def width(self):
        return self._place_file.raw.readU8(0x2E + self._infile_id * 10)

    @width.setter
    def width(self, value):
        self._place_file.raw.replU8(value, 0x2E + self._infile_id * 10)

    @property
    def height(self):
        return self._place_file.raw.readU8(0x2F + self._infile_id * 10)

    @height.setter
    def height(self, value):
        self._place_file.raw.replU8(value, 0x2F + self._infile_id * 10)

    @property
    def character_id(self):
        return self._place_file.raw.readU16(0x30 + self._infile_id * 10)

    @character_id.setter
    def character_id(self, value):
        self._place_file.raw.replU16(value, 0x30 + self._infile_id * 10)

    @property
    def text_id(self):
        return self._place_file.raw.readU16(0x32 + self._infile_id * 10)

    @text_id.setter
    def text_id(self, value):
        self._place_file.raw.replU16(value, 0x32 + self._infile_id * 10)

    @property
    def unk(self):
        return self._place_file.raw.readU16(0x34 + self._infile_id * 10)

    @unk.setter
    def unk(self, value):
        self._place_file.raw.replU16(value, 0x34 + self._infile_id * 10)


class PlaceExit:
    def __init__(self, placefile: Place, infile_id):
        self._infile_id = infile_id
        self._place_file = placefile

    @property
    def x(self):
        return self._place_file.raw.readU8(0x2cc + self._infile_id * 12)

    @x.setter
    def x(self, value):
        self._place_file.raw.replU8(value, 0x2cc + self._infile_id * 12)

    @property
    def y(self):
        return self._place_file.raw.readU8(0x2cd + self._infile_id * 12)

    @y.setter
    def y(self, value):
        self._place_file.raw.replU8(value, 0x2cd + self._infile_id * 12)

    @property
    def width(self):
        return self._place_file.raw.readU8(0x2ce + self._infile_id * 12)

    @width.setter
    def width(self, value):
        self._place_file.raw.replU8(value, 0x2ce + self._infile_id * 12)

    @property
    def height(self):
        return self._place_file.raw.readU8(0x2cf + self._infile_id * 12)

    @height.setter
    def height(self, value):
        self._place_file.raw.replU8(value, 0x2cf + self._infile_id * 12)

    @property
    def img(self):
        return self._place_file.raw.readU8(0x2d0 + self._infile_id * 12)

    @img.setter
    def img(self, value):
        self._place_file.raw.replU8(value, 0x2d0 + self._infile_id * 12)

    @property
    def action(self):
        return self._place_file.raw.readU8(0x2d1 + self._infile_id * 12)

    @action.setter
    def action(self, value):
        self._place_file.raw.replU8(value, 0x2d1 + self._infile_id * 12)

    @property
    def unk0(self):
        return self._place_file.raw.readU8(0x2d2 + self._infile_id * 12)

    @unk0.setter
    def unk0(self, value):
        self._place_file.raw.replU8(value, 0x2d2 + self._infile_id * 12)

    @property
    def unk1(self):
        return self._place_file.raw.readU8(0x2d3 + self._infile_id * 12)

    @unk1.setter
    def unk1(self, value):
        self._place_file.raw.replU8(value, 0x2d3 + self._infile_id * 12)

    @property
    def unk2(self):
        return self._place_file.raw.readU8(0x2d4 + self._infile_id * 12)

    @unk2.setter
    def unk2(self, value):
        self._place_file.raw.replU8(value, 0x2d4 + self._infile_id * 12)

    @property
    def unk3(self):
        return self._place_file.raw.readU8(0x2d5 + self._infile_id * 12)

    @unk3.setter
    def unk3(self, value):
        self._place_file.raw.replU8(value, 0x2d5 + self._infile_id * 12)

    @property
    def event(self):
        return self._place_file.raw.readU16(0x2d6 + self._infile_id * 12)

    @event.setter
    def event(self, value):
        self._place_file.raw.replU16(value, 0x2d6 + self._infile_id * 12)

    @property
    def to_place_id(self): # Located at same position as event
        return self.event

    @to_place_id.setter
    def to_place_id(self, value):
        self.event = value


class Hintcoin:
    def __init__(self, placefile: Place, infile_id):
        self._infile_id = infile_id
        self._place_file = placefile

    @property
    def x(self):
        return self._place_file.raw.readU8(0x1c + self._infile_id * 4)

    @x.setter
    def x(self, value):
        self._place_file.raw.replU8(value, 0x1c + self._infile_id * 4)

    @property
    def y(self):
        return self._place_file.raw.readU8(0x1d + self._infile_id * 4)

    @y.setter
    def y(self, value):
        self._place_file.raw.replU8(value, 0x1d + self._infile_id * 4)

    @property
    def id(self):
        return self._place_file.raw.readU8(0x1e + self._infile_id * 4)

    @id.setter
    def id(self, value):
        self._place_file.raw.replU8(value, 0x1e + self._infile_id * 4)

    @property
    def unk(self):
        return self._place_file.raw.readU8(0x1f + self._infile_id * 4)

    @unk.setter
    def unk(self, value):
        self._place_file.raw.replU8(value, 0x1f + self._infile_id * 4)
