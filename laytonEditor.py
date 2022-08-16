import logging
from utility.logger import set_up_logger
import sys
import os

VERSION = "v0.4.3-pre2"

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))  # Ensure that the cwd is set correctly
    set_up_logger()  # Set logger up before importing to log import errors
    logging.info(f"\n\nLayton Editor {VERSION} running in python version {sys.version}")

import wx
from gui import MainEditor

class LaytonEditor(wx.App):
    editor: MainEditor

    def OnInit(self):
        self.editor = MainEditor(None)
        self.editor.Show(True)
        return True


if __name__ == '__main__':
    app = LaytonEditor(None)
    app.MainLoop()
