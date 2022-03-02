import os


def set_extension(path, ext):
    return os.path.splitext(path)[0] + ext
