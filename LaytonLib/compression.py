import ndspy.lz10 as lz10
from LaytonLib.binary import BinaryReader, BinaryWriter

LZ10 = 0x10
RLE = 0x30
HUFF8BIT = 0x28
HUFF4BIT = 0x24

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

    @staticmethod
    def compress(data):
        rdr = BinaryReader(data)
        wtr = BinaryWriter()
        wtr.writeU8(0x30)

        wtr.writeU8(len(data)&0xff)
        wtr.writeU16(len(data)>>8)

        readLenght = 0
        repCount = 1
        currentBlockLenght = 0
        dataBlock = [0 for _ in range(130)]
        while rdr.c < len(rdr.data):
            foundRepetition = False
            while (currentBlockLenght < 130 and rdr.c < len(rdr.data)):
                nextByte = rdr.readU8()
                readLenght+=1
                dataBlock[currentBlockLenght] = nextByte
                currentBlockLenght += 1
                if (currentBlockLenght > 1):
                    if nextByte == dataBlock[currentBlockLenght - 2]:
                        repCount += 1
                    else:
                        repCount = 1
                foundRepetition = repCount > 2
                if foundRepetition:
                    break
            numUncompToCopy = 0
            if foundRepetition:
                numUncompToCopy = currentBlockLenght - 3
            else:
                numUncompToCopy = min(currentBlockLenght, 130-2)

            if numUncompToCopy > 0:
                flag = numUncompToCopy - 1
                wtr.writeU8(flag)
                for i in range(numUncompToCopy):
                    wtr.writeU8(dataBlock[i])
                for i in range(numUncompToCopy, currentBlockLenght):
                    dataBlock[i - numUncompToCopy] = dataBlock[i]
                currentBlockLenght -= numUncompToCopy
            if foundRepetition:
                while currentBlockLenght < 130 and rdr.c < len(rdr.data):
                    nextByte = rdr.readU8()
                    readLenght += 1
                    dataBlock[currentBlockLenght] = nextByte
                    currentBlockLenght += 1
                    if nextByte != dataBlock[0]:
                        break
                    else:
                        repCount+=1
                flag = 0x80 | (repCount-3)
                wtr.writeU8(flag)
                wtr.writeU8(dataBlock[0])
                if (repCount != currentBlockLenght):
                    dataBlock[0] = dataBlock[currentBlockLenght-1]
                currentBlockLenght -= repCount

        if currentBlockLenght > 0:
            flag = currentBlockLenght - 1
            wtr.writeU8(flag)
            for i in range(currentBlockLenght):
                wtr.writeU8(dataBlock[i])
            currentBlockLenght = 0


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
class huffman():
    @staticmethod
    def decompress(data: bytes):
        rdr = BinaryReader(data)
        wtr = BinaryWriter()
        type = rdr.readU8()
        if type == 0x24:
            blocksize = 4
        elif type == 0x28:
            blocksize = 8
        else:
            raise Exception("Tried to decompress something as huffman that isn't huffman")

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

        cashedbyte = -1

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

            if blocksize == 8:
                current_size += 1
                wtr.writeU8(currentNode.data)

            elif blocksize == 4:
                if cashedbyte < 0:
                    cashedbyte = currentNode.data
                else:
                    cashedbyte |= currentNode.data << 4
                    wtr.writeU8(cashedbyte)
                    current_size += 1
                    cashedbyte = -1
            currentNode = rootNode

        return wtr.data

def decompress(data: bytes):
    if int(data[0]) == LZ10:
        return lz10.decompress(data)
    elif int(data[0]) == RLE:
        return rle.decompress(data)
    elif int(data[0]) == HUFF8BIT:
        return huffman.decompress(data)
    elif int(data[0]) == HUFF4BIT:
        return huffman.decompress(data)
    elif int(data[0]) == 0x0:
        return data[4:]
    else:
        raise Exception("Unsupported compression filetype with starting byte %s" % hex(data[0]))


def compress(data: bytes, type):
    if type == 0x10:
        return lz10.compress(data)
    elif type == RLE:
        return rle.compress(data)
    else:
        raise Exception("Unsupported compression filetype with starting byte %s" % type)