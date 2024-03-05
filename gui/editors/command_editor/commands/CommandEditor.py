from formats.gds import GDSCommand
from formats.event import Event
from formats.movie import Movie


class CommandEditor:
    def __init__(self):
        super(CommandEditor, self).__init__()
        self.command: GDSCommand = None
        self.on_command_saved = None

    def set_command(self, command: GDSCommand, on_command_saved=None, **_kwargs):
        self.command = command
        self.on_command_saved = on_command_saved

    def save(self):
        if self.on_command_saved:
            self.on_command_saved(self.command)


class CommandEditorEvent(CommandEditor):
    def __init__(self):
        super().__init__()
        self.event: Event = None

    def set_command(self, command: GDSCommand, on_command_saved, event: Event = None, **kwargs):
        super().set_command(command, **kwargs)
        self.event = event


class CommandMovieEvent(CommandEditor):
    def __init__(self):
        super().__init__()
        self.movie: Movie = None

    def set_command(self, command: GDSCommand, movie: Movie = None, **kwargs):
        super().set_command(command, **kwargs)
        self.movie = movie
