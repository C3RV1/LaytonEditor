import ndspy.rom
import os.path

SAVE_FOLDER = "../../overlays"
ROM = "../../Base File.nds"
N_OVERLAYS = 55
START_AT_OV = 0

rom = ndspy.rom.NintendoDSRom.fromFile(ROM)

overlays = rom.loadArm9Overlays(range(START_AT_OV, N_OVERLAYS))
arm9 = rom.loadArm9()

data = ""

with open(os.path.join(SAVE_FOLDER, "arm9.bin"),"wb+") as file:
    file.write(rom.arm9)

data += "Arm9:\n"
data += f"  ram address: {hex(arm9.ramAddress)}\n"
data += f"  size:   {hex(len(rom.arm9))}\n"
data += f"  end address: {hex(arm9.ramAddress+len(rom.arm9))}\n"
data += "\n"

for i in range(len(arm9.sections)):
    section: arm9.Section = arm9.sections[i]
    with open(os.path.join(SAVE_FOLDER, f"section{i}.bin"), "wb+") as file:
        file.write(section.data)
    data += f"Arm9 Section {i}:\n"
    data += f"  ram address: {hex(section.ramAddress)}\n"
    data += f"  size:   {hex((len(section.data)))}\n"
    data += f"  end address: {hex(section.ramAddress + (len(section.data)))}\n"
    data += "\n"


for i in range(START_AT_OV, N_OVERLAYS):
    overlay = overlays[i]
    with open(os.path.join(SAVE_FOLDER, f"ov{i}.bin"), "wb+") as file:
        file.write(overlay.data)
    data += f"Overlay {i}:\n"
    data += f"  ram address: {hex(overlay.ramAddress)}\n"
    data += f"  size:   {hex((overlay.ramSize))}\n"
    data += f"  end address: {hex(overlay.ramAddress+overlay.ramSize)}\n"
    data += "\n"

with open(os.path.join(SAVE_FOLDER, "data.txt"), "w+") as file:
    file.write(data)
