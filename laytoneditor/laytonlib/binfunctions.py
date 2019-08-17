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

    def readU8List(self, lenght):
        out = [int(x) for x in self.data[self.c:self.c+lenght]]
        self.c += lenght
        return out

    def readU4List(self, lenght):
        outd = [split_byte(int(x)) for x in self.data[self.c:self.c + lenght]]
        out = []
        for u in outd:
            out.append(u[1])
            out.append(u[0])
        self.c += lenght
        return out

    def readChars(self, lenght):
        out = str(self.data[self.c:self.c + lenght], encoding="ascii")
        self.c += lenght
        return out

class BinaryWriter:
    def __init__(self):
        self.data = bytes()

    def writeU8(self, x):
        self.data += bytes([x&0xFF])

    def writeZeros(self, lenght):
        self.data += bytes([0,]*lenght)

    def writeU32(self, x):
        self.data += bytes([x&0xFF, x>>8&0xFF, x>>16&0xFF, x>>24&0xFF])

    def writeU16(self, x):
        self.data += bytes([x&0xFF, x>>8&0xFF])

    def write(self, data: (bytes, str)):
        if type(data) == str:
            data = bytes(data, "ascii")
        self.data += data

    def writeU8List(self, u4list: list):
        for l in u4list:
            self.writeU8(l)

    def writeU4List(self, u4list: list):
        if len(u4list) % 2 != 0:
            u4list.append(0)
        for i in range(0, len(u4list), 2):
            self.writeU8(u4by4(u4list[i+1], u4list[i]))



def split_byte(byte):
    low = byte & 0xf
    high = (byte >> 4) % 0xf
    return high, low

def u4by4(high, low):
    return (high<<4) + low

def to_bin(integer, w=0):
    out = "{0:b}".format(integer)
    while len(out)<w:
        out = "0" + out
    return out