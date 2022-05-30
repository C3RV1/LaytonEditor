import logging
import sys

import wx
import os

from utility.logger import set_up_logger
from gui import MainEditor

VERSION = "v0.4.3-pre1"

class LaytonEditor(wx.App):
    editor: MainEditor

    def OnInit(self):
        self.editor = MainEditor(None)
        self.editor.Show(True)
        return True


if __name__ == '__main__':
    set_up_logger()
    logging.info(f"Layton Editor {VERSION} running in python version {sys.version}")
    os.chdir(os.path.dirname(__file__))  # Ensure that the cwd is set correctly
    app = LaytonEditor(None)
    app.MainLoop()
