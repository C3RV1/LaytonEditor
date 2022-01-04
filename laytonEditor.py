import sys

import wx
import os

from gui import MainEditor

print(f"Layton Editor running in python version {sys.version}")


class LaytonEditor(wx.App):
    editor: MainEditor

    def OnInit(self):
        self.editor = MainEditor(None)
        self.editor.Show(True)
        return True


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))  # Ensure that the cwd is set correctly
    app = LaytonEditor(None)
    app.MainLoop()
