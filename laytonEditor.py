import sys
print(f"Layton Editor running in python version {sys.version}")
#sys.path.append(".")

DEBUG = 0
DEBUG_ROM = "../Base File.nds"

if DEBUG:
    import ndspy.rom

import GUI

def main():
    app = GUI.LaytonEditor()
    if DEBUG:
        with open(DEBUG_ROM, "rb") as file:
            app.mainFrame.rom = ndspy.rom.NintendoDSRom(file.read())
        app.mainFrame.setupAfterOpen()
    app.MainLoop()


if __name__ == '__main__':
    main()
