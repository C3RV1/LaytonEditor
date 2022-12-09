import logging

from .ui.PuzzleWidget import PuzzleWidgetUI
from formats.puzzle import Puzzle
from formats_parsed.PuzzleDCC import PuzzleDCC

from previewers.puzzle.PuzzlePlayer import PuzzlePlayer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from MainEditor import MainEditor


class PuzzleWidget(PuzzleWidgetUI):
    def __init__(self, main_editor):
        super(PuzzleWidget, self).__init__()
        self.puzzle = None
        self.main_editor: MainEditor = main_editor

    def set_puzzle(self, pz: Puzzle):
        self.puzzle = pz
        dcc_text = PuzzleDCC(pz)
        serialized = dcc_text.serialize()
        self.text_editor.setPlainText(serialized)

    def preview_dcc_btn_click(self):
        text = self.text_editor.toPlainText()
        is_ok, error = PuzzleDCC(self.puzzle).parse(text)
        if is_ok:
            self.main_editor.pg_previewer.start_renderer(PuzzlePlayer(self.puzzle))
        else:
            logging.error(f"Error compiling DCC: {error}")

    def save_dcc_btn_click(self):
        text = self.text_editor.toPlainText()
        is_ok, error = PuzzleDCC(self.puzzle).parse(text)
        if is_ok:
            self.puzzle.save_to_rom()
            self.main_editor.pg_previewer.start_renderer(PuzzlePlayer(self.puzzle))
        else:
            logging.error(f"Error compiling DCC: {error}")
