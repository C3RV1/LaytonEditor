from formats.gds import GDSCommand
from formats.event import Event
from formats.movie import Movie


class CommandEditor:
    def __init__(self):
        super(CommandEditor, self).__init__()
        self.command: GDSCommand = None

    def set_command(self, command: GDSCommand, **_kwargs):
        self.command = command

    def save(self):
        pass


class CommandEditorEvent(CommandEditor):
    def __init__(self):
        super().__init__()
        self.event: Event = None

    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super().set_command(command, **kwargs)
        self.event = event


class CommandMovieEvent(CommandEditor):
    def __init__(self):
        super().__init__()
        self.movie: Movie = None

    def set_command(self, command: GDSCommand, movie: Movie = None, **kwargs):
        super().set_command(command, **kwargs)
        self.movie = movie
