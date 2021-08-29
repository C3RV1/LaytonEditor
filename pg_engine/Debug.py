import colorama


class Debug(object):
    def __init__(self):
        pass

    @staticmethod
    def log(log_message, origin):
        if isinstance(origin, str):
            msg = Debug.name_and_message(origin, log_message)
        else:
            msg = Debug.name_and_message(type(origin).__name__, log_message)
        print(colorama.Fore.WHITE + msg)

    @staticmethod
    def log_error(log_message, origin):
        if isinstance(origin, str):
            msg = Debug.name_and_message(origin, log_message)
        else:
            msg = Debug.name_and_message(type(origin).__name__, log_message)
        print(colorama.Fore.RED + msg)

    @staticmethod
    def log_warning(log_message, origin):
        if isinstance(origin, str):
            msg = Debug.name_and_message(origin, log_message)
        else:
            msg = Debug.name_and_message(type(origin).__name__, log_message)
        print(colorama.Fore.YELLOW + msg)

    @staticmethod
    def log_debug(log_message, origin):
        if isinstance(origin, str):
            msg = Debug.name_and_message(origin, log_message)
        else:
            msg = Debug.name_and_message(type(origin).__name__, log_message)
        print(colorama.Fore.GREEN + msg)

    @staticmethod
    def name_and_message(name, message, spaces=25):
        # [NAME] + " "*(((40 - (len(name) + 2)) > 0) * (spaces - (len(name) + 2))) * message
        return "[" + name + "]" + " " * (((spaces - (len(name) + 2)) > 0) * (spaces - (len(name) + 2))) + message
