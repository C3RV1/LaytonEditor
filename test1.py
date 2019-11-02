import LaytonLib
import ndspy.rom

rom = ndspy.rom.NintendoDSRom.fromFile("../Base File.nds")
anim = LaytonLib.images.ani.AniFile(rom, 0x401)
gfx: LaytonLib.images.ani.Animation = anim.animations[1]
gfx.frameDurations = [6, 6, 6, 6]
anim.save()
rom.saveToFile("../Test File.nds")