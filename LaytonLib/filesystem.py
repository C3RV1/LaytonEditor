from ndspy.rom import NintendoDSRom
from LaytonLib.compression import decompress, compress, LZ10
from LaytonLib.binary import *
from hexdump import hexdump


# Compressed Folder
class Plz:
    def __init__(self):
        self.filenames = []
        self.files = []

    def import_data(self, data: bytes):
        # clear self
        self.filenames = []
        self.files = []

        uncompressed = decompress(data)
        rdr = BinaryReader(uncompressed)

        headersize = rdr.readU32()
        filesize = rdr.readU32()
        pck2 = rdr.readChars(4)
        if pck2 != "PCK2":
            raise Exception("Not a PCK2 file")
        always0 = rdr.readU32()

        rdr.c = headersize

        # read all files
        while rdr.c < len(rdr.data):
            pos = rdr.c
            fileheadersize = rdr.readU32()
            size = rdr.readU32()
            rdr.c += 4
            data_size = rdr.readU32()

            filename = rdr.readString()

            rdr.c = pos + fileheadersize
            data = rdr.readBytes(data_size)
            rdr.c = pos + size

            # save the new file's data
            self.filenames.append(filename)
            self.files.append(data)

    def export_data(self):
        wtr = BinaryWriter()
        wtr.writeU32(16)  # Header is 16 bytes long
        wtr.writeU32(0) # placeholder for filesize
        wtr.write(b"PCK2")
        wtr.writeU32(0)

        for i in range(len(self.files)):
            headersize = 16 + len(self.filenames[i]) + 1
            if headersize % 4 != 0:
                headersize += 4 - headersize % 4
            wtr.writeU32(headersize)

            totalsize = headersize + len(self.files[i])
            if totalsize % 4 != 0:
                totalsize += 4 - totalsize % 4
            wtr.writeU32(totalsize)

            wtr.writeU32(0) # unknown zero

            data_size = len(self.files[i])
            wtr.writeU32(data_size)

            wtr.write(bytes(self.filenames[i], "ascii"))
            wtr.writeU8(0)

            wtr.align(4)

            wtr.write(self.files[i])

            wtr.align(4)

        wtr = BinaryEditor(wtr.data)
        wtr.replU32(len(wtr.data), 4)
        return compress(wtr.data, LZ10)

    def idOf(self, filename):
        return self.filenames.index(filename)


# Allows something to edit a certain file at any time
class File:
    def __init__(self, romOrArchive, id: int):
        self.romOrArchive = romOrArchive
        self._id: int = id

    @property
    def name(self):
        return self.romOrArchive.filenames[self._id]

    @name.setter
    def name(self, value: str):
        self.romOrArchive.filenames[self._id] = value

    def read(self):
        return self.romOrArchive.files[self._id]

    def write(self, data):
        self.romOrArchive.files[self._id] = data

    @property
    def id(self):
        return int(self._id)


class PlzFile(Plz, File):
    def __init__(self, romOrArchive, id):
        Plz.__init__(self)
        File.__init__(self, romOrArchive, id)
        self.reload()

    def save(self):
        self.write(self.export_data())

    def reload(self):
        self.import_data(self.read())
