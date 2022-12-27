import logging

from gui.ui.puzzle.PuzzleWidget import PuzzleWidgetUI
from formats.puzzle import Puzzle
from formats_parsed.PuzzleDCC import PuzzleDCC

from previewers.puzzle.get_puzzle_player import get_puzzle_player

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.MainEditor import MainEditor

from .PuzzlePropertiesWidget import PuzzlePropertiesWidget


class PuzzleEditor(PuzzleWidgetUI):
    def __init__(self, main_editor):
        super(PuzzleEditor, self).__init__()
        self.puzzle = None
        self.main_editor: MainEditor = main_editor

    def get_puzzle_properties_widget(self):
        return PuzzlePropertiesWidget(self)

    def set_puzzle(self, pz: Puzzle):
        self.puzzle = pz
        dcc_text = PuzzleDCC(pz)
        serialized = dcc_text.serialize(include_properties=False)
        self.text_editor.setPlainText(serialized)
        self.puzzle_properties.set_puzzle(pz)

    def preview_dcc_btn_click(self):
        text = self.text_editor.toPlainText()
        is_ok, error = PuzzleDCC(self.puzzle).parse(text, include_properties=False)
        if is_ok:
            self.main_editor.pg_previewer.start_renderer(get_puzzle_player(self.puzzle))
        else:
            logging.error(f"Error compiling DCC: {error}")

    def save_dcc_btn_click(self):
        text = self.text_editor.toPlainText()
        is_ok, error = PuzzleDCC(self.puzzle).parse(text, include_properties=False)
        if is_ok:
            self.puzzle.save_to_rom()
            self.main_editor.pg_previewer.start_renderer(get_puzzle_player(self.puzzle))
        else:
            logging.error(f"Error compiling DCC: {error}")
