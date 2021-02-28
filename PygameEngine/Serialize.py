

class Serialize:

    separator = b";"
    string_separator = b"-"
    string_format = "ascii"

    def __init__(self):
        self.__current = b""
        self.__unpacked = []

    def reset(self):
        self.__current = b""

    def get_packed(self):
        return self.__current

    def __add_to_current(self, string):
        if self.__current == b"":
            self.__current = string
        else:
            self.__current += self.separator
            self.__current += string

    def pack_obj(self, obj):
        if isinstance(obj, int):
            self.__pack_int(obj)
        elif isinstance(obj, float):
            self.__pack_float(obj)
        elif isinstance(obj, str):
            self.__pack_string(obj)
        elif isinstance(obj, bytes):
            self.__pack_bytes(obj)
        elif isinstance(obj, dict):
            self.__pack_dict(obj)
        elif isinstance(obj, list) or isinstance(obj, tuple):
            self.__pack_array(obj)
        elif obj is None:
            self.__pack_none()
        else:
            obj = str(obj)
            self.__pack_string(obj)

    def __pack_int(self, integer):
        self.__add_to_current(b"i" + str(integer).encode("ascii"))

    def __pack_float(self, f):
        self.__add_to_current(b"f" + str(f).encode("ascii"))

    def __pack_string(self, s):
        self.__add_to_current(b"s" + str(len(s)).encode("ascii") + self.string_separator +
                              self.string_format.encode("ascii") + self.string_separator +
                              s.encode(self.string_format))

    def __pack_bytes(self, b):
        self.__add_to_current(b"b" + str(len(b)).encode("ascii") + self.string_separator + b)

    def __pack_dict(self, dictionary):
        self.__add_to_current(b"d" + str(len(dictionary.keys())).encode("ascii"))
        for key, value in dictionary.items():
            self.pack_obj(key)
            self.pack_obj(value)

    def __pack_array(self, arr):
        self.__add_to_current(b"a" + str(len(arr)).encode("ascii"))
        for value in arr:
            self.pack_obj(value)

    def __pack_none(self):
        self.__add_to_current(b"n")

    def unpack(self, packed):
        self.__current = packed
        self.__unpacked = []
        while len(self.__current) > 0:
            self.__unpacked.append(self.__unpack_1())
            print(self.__current)

        return self.__unpacked

    def __unpack_1(self):
        identifier = self.__current[:1]
        self.__current = self.__current[1:]

        print(identifier)

        if identifier == b"i":
            return self.__unpack_int()
        elif identifier == b"f":
            return self.__unpack_float()
        elif identifier == b"s":
            return self.__unpack_string()
        elif identifier == b"b":
            return self.__unpack_bytes()
        elif identifier == b"d":
            return self.__unpack_dict()
        elif identifier == b"a":
            return self.__unpack_array()
        elif identifier == b"n":
            return self.__unpack_none()
        else:
            raise TypeError("Identifier {} not recognised".format(identifier))

    def __unpack_int(self):
        ret = int(self.__current.split(self.separator)[0])
        self.__current = self.separator.join(self.__current.split(self.separator)[1:])
        return ret

    def __unpack_float(self):
        ret = float(self.__current.split(self.separator)[0])
        self.__current = self.separator.join(self.__current.split(self.separator)[1:])
        return ret

    def __unpack_string(self):
        str_len = int(self.__current.split(self.string_separator)[0])
        self.format = self.__current.split(self.string_separator)[1].decode("ascii")
        self.__current = self.string_separator.join(self.__current.split(self.string_separator)[2:])

        ret = self.__current[:str_len]
        self.__current = self.__current[str_len + 1:]
        return ret.decode(self.format)

    def __unpack_bytes(self):
        str_len = int(self.__current.split(self.string_separator)[0])
        self.__current = self.string_separator.join(self.__current.split(self.string_separator)[1:])

        ret = self.__current[:str_len]
        self.__current = self.__current[str_len + 1:]
        return ret

    def __unpack_dict(self):
        dict_len = int(self.__current.split(self.separator)[0])
        self.__current = self.separator.join(self.__current.split(self.separator)[1:])

        dictionary = {}
        for i in range(dict_len):
            key, value = self.__unpack_1(), self.__unpack_1()
            dictionary[key] = value

        return dictionary

    def __unpack_array(self):
        arr_len = int(self.__current.split(self.separator)[0])
        self.__current = self.separator.join(self.__current.split(self.separator)[1:])

        arr = []
        for i in range(arr_len):
            arr.append(self.__unpack_1())

        return arr

    def __unpack_none(self):
        self.__current = self.separator.join(self.__current.split(self.separator)[1:])
        return None
