#!python3

import sys
print(f"Layton Editor running in python version {sys.version}")
sys.path.append(".")
sys.path.append("..")

from laytoneditor import gui

def main():
    app = gui.LaytonEditor()
    app.MainLoop()


if __name__ == '__main__':
    main()
