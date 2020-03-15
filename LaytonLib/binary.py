import struct


# Makes reading binaries easier
class BinaryReader:
    def __init__(self, data: (bytes, str)):
        self.data = bytes(data)
        self.c = 0

    def readU8(self):
        out = int(self.data[self.c])
        self.c += 1
        return out

    def readU16(self):
        out = int(self.data[self.c] + self.data[self.c + 1] * 256)
        self.c += 2
        return out

    def readU32(self):
        out = self.data[self.c] + self.data[self.c + 1] * 256 + self.data[self.c + 2] * 256 ** 2 + self.data[
            self.c + 3] * 256 ** 3
        self.c += 4
        return out

    def readU8_at(self, at):
        out = int(self.data[at])
        return out

    def readU16_at(self, at):
        out = int(self.data[at] + self.data[at + 1] * 256)
        return out

    def readU32_at(self, at):
        out = self.data[at] + self.data[at + 1] * 256 + self.data[at + 2] * 256 ** 2 + self.data[
            at + 3] * 256 ** 3
        return out

    def readU8List(self, len):
        out = [int(x) for x in self.data[self.c:self.c + len]]
        self.c += len
        return out

    def readU4List(self, len):
        outd = [split_byte(int(x)) for x in self.data[self.c:self.c + len]]
        out = []
        for u in outd:
            out.append(u[1])
            out.append(u[0])
        self.c += len
        return out

    def readChars(self, len, zeroterminated=True):
        out = str(self.data[self.c:self.c + len], encoding="ascii")
        self.c += len
        if zeroterminated: out = out.split("\0")[0]
        return out

    def readBytes(self, len):
        out = self.data[self.c:self.c + len]
        self.c += len
        return out

    def readFinal(self):
        return self.data[self.c:]

    def readString(self):
        string = ""
        while self.data[self.c] != 0:
            string += self.readChars(1)
        self.c += 1
        return string

    def readFloat(self):
        return struct.unpack("f", self.readBytes(4))[0]

    def readS8(self):
        return int.from_bytes(self.readBytes(1), "little", signed=True)

    def readS16(self):
        return int.from_bytes(self.readBytes(2), "little", signed=True)

    def readS32(self):
        return int.from_bytes(self.readBytes(4), "little", signed=True)


# Makes writing binaries easier
class BinaryWriter:
    def __init__(self):
        self.data = bytes()

    def writeU8(self, x):
        self.data += bytes([x & 0xFF])

    def writeZeros(self, len):
        self.data += bytes([0, ] * len)

    def writeMultiple(self, x, len):
        self.data += bytes([x, ] * len)

    def writeU32(self, x):
        self.data += bytes([x & 0xFF, x >> 8 & 0xFF, x >> 16 & 0xFF, x >> 24 & 0xFF])

    def writeU16(self, x):
        self.data += bytes([x & 0xFF, x >> 8 & 0xFF])

    def write(self, data: (bytes, str)):
        if type(data) == str:
            data = bytes(data, "ascii")
        self.data += data

    def writeU8List(self, u8list: list):
        for l in u8list:
            self.writeU8(l)

    def writeU16List(self, u16list: list):
        for l in u16list:
            self.writeU16(l)

    def writeU4List(self, u4list: list):
        if len(u4list) % 2 != 0:
            u4list.append(0)
        for i in range(0, len(u4list), 2):
            self.writeU8(join_U4(u4list[i + 1], u4list[i]))

    def __len__(self):
        return len(self.data)

    def align(self, by, pad=0):
        while len(self.data) % by:
            self.writeU8(pad)

    def writeFloat(self, x: float):
        self.write(struct.pack("f", x))

    def writeChars(self, chars, lenght, pad=0, zero_terminated=True):
        self.write(chars[:lenght - (1 if zero_terminated else 0)])
        if zero_terminated: self.writeU8(0)
        if len(chars)  - (1 if zero_terminated else 0) < lenght: self.writeMultiple( pad,
            lenght - len(chars) - (1 if zero_terminated else 0))

    def writeString(self, string):
        self.write(string)
        self.writeU8(0)

    def writeS8(self, x: int):
        self.write(x.to_bytes(1, "little", signed=True))

    def writeS16(self, x: int):
        self.write(x.to_bytes(2, "little", signed=True))

    def writeS32(self, x: int):
        self.write(x.to_bytes(4, "little", signed=True))


# Makes editing binaries easier
class BinaryEditor:
    def __init__(self, data: bytes):
        self.data = data

    def addU8(self, x):
        self.data += bytes([x & 0xFF])

    def addZeros(self, lenght):
        self.data += bytes([0, ] * lenght)

    def addU32(self, x):
        self.data += bytes([x & 0xFF, x >> 8 & 0xFF, x >> 16 & 0xFF, x >> 24 & 0xFF])

    def addU16(self, x):
        self.data += bytes([x & 0xFF, x >> 8 & 0xFF])

    def add(self, data: (bytes, str)):
        if type(data) == str:
            data = bytes(data, "ascii")
        self.data += data

    def readU8(self, at):
        out = int(self.data[at])
        return out

    def readU16(self, at):
        out = int(self.data[at] + self.data[at + 1] * 256)
        return out

    def readU32(self, at):
        out = self.data[at] + self.data[at + 1] * 256 + self.data[at + 2] * 256 ** 2 + self.data[
            at + 3] * 256 ** 3
        return out

    def replU8(self, x, pos):
        while pos >= len(self.data):
            self.addZeros(1)
        self.data = bytearray(self.data)
        self.data[pos] = x & 0xFF
        self.data = bytes(self.data)

    def replU16(self, x, pos):
        while pos + 1 >= len(self.data):
            self.addZeros(1)
        self.data = bytearray(self.data)
        self.data[pos] = x & 0xFF
        self.data[pos + 1] = x >> 8 & 0xFF
        self.data = bytes(self.data)

    def replU32(self, x, pos):
        while pos + 3 >= len(self.data):
            self.addZeros(1)
        self.data = bytearray(self.data)
        self.data[pos] = x & 0xFF
        self.data[pos + 1] = x >> 8 & 0xFF
        self.data[pos + 2] = x >> 16 & 0xFF
        self.data[pos + 3] = x >> 24 & 0xFF
        self.data = bytes(self.data)

    def readChars(self, pos, len):
        return str(self.data[pos:pos + len], "ascii")

    def replChars(self, x, pos, len):
        x = bytes(x[:len], "ascii")
        while (len(x)) < len:
            x += 0x0
        self.data[pos:pos + len] = x

    def align(self, by):
        while len(self.data) % by:
            self.addU8(0)

    def __len__(self):
        return len(self.data)


# Splits byte into 2 u4
def split_byte(byte):
    low = byte & 0xf
    high = (byte >> 4) % 0xf
    return high, low


# Joins 2 u4 into one byte
def join_U4(high, low):
    return (high << 4) + low


class BitReader(BinaryReader):
    def __init__(self, stream: bytes):
        super().__init__(stream)
        self.bitpos = 0
        self.last = 0

    def resetBits(self):
        self.bitpos = 0

    def Pop(self):
        if (self.bitpos % 16 == 0):
            self.last = self.readU16()
        else:
            self.last = (self.last << 1) & 0xffff
        self.bitpos += 1
        return 1 if self.last & 0x8000 > 0 else 0

    def PopInt(self, n):
        value = 0
        for i in range(n):
            value = 2 * value + self.Pop()
        return value
