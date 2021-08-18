import formats.gds
import formats.filesystem
import re

from formats import conf

command_names = [
    "x00", "x01", "fade_in", "fade_out", "dial", "x05", "set_mode", "set_next_mode",
    "play_movie", "goto", "x0a", "x0b", "x0c", "x0d", "x0e", "x0f",
    "x10", "x11", "x12", "x13", "x14", "x15", "x16", "x17",
    "x18", "x19", "x1a", "x1b", "x1c", "x1d", "x1e", "x1f",
    "x20", "load_bg_bottom", "load_bg_top", "x23", "x24", "x25", "x26", "x27",
    "x28", "x29", "show_character", "hide_character", "x2c", "show_chapter", "x2e", "x2f",
    "x30", "sleep", "x32", "fade_out_bottom", "x34", "x35", "x36", "x37",
    "x38", "x39", "x3a", "x3b", "x3c", "x3d", "x3e", "x3f",
    "x40", "x41", "x42", "x43", "x44", "x45", "x46", "x47",
    "x48", "x49", "x4a", "x4b", "x4c", "x4d", "x4e", "x4f",
    "x50", "x51", "x52", "x53", "x54", "x55", "x56", "x57",
    "x58", "x59", "x5a", "x5b", "play_voiceline", "x5d", "x5e", "x5f",
    "x60", "x61", "play_bg", "x63", "x64", "x65", "x66", "x67",
    "x68", "x69", "x6a", "x6b", "idle", "x6d", "x6e", "x6f",
    "x70", "x71", "x72", "x73", "x74", "x75", "x76", "x77",
    "x78", "x79", "x7a", "x7b", "x7c", "x7d", "x7e", "x7f",
    "x80", "x81", "x82", "x83", "x84", "x85", "x86", "x87",
    "x88", "x89", "x8a", "x8b", "x8c", "x8d", "x8e", "x8f",
    "x90", "x91", "touch_popup", "x93", "x94", "x95", "x96", "x97",
    "x98", "play_st_stream", "x9a", "x9b", "x9c", "x9d", "x9e", "x9f",
    "xa0", "xa1", "xa2", "xa3", "xa4", "xa5", "xa6", "xa7",
    "xa8", "xa9", "xaa", "xab", "xac", "xad", "xae", "xaf",
    "xb0", "xb1", "xb2", "xb3", "xb4", "xb5", "xb6", "xb7",
    "xb8", "xb9", "xba", "xbb", "xbc", "xbd", "xbe", "xbf",
    "xc0", "xc1", "xc2", "xc3", "xc4", "xc5", "xc6", "xc7",
    "xc8", "xc9", "xca", "xcb", "xcc", "xcd", "xce", "xcf",
    "xd0", "xd1", "xd2", "xd3", "xd4", "xd5", "xd6", "xd7",
    "xd8", "xd9", "xda", "xdb", "xdc", "xdd", "xde", "xdf",
    "xe0", "xe1", "xe2", "xe3", "xe4", "xe5", "xe6", "xe7",
    "xe8", "xe9", "xea", "xeb", "xec", "xed", "xee", "xef",
    "xf0", "xf1", "xf2", "xf3", "xf4", "xf5", "xf6", "xf7",
    "xf8", "xf9", "xfa", "xfb", "xfc", "xfd", "xfe", "xff",
]


def convert_to_textscript(gdsscript: formats.gds.GDS, index=None, rom=None) -> str:
    ret = ""
    handlers = {
        int: lambda x: str(x),
        float: lambda x: str(x),
        str: lambda x: '"' + x + '"'
    }
    arch = None
    for command in gdsscript.commands:
        if rom and command.command == 0x04 and index // 1000 != 24:
            # TODO: event-24_xxx
            if arch is None:
                arch = rom.get_archive(f"/data_lt2/event/?/ev_t{index // 1000}.plz".replace("?", conf.LANG))
            dial_gds = formats.gds.GDS(f"t{index // 1000:02}_{index % 1000:03}_{command.params[0]:03}.gds", rom=arch)
            ret += command_names[command.command] + " " + ", ".join(
                handlers[type(x)](x) for x in dial_gds.params)
            ret += "\n"
            continue
        ret += command_names[command.command] + " " + ", ".join(
            handlers[type(x)](x) for x in command.params) + "\n"
    return ret


REGEX_WHITESPACE_LINE = re.compile(r"^\s*$")
REGEX_STRING_PARAM = re.compile(r"^\s*[\"\'](.*)[\"\']\s*$")
REGEX_INTEGER_PARAM = re.compile(r"^\s*(\d+)\s*$")
REGEX_FLOAT_PARAM = re.compile(r"^\s*((\d+\.\d*)|(\d*\.\d+))\s*$")


def convert_to_gdsscript(textscript: str):
    gdsscript = formats.gds.GDS()
    for line in textscript.split("\n"):
        if re.match(REGEX_WHITESPACE_LINE, line):
            continue
        command_name = line.split(" ")[0]
        command = command_names.index(command_name)
        param_strings = line[len(command_name):].split(",")
        params = []
        for param_string in param_strings:
            if m := re.match(REGEX_STRING_PARAM, param_string):
                params.append(m[1])
            elif m := re.match(REGEX_INTEGER_PARAM, param_string):
                params.append(int(m[1]))
            elif m := re.match(REGEX_FLOAT_PARAM, param_string):
                params.append(float(m[1]))
        gdsscript.commands.append(formats.gds.GDSCommand(command, params))
    return gdsscript


if __name__ == '__main__':
    rom = formats.filesystem.NintendoDSRom.fromFile("../../Base File.nds")
    # arch = formats.filesystem.PlzArchive("/data_lt2/script/logo.gds", rom=rom)
    gds = formats.gds.GDS("/data_lt2/script/logo.gds", rom=rom)
    textscript = convert_to_textscript(gds)
