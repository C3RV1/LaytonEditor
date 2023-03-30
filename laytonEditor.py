if __name__ == '__main__':
    import logging
    from utility.logger import set_up_logger
    import sys
    import os
    import multiprocessing
    from PySide6.QtWidgets import QApplication
    from gui.MainEditor import MainEditor

    # import faulthandler

    VERSION = "v0.5-pre1"

    multiprocessing.freeze_support()
    os.chdir(os.path.dirname(__file__))  # Ensure that the cwd is set correctly
    set_up_logger()  # Set logger up before importing to log import errors
    logging.info(f"\n\nLayton Editor {VERSION} running in python version {sys.version}")
    # faulthandler.enable()

    app = QApplication(sys.argv)
    main_editor = MainEditor()
    app.exec()
