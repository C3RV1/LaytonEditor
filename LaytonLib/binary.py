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

    def readU8List(self, len):
        out = [int(x) for x in self.data[self.c:self.c+len]]
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

    def readChars(self, len):
        out = str(self.data[self.c:self.c + len], encoding="ascii")
        self.c += len
        return out

    def readBytes(self, len):
        out = self.data[self.c:self.c + len]
        self.c += len
        return out

    def readFinal(self):
        return self.data[self.c:]

# Makes writing binaries easier
class BinaryWriter:
    def __init__(self):
        self.data = bytes()

    def writeU8(self, x):
        self.data += bytes([x&0xFF])

    def writeZeros(self, len):
        self.data += bytes([0,]*len)

    def writeU32(self, x):
        self.data += bytes([x&0xFF, x>>8&0xFF, x>>16&0xFF, x>>24&0xFF])

    def writeU16(self, x):
        self.data += bytes([x&0xFF, x>>8&0xFF])

    def write(self, data: (bytes, str)):
        if type(data) == str:
            data = bytes(data, "ascii")
        self.data += data

    def writeU8List(self, u8list: list):
        for l in u8list:
            self.writeU8(l)

    def writeU4List(self, u4list: list):
        if len(u4list) % 2 != 0:
            u4list.append(0)
        for i in range(0, len(u4list), 2):
            self.writeU8(join_U4(u4list[i+1], u4list[i]))

    def __len__(self):
        return len(self.data)

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

    def replU32(self, x, pos):
        while pos + 4 >= len(self.data):
            self.addZeros(4)
        self.data[pos] = x & 0xFF
        self.data[pos + 1] = x >> 8 & 0xFF
        self.data[pos + 2] = x >> 16 & 0xFF
        self.data[pos + 3] = x >> 24 & 0xFF

    def align(self, by):
        while len(self.data) % by:
            self.addU8(0)

# Splits byte into 2 u4
def split_byte(byte):
    low = byte & 0xf
    high = (byte >> 4) % 0xf
    return high, low

# Joins 2 u4 into one byte
def join_U4(high, low):
    return (high<<4) + low