import ndspy.lz10 as lz10
from LaytonLib.binary import BinaryReader, BinaryWriter

LZ10 = 0x10
RLE = 0x30
HUFF8BIT = 0x28


# Mostly copied from Tinke
class rle():
    @staticmethod
    def decompress(data):
        rdr = BinaryReader(data)
        wtr = BinaryWriter()
        type = rdr.readU8()
        if type != 0x30:
            raise Exception("Tried to decompress commands that isn't RLE")
        ds = rdr.readU8() + rdr.readU16() << 8  # Decompressed size we dont care
        # about unless it's 0
        if ds == 0:
            rdr.readU32()

        while True:
            try:  # Test if we've run out of commands
                flag = rdr.readU8()
            except IndexError:  # If we have, nice, cause we're done!
                break
            compressed = (flag & 0x80) > 0
            lenght = flag & 0x7f
            lenght += 3 if compressed else 1
            if compressed:
                next = rdr.readU8()
                for i in range(lenght):
                    wtr.writeU8(next)
            else:
                wtr.write(rdr.readBytes(lenght))

        return wtr.data


class HuffTreeNode:
    def __init__(self, rdr: BinaryReader, isData: bool, relOffset, maxStreamPos):
        self.isData = isData
        self.parent = None
        if rdr.c >= maxStreamPos:
            self.isFilled = False
            return
        self.isFilled = True
        self.data = rdr.readU8()
        if not isData:
            offset = self.data & 0x3F
            zeroIsData = (self.data & 0x80) > 0
            oneIsData = (self.data & 0x40) > 0

            # off AND NOT == off XOR (off AND 1)
            zeroRelOffset = (relOffset ^ (relOffset & 1)) + offset * 2 + 2

            currStreamPos = rdr.c

            rdr.c += (zeroRelOffset - relOffset) - 1

            # Node after 0
            self.child0 = HuffTreeNode(
                rdr, zeroIsData, zeroRelOffset, maxStreamPos)
            self.child0.parent = self
            # Node after 1 directly located after the node after 0
            self.child1 = HuffTreeNode(
                rdr, oneIsData, zeroRelOffset + 1, maxStreamPos)
            self.child1.parent = self

            # reset stream
            rdr.c = currStreamPos


# Mostly copied from Tinke
class huff8bit():
    @staticmethod
    def decompress(data: bytes):
        rdr = BinaryReader(data)
        wtr = BinaryWriter()
        type = rdr.readU8()
        if type != 0x28:
            raise Exception("Tried to decompress commands that isn't Huffman")

        ds = rdr.readU8() + (rdr.readU16() << 8)

        if ds == 0:
            ds = rdr.readU32()

        # Read the tree
        treesize = (rdr.readU8() + 1) * 2
        tree_end = (rdr.c - 1) + treesize
        rootNode = HuffTreeNode(rdr, False, 5, tree_end)
        rdr.c = tree_end

        # Decompress with the tree
        bitsleft = 0  # amount of bits left to read from {commands}
        current_size = 0
        currentNode = rootNode

        while (current_size < ds):
            # Find next refrence to commands node
            while not currentNode.isData:
                if bitsleft == 0:
                    data = rdr.readU32()
                    bitsleft = 32

                bitsleft-=1
                nextIsOne = (data & (1 << bitsleft)) != 0
                if nextIsOne:
                    currentNode = currentNode.child1
                else:
                    currentNode = currentNode.child0

            wtr.writeU8(currentNode.data)
            current_size += 1
            currentNode = rootNode

        return wtr.data

def decompress(data: bytes):
    if int(data[0]) == LZ10:
        return lz10.decompress(data)
    elif int(data[0]) == RLE:
        return rle.decompress(data)
    elif int(data[0]) == HUFF8BIT:
        return huff8bit.decompress(data)
    else:
        raise Exception("Unsupported compression filetype with starting byte %s" % hex(data[0]))


def compress(data: bytes, type):
    if type == 0x10:
        return lz10.compress(data)
    else:
        raise Exception("Unsupported compression filetype with starting byte %s" % type)