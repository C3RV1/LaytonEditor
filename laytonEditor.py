if __name__ == '__main__':
    import logging
    import os
    from utility.logger import set_up_logger
    import sys
    import multiprocessing
    # import faulthandler

    # Initial setup before any imports

    VERSION = "v0.6-pre3"

    os.chdir(os.path.dirname(__file__))  # Ensure that the cwd is set correctly

    set_up_logger()  # Set logger up before everything
    logging.info(f"\n\nLayton Editor {VERSION} running in python version {sys.version}")

    multiprocessing.freeze_support()
    # faulthandler.enable()

    from PySide6.QtWidgets import QApplication
    from gui.MainEditor import MainEditor

    app = QApplication(sys.argv)
    main_editor = MainEditor()
    app.exec()
