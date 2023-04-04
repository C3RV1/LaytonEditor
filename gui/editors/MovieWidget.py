from gui.ui.MovieWidget import MovieWidgetUI
from gui.editor_categories.Movies import MovieAsset
from .command_editor.CommandListEditor import CommandListEditor
from .command_editor.commands import get_movie_command_widget
from .command_editor.command_parsers import movie_cmd_context_menu, movie_cmd_parsers
from formats.gds import GDS
from formats.movie import Movie


class MovieEditor(MovieWidgetUI):
    subtitle_editor: CommandListEditor

    def __init__(self):
        super().__init__()
        self.movie: Movie = None

    def set_movie(self, movie_asset: MovieAsset):
        self.movie = movie_asset.get_movie()
        self.subtitle_editor.set_gds_and_data(self.movie.gds, rom=movie_asset.rom, movie=movie_asset.movie)

    def get_command_editor(self):
        return CommandListEditor(get_movie_command_widget, movie_cmd_parsers, movie_cmd_context_menu)

    def save_click(self):
        self.subtitle_editor.save()
        self.movie.save_to_rom()
