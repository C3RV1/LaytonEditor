import os
import re
import subprocess

from formats.binary import *

__all__ = ["patch_arm9"]

REGEX_SYMBOL = re.compile(r"([0-9a-f]{8})\s+.\s+.\s+\.text\s+([0-9a-f]{8})\s+(.*)")
ARM9_BASE = 0x02000000
ARM9_START = 0x02000800


def _make_and_load(patch_dir, bootstrap_location, patch_location, rebuild=True):
    if rebuild:
        process = subprocess.Popen(f"make clean", cwd=patch_dir, shell=True)
        process.wait()
    process = subprocess.Popen(f"make CODEADDR=0x{patch_location:x} "
                               f"STRAPADDR=0x{bootstrap_location:x}", cwd=patch_dir, shell=True)
    process.wait()
    with open(os.path.join(patch_dir, "output/patch.bin"), "rb") as f:
        patch_bin = f.read()
    with open(os.path.join(patch_dir, "output/patch.sym")) as f:
        patch_sym = f.read()
    with open(os.path.join(patch_dir, "output/bootstrap.bin"), "rb") as f:
        bootstrap_bin = f.read()
    with open(os.path.join(patch_dir, "output/bootstrap.sym")) as f:
        bootstrap_sym = f.read()
    return {"patch.bin": patch_bin, "patch.sym": patch_sym,
            "bootstrap.bin": bootstrap_bin, "bootstrap.sym": bootstrap_sym}


def _get_symbols(symfile, name_pattern=".*"):
    all_symbols = re.findall(REGEX_SYMBOL, symfile)
    return [(int(sym[0], 16), int(sym[1], 16), sym[2]) for sym in all_symbols if re.match(name_pattern, sym[2])]


def _branch_opp(src, dest, do_link):
    res = 0xEB000000 if do_link else 0xEA000000
    offs = ((dest - src) // 4 - 2) & 0x00ffffff
    return res | offs


def _repl(editor, src, dest, do_link):
    editor.seek(src - ARM9_BASE)
    editor.write_uint(_branch_opp(src, dest, do_link))


def patch_arm9(decompressed_arm9: bytearray, patch_dir, heap_ptr_location=0x0201efb8, rebuild=True):
    editor = BinaryEditor(decompressed_arm9)
    # Get the current location of the heap
    editor.seek(heap_ptr_location - ARM9_BASE)
    patch_location = editor.read_uint()

    # Build the patch
    patch_files = _make_and_load(patch_dir, len(decompressed_arm9) | 0x02000000, patch_location, rebuild=rebuild)
    bootstrap_adress, *_ = _get_symbols(patch_files["bootstrap.sym"], "bootstrap")[0]

    # Write the bootstrap and patch at the end
    editor.seek(0, SEEK_END)
    editor.write(patch_files["bootstrap.bin"])
    patch_in_arm9 = editor.tell()
    editor.write(patch_files["patch.bin"])

    # Hook the start of the game to our bootstrap function
    _repl(editor, ARM9_START, bootstrap_adress, True)

    # Put the heap after our patch.
    editor.seek(heap_ptr_location - ARM9_BASE)
    new_heap_location = (patch_location + len(patch_files["patch.bin"]) + 3) // 4 * 4
    editor.write_uint(new_heap_location)
    print("Patch location:", hex(patch_location))
    print("Patch lenght:", hex(len(patch_files["patch.bin"])))

    # Replace the __org_ symbols to their instructions in arm9
    for location, _, name in _get_symbols(patch_files["patch.sym"], "__org_.*"):
        finds = re.findall(r"__org_(.*)", name)
        arm9_location = int(finds[0], 0)
        editor.seek(arm9_location - ARM9_BASE)
        instr = editor.read_uint()
        editor.seek(location - patch_location + patch_in_arm9)
        editor.write_uint(instr)

    # Write the __repl_ branches
    for location, _, name in _get_symbols(patch_files["patch.sym"], "__repl_.*"):
        finds = re.findall(r"__repl_(.*)", name)
        arm9_location = int(finds[0], 0)
        _repl(editor, arm9_location, location, True)

    # Write the __escp_ branches
    for location, _, name in _get_symbols(patch_files["patch.sym"], "__escp_.*"):
        finds = re.findall(r"__escp_(.*)", name)
        arm9_location = int(finds[0], 0)
        _repl(editor, arm9_location, location, False)

    return editor.data
