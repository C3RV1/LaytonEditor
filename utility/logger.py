import logging
import os.path
import sys
import threading


_threading_excepthook = threading.excepthook
_sys_excepthook = sys.excepthook


def sys_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        _sys_excepthook(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    _sys_excepthook(exc_type, exc_value, exc_traceback)


def threading_exception(exc_args: threading.ExceptHookArgs, **kwargs):
    exc_value = exc_args.exc_value
    exc_traceback = exc_args.exc_traceback
    _thread = exc_args.thread
    exc_type = exc_args.exc_type
    if issubclass(exc_type, KeyboardInterrupt):
        _threading_excepthook(exc_args, **kwargs)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    _threading_excepthook(exc_args, **kwargs)


def set_up_logger():
    if getattr(sys, 'frozen', False):
        # Running in bundle
        filepath = os.path.join(os.path.dirname(sys.executable), "laytonEditor.log")
    else:
        # Normal python instance
        filepath = "./laytonEditor.log"
    logging.basicConfig(filename=filepath, level=logging.INFO, filemode="w", force=True)
    logging.getLogger().addHandler(logging.StreamHandler())
    sys.excepthook = sys_exception
    threading.excepthook = threading_exception
