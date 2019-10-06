import sys
print(f"Layton Editor running in python version {sys.version}")
sys.path.append(".")

import GUI

def main():
    app = GUI.LaytonEditor()
    app.MainLoop()


if __name__ == '__main__':
    main()
