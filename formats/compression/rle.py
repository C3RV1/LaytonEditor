from formats.binary import BinaryReader, BinaryWriter


def compress(data: bytes):
    rdr = BinaryReader(data)
    wtr = BinaryWriter()

    wtr.write_uint8(0x30)  # rle identifier

    wtr.write_uint24(len(data) if len(data) < 0xffffff else 0)
    if len(data) > 0xffffff:
        wtr.write_uint32(len(data))

    repCount = 1
    currentBlockLenght = 0
    dataBlock = [0 for _ in range(130)]
    while rdr.c < len(rdr.data):
        foundRepetition = False
        while (currentBlockLenght < 130 and rdr.c < len(rdr.data)):
            nextByte = rdr.read_uint8()
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
        if foundRepetition:
            numUncompToCopy = currentBlockLenght - 3
        else:
            numUncompToCopy = min(currentBlockLenght, 130 - 2)

        if numUncompToCopy > 0:
            flag = numUncompToCopy - 1
            wtr.write_uint8(flag)
            for i in range(numUncompToCopy):
                wtr.write_uint8(dataBlock[i])
            for i in range(numUncompToCopy, currentBlockLenght):
                dataBlock[i - numUncompToCopy] = dataBlock[i]
            currentBlockLenght -= numUncompToCopy
        if foundRepetition:
            while currentBlockLenght < 130 and rdr.c < len(rdr.data):
                nextByte = rdr.read_uint8()
                dataBlock[currentBlockLenght] = nextByte
                currentBlockLenght += 1
                if nextByte != dataBlock[0]:
                    break
                else:
                    repCount += 1
            flag = 0x80 | (repCount - 3)
            wtr.write_uint8(flag)
            wtr.write_uint8(dataBlock[0])
            if (repCount != currentBlockLenght):
                dataBlock[0] = dataBlock[currentBlockLenght - 1]
            currentBlockLenght -= repCount

    if currentBlockLenght > 0:
        flag = currentBlockLenght - 1
        wtr.write_uint8(flag)
        for i in range(currentBlockLenght):
            wtr.write_uint8(dataBlock[i])
        currentBlockLenght = 0

    return wtr.data


def decompress(data: bytes):
    rdr = BinaryReader(data)
    wtr = BinaryWriter()
    type = rdr.read_uint8()
    if type != 0x30:
        raise Exception("Tried to decompress commands that isn't RLE")
    ds = rdr.read_uint24()
    if ds == 0:
        rdr.read_uint32()

    while True:
        flag = rdr.read_uint8()
        if flag is None:
            break # we've hit the end
        compressed = (flag & 0x80) > 0
        lenght = flag & 0x7f
        lenght += 3 if compressed else 1
        if compressed:
            next = rdr.read_uint8()
            for i in range(lenght):
                wtr.write_uint8(next)
        else:
            wtr.write(rdr.read(lenght))

    return wtr.data
