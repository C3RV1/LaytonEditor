import ndspy.rom
from LaytonLib.binary import *

# Create the hex that represents a branch instruction
def makeBranchOpcode(srcAddr, destAddr, withLink):
    res = 0xEA000000
    if withLink: res |= 0x01000000
    offs = int(destAddr / 4) - int(srcAddr / 4) - 2
    offs &= 0x00FFFFFF
    if offs < 0:
        offs = int.from_bytes(offs.to_bytes(4, "little", signed=True), "little", signed=False)
    offs &= 0x00FFFFFF
    res |= offs
    return res

# Made into a class for readability
class PatchRom:
    def __init__(self, rom: ndspy.rom.NintendoDSRom, setupcode_folder, patchcode_folder):
        self.rom = rom
        self.setupcode_folder = setupcode_folder
        self.patchcode_folder = patchcode_folder
        self.arm9_edit = BinaryEditor(rom.loadArm9())
        self.apply_setupcodehook()
        self.add_patchcode()
        self.apply_hooks()
        self.replace_setupcodeplaceholders()

    def apply_setupcodehook(self):
        ...
        self.build_setupcode()
        ...
        pass

    def build_setupcode(self):
        pass

    def add_patchcode(self):
        ...
        self.build_patchcode()
        ...

    def build_patchcode(self):
        pass

    def apply_hooks(self):
        pass

    def replace_setupcodeplaceholders(self):
        pass

