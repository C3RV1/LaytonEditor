import pygame


class Screen:
    _screen = None  # type: pygame.Surface
    _screen_size = None  # type: tuple

    @staticmethod
    def new_screen(size, flags, name="Default Name"):
        pygame.display.set_caption(name)
        Screen._screen = pygame.display.set_mode(size, flags=flags)
        Screen._screen_size = size

    @staticmethod
    def screen():  # type: () -> pygame.Surface
        if not Screen._screen:
            raise Exception("Screen not created")
        return Screen._screen

    @staticmethod
    def screen_size():
        if not Screen._screen:
            raise Exception("Screen not created")
        return tuple(Screen._screen_size)
