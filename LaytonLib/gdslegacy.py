def extract_from_gds(raw):
    data_str = raw
    data = [hex(x) for x in data_str]
    data_ext = []

    filestart = 2

    current = 2
    current_data = []
    first = True
    zeros = 0
    while current < len(data):
        if int(data[current], 0) == 0 and zeros < 2 and not first:
            zeros += 1
            current += 2
            continue
        if int(data[current], 0) > 3 or first or (zeros == 2 and int(data[current], 0) > 1):
            if first:
                first = False
                filestart = current
            else:
                if current_data[0] == '0x0' and len(current_data) == 1:
                    current_data = []
                    filestart = 6
            if current_data:
                data_ext.append(current_data)
            current_data = [data[current], ]
        elif int(data[current], 0) == 1:
            current += 2
            n = int(data[current], 0)
            current += 1
            current_data.append(n + int(data[current], 0) * 256)
            current += 1
            continue
        elif int(data[current], 0) == 3:
            current += 2
            end = int(data[current], 0) + (int(data[current + 1], 0) * 256) + current
            current_string = ""
            current += 1
            while current < end:
                current += 1
                current_string += chr(data_str[current])
            current_data.append(current_string)
        elif int(data[current], 0) == 0:
            pass
        elif int(data[current], 0) == 2:
            current += 2
            vector = []
            vector.append(int(data[current], 0) * 256 + int(data[current + 1], 0))
            current += 2
            vector.append(int(data[current], 0) * 256 + int(data[current + 1], 0))
            current_data.append(vector)
            current += 0
        else:
            print("ERROR: Unsupported commands type")
        zeros = 0
        current += 2
    data_ext.append(current_data)

    return {"start": filestart, "commands": data_ext}


def extract_from_simplified(raw):
    data_str = raw
    lines = [l.split('#')[0] for l in data_str.split('\n')]
    data_ext = []
    current = 0
    current_data = []
    filestart = 6

    while current < len(lines):
        line = lines[current]
        if line:
            if line[0:6] == "START:":
                filestart = int(line[6:])
            elif line[0:2] == "0x":
                current_data = [line, ]
                if lines[current + 1] == "[":
                    offset = 2
                    while lines[current + offset] != ']':
                        if lines[current + offset][1:5] == 'int:':
                            current_data.append(int(lines[current + offset][6:]))
                        if lines[current + offset][1:5] == 'hex:':
                            current_data.append(int(lines[current + offset][6:], 16))
                        if lines[current + offset][1:5] == 'str:':
                            current_data.append(lines[current + offset][6:])
                        if lines[current + offset][1:5] == "vec:":
                            strs = lines[current + offset].replace(']', '').split('[')[1].split(',')
                            current_data.append([int(strs[0]), int(strs[1])])
                        offset += 1
                data_ext.append(current_data)
        current += 1

    return {"start": filestart, "commands": data_ext}


def convert_to_gds(data):
    filestart = data["start"]
    data_ext = data["commands"]
    raw = bytes()
    for i, item in enumerate(data_ext):
        raw += bytes([int(item[0], 0)])
        if len(item) > 1:
            raw += bytes(1)
            for ii, subitem in enumerate(item[1:]):
                if type(subitem) is int:
                    raw += bytes([1, 0, subitem % 256, int(subitem / 256)])
                    raw += bytes([0, 0])
                if type(subitem) is str:
                    raw += bytes([3, 0, (len(subitem) + 1) % 256, int((len(subitem) + 1) / 256)])
                    raw += bytes(subitem, "ascii")
                    raw += bytes(1)
                if type(subitem) is list:
                    raw += bytes([2, 0, int(subitem[0] / 256), int(subitem[0] % 256), int(subitem[1] / 256),
                                  int(subitem[1] % 256)])
        else:
            raw += bytes(1)
        if i != len(data_ext) - 1 and i != len(data_ext) - 2:
            raw += bytes(2)
    lenght = len(raw) - 4 + filestart
    final = bytes([lenght % 256, int(lenght / 256)])
    final += bytes(filestart - 2)
    final += raw
    return final


def convert_to_simplified(data):
    filestart = data["start"]
    data_ext = data["commands"]
    lines = ["START: " + str(filestart), ""]
    for item in data_ext:
        lines.append(item[0])
        if len(item) > 1:
            lines.append('[')
            for subitem in item[1:]:
                if type(subitem) is int:
                    lines.append("\tint: " + str(subitem) + "\t\t# hex: " + hex(subitem))
                elif type(subitem) is str:
                    lines.append("\tstr: " + subitem)
                elif type(subitem) is list:
                    lines.append("\tvec: [{}, {}]".format(subitem[0], subitem[1]))

            lines.append(']')
        lines.append('')
    return "\n".join(lines)
