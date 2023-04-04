from gui.ui.command_editor.commands.movie.Subtitle import SubtitleUI
from ..CommandEditor import CommandMovieEvent
from formats.gds import GDSCommand
from formats.movie import Movie


class Subtitle(CommandMovieEvent, SubtitleUI):
    def set_command(self, command: GDSCommand, movie: Movie = None, **kwargs):
        super().set_command(command, movie=movie, **kwargs)
        self.start_time.setValue(command.params[1])
        self.end_time.setValue(command.params[2])
        self.sub_text.setPlainText(
            movie.subtitles[command.params[0]]
        )

    def save(self):
        self.command.params[1] = self.start_time.value()
        self.command.params[2] = self.end_time.value()
        self.movie.subtitles[self.command.params[0]] = self.sub_text.toPlainText()
