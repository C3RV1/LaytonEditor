import wx
import wx.propgrid

import formats.puzzles.puzzle_data as pzd
import gui.generated
from utility.auto_newline import auto_newline


class PuzzleEditor(gui.generated.PuzzleEditor):
    puzzle_data: pzd.PuzzleData

    def load_puzzle(self, rom, puzzle_index):
        self.puzzle_data = pzd.PuzzleData(rom)
        self.puzzle_data.set_internal_id(puzzle_index)
        if not self.puzzle_data.load_from_rom():
            return

        def create_property(name, value):
            if isinstance(value, int):
                return wx.propgrid.IntProperty(name, name, value)
            elif isinstance(value, str):
                return wx.propgrid.StringProperty(name, name, value)
            elif isinstance(value, float):
                return wx.propgrid.FloatProperty(name, name, value)
            return None

        self.pz_data_grid.Append(create_property("Puzzle Title", self.puzzle_data.title))

    def enter(self):
        pass


class PuzzleBaseDataEditor(gui.generated.PuzzleBaseDataEditor):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.puzzle_data = pzd.PuzzleData(rom=self.parent.rom)

    def OnButtonLoadPuzzle(self, event):  # Load puzzle from id
        puzzle_id = int(self.puzz_id_text.Value, 0)

        self.puzzle_data.set_internal_id(puzzle_id)
        if not self.puzzle_data.load_from_rom():
            error_msg = "Error loading puzzle with id {} from rom".format(self.puzzle_data.internal_id)
            error_dialog = wx.MessageDialog(self, error_msg, style=wx.ICON_ERROR | wx.OK)
            error_dialog.ShowModal()
            return

        self.puzz_txt_input.Value = self.puzzle_data.text
        self.correct_input.Value = self.puzzle_data.correct_answer
        self.incorrect_input.Value = self.puzzle_data.incorrect_answer
        self.hint1_input.Value = self.puzzle_data.hint1
        self.hint2_input.Value = self.puzzle_data.hint2
        self.hint3_input.Value = self.puzzle_data.hint3
        self.puzz_title_input.Value = self.puzzle_data.title
        self.puzzle_type_choice.Selection = self.puzzle_data.type
        self.puzzle_num_display.LabelText = str(self.puzzle_data.number)

        self.puzz_display.SetBitmap(self.puzzle_data.bg.extract_image_wx_bitmap())

    def OnButtonSavePuzzle(self, event):
        puzzle_id = int(str(self.puzz_id_text.Value), 0)

        self.puzzle_data.set_internal_id(puzzle_id)

        try:
            self.puzzle_data.text = auto_newline(str(self.puzz_txt_input.Value), 42).encode("ascii")
            self.puzzle_data.correct_answer = auto_newline(str(self.correct_input.Value), 38).encode("ascii")
            self.puzzle_data.incorrect_answer = auto_newline(str(self.incorrect_input.Value), 38).encode("ascii")
            self.puzzle_data.hint1 = auto_newline(str(self.hint1_input.Value), 38).encode("ascii")
            self.puzzle_data.hint2 = auto_newline(str(self.hint2_input.Value), 38).encode("ascii")
            self.puzzle_data.hint3 = auto_newline(str(self.hint3_input.Value), 38).encode("ascii")
            self.puzzle_data.title = auto_newline(str(self.puzz_title_input.Value), 38).encode("ascii")
            self.puzzle_data.type = self.puzzle_type_choice.Selection
        except UnicodeEncodeError:
            error_unicode = wx.MessageDialog(self, "There can't be unicode characters in the texts",
                                             style=wx.ICON_ERROR | wx.OK)
            error_unicode.ShowModal()
            return

        self.puzzle_data.save_to_rom()

        successful = wx.MessageDialog(self, "Saved successfully")
        successful.ShowModal()
