import ndspy.rom
from LaytonLib.binary import *
import subprocess
import os.path


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
    def __init__(self, rom: ndspy.rom.NintendoDSRom, setupcode_folder,
                 patchcode_folder, arenaLoPtrAddress, complete_rebuild=False):
        self.rom = rom
        self.setupcode_folder = setupcode_folder
        self.patchcode_folder = patchcode_folder
        self.arm9_edit = BinaryEditor(rom.arm9)
        print(hex(len(self.arm9_edit)))
        print(hex(self.arm9_edit.readU32(len(self.arm9_edit)-4)))
        print(self.arm9_edit.data)
        self.arm9_edit.align(4)
        self.arenaLoPtrAddress = arenaLoPtrAddress

        if complete_rebuild:
            self.clean_all()

        self.offset_setupcode_hook = 0x02000000 | len(self.arm9_edit.data)
        self.offset_setupcode = self.offset_setupcode_hook + 5 * 4  # 5 instructions
        self.offset_patchcode = self.arm9_edit.readU32(arenaLoPtrAddress & 0xFFFFFF)

        self.apply_setupcodehook()
        self.build_patchcode()

        self.patchcode_edit = BinaryEditor(self.patchcode_bin)

        self.apply_hooks()

        self.patchcode_edit.align(4)
        self.arm9_edit.align(4)
        self.arm9_edit.add(self.patchcode_edit.data)

        self.replace_setupcodeplaceholders()

        # Finally change the value in the arenaLo ptr
        self.arm9_edit.replU32(self.offset_patchcode + len(self.patchcode_edit) + 0x10,  # Extra offset
                               arenaLoPtrAddress - 0x02000000)

        # Save the new arm9
        rom.arm9 = self.arm9_edit.data

    def apply_setupcodehook(self):
        # First we read the instruction that will be replaced (In our case 0x800,
        # because that's the first instruction of the game. And put it at the
        # start of the hook code.

        self.arm9_edit.addU32(self.arm9_edit.readU32(0x800))
        self.arm9_edit.addU32(0xE92D5FFF)  # push {r0-r12, r14}

        # Here is where we jump to the setup code
        self.build_setupcode()

        # Now find the "setupcustomcode" function and branch to it.
        for line in self.setupcode_sym.split("\n"):
            if line.endswith(" _Z15setupcustomcodev"):
                self.arm9_edit.addU32(
                    makeBranchOpcode(len(self.arm9_edit.data) | 0x02000000, int(line[:8], 16)
                                     , True))

        # Return back to the games code
        self.arm9_edit.addU32(0xE8BD5FFF)  # pop ^
        self.arm9_edit.addU32(0xE12FFF1E)  # BX LR

        # Now put the setupcode in
        self.arm9_edit.add(self.setupcode_bin)

        # Branch to hook at start of game
        self.arm9_edit.replU32(makeBranchOpcode(0x02000800, self.offset_setupcode_hook, True), 0x800)

    def build_setupcode(self):
        process = subprocess.Popen(f"make CODEADDR={hex(self.offset_setupcode)}",
                                   cwd=self.setupcode_folder)
        process.wait()
        with open(os.path.join(self.setupcode_folder, "newcode.bin"), "rb") as file:
            self.setupcode_bin = file.read()
        with open(os.path.join(self.setupcode_folder, "newcode.sym"), "r") as file:
            self.setupcode_sym = file.read()

    def build_patchcode(self):
        process = subprocess.Popen(f"make CODEADDR={hex(self.offset_patchcode)}",
                                   cwd=self.patchcode_folder)
        process.wait()
        with open(os.path.join(self.patchcode_folder, "newcode.bin"), "rb") as file:
            self.patchcode_bin = file.read()
        with open(os.path.join(self.patchcode_folder, "newcode.sym"), "r") as file:
            self.patchcode_sym = file.read()

    def apply_hooks(self):
        for line in self.patchcode_sym.split("\n"):
            if "repl_" in line:
                try:
                    offset_function = int(line[:8], 16)
                    offset_original_hex = line.find("repl_") + 5  # +5 because it gives the adress at the start of repl_
                    offset_original = int(line[offset_original_hex:offset_original_hex + 8], 16)
                    offset_arm9_original = offset_original - 0x02000000
                    self.arm9_edit.replU32(makeBranchOpcode(offset_original, offset_function, False),
                                           offset_arm9_original)

                except:
                    print("Warning: repl function not working:", line)
            elif "nsub_" in line:
                try:
                    offset_function = int(line[:8], 16)
                    offset_original_hex = line.find("nsub_") + 5  # +5 because it gives the adress at the start of repl_
                    offset_original = int(line[offset_original_hex:offset_original_hex + 8], 16)

                    offset_arm9_original = offset_original - 0x02000000
                    self.arm9_edit.replU32(makeBranchOpcode(offset_original, offset_function, True),
                                           offset_arm9_original)
                except:
                    print("Warning: repl function not working:", line)
            elif "hook_" in line:
                offset_function = int(line[:8], 16)
                offset_original_hex = line.find("hook_") + 5
                offset_original = int(line[offset_original_hex:offset_original_hex + 8], 16)
                offset_hookpoint = self.offset_patchcode + len(self.patchcode_edit.data)


                offset_arm9_original = offset_original - 0x02000000
                print(hex(offset_original-0x02000000))
                original_instruction = self.arm9_edit.readU32(offset_original - 0x02000000)
                self.arm9_edit.replU32(makeBranchOpcode(offset_original, offset_hookpoint, False),
                                       offset_arm9_original)
                print(hex(original_instruction))

                self.patchcode_edit.addU32(original_instruction)
                self.patchcode_edit.addU32(0xE92D5FFF)  # push {r0-r12, r14    }
                self.patchcode_edit.addU32(
                    makeBranchOpcode(self.offset_patchcode + len(self.patchcode_edit.data),
                                     offset_function, True))
                self.patchcode_edit.addU32(0xE8BD5FFF)  # pop ^
                self.patchcode_edit.addU32(
                    makeBranchOpcode(self.offset_patchcode + len(self.patchcode_edit.data), offset_original + 4, False))

    def replace_setupcodeplaceholders(self):
        for line in self.setupcode_sym.split("\n"):
            if "PatchCodeOffset" in line:
                self.arm9_edit.replU32(self.offset_patchcode, int(line[:8], 16) - 0x02000000)
            if "CustomCodeLenght" in line:
                self.arm9_edit.replU32(len(self.patchcode_edit.data), int(line[:8], 16) - 0x02000000)

    def clean_all(self):
        process = subprocess.Popen(f"make clean",
                                   cwd=self.patchcode_folder)
        process.wait()
        process = subprocess.Popen(f"make clean",
                                   cwd=self.setupcode_folder)
        process.wait()
