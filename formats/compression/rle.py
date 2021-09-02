from formats.binary import BinaryReader, BinaryWriter


def compress(data: bytes):
    rdr = BinaryReader(data)
    wtr = BinaryWriter()

    wtr.write_uint8(0x30)  # rle identifier

    wtr.write_uint24(len(data) if len(data) < 0xffffff else 0)
    if len(data) > 0xffffff:
        wtr.write_uint32(len(data))

    rep_count = 1
    current_block_length = 0
    data_block = [0 for _ in range(130)]
    while rdr.c < len(rdr.data):
        found_repetition = False
        while current_block_length < 130 and rdr.c < len(rdr.data):
            next_byte = rdr.read_uint8()
            data_block[current_block_length] = next_byte
            current_block_length += 1
            if current_block_length > 1:
                if next_byte == data_block[current_block_length - 2]:
                    rep_count += 1
                else:
                    rep_count = 1
            found_repetition = rep_count > 2
            if found_repetition:
                break
        if found_repetition:
            num_uncomp_to_copy = current_block_length - 3
        else:
            num_uncomp_to_copy = min(current_block_length, 130 - 2)

        if num_uncomp_to_copy > 0:
            flag = num_uncomp_to_copy - 1
            wtr.write_uint8(flag)
            for i in range(num_uncomp_to_copy):
                wtr.write_uint8(data_block[i])
            for i in range(num_uncomp_to_copy, current_block_length):
                data_block[i - num_uncomp_to_copy] = data_block[i]
            current_block_length -= num_uncomp_to_copy
        if found_repetition:
            while current_block_length < 130 and rdr.c < len(rdr.data):
                next_byte = rdr.read_uint8()
                data_block[current_block_length] = next_byte
                current_block_length += 1
                if next_byte != data_block[0]:
                    break
                else:
                    rep_count += 1
            flag = 0x80 | (rep_count - 3)
            wtr.write_uint8(flag)
            wtr.write_uint8(data_block[0])
            if rep_count != current_block_length:
                data_block[0] = data_block[current_block_length - 1]
            current_block_length -= rep_count

    if current_block_length > 0:
        flag = current_block_length - 1
        wtr.write_uint8(flag)
        for i in range(current_block_length):
            wtr.write_uint8(data_block[i])

    return wtr.data


def decompress(data: bytes):
    rdr = BinaryReader(data)
    wtr = BinaryWriter()
    type_ = rdr.read_uint8()
    if type_ != 0x30:
        raise Exception("Tried to decompress commands that isn't RLE")
    ds = rdr.read_uint24()
    if ds == 0:
        rdr.read_uint32()

    while True:
        flag = rdr.read_uint8()
        if flag is None:
            break  # we've hit the end
        compressed = (flag & 0x80) > 0
        length = flag & 0x7f
        length += 3 if compressed else 1
        if compressed:
            next_ = rdr.read_uint8()
            for i in range(length):
                wtr.write_uint8(next_)
        else:
            wtr.write(rdr.read(length))

    return wtr.data
