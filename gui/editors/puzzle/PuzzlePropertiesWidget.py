from gui.ui.puzzle.PuzzlePropertiesWidget import PuzzlePropertiesWidgetUI
from formats.puzzle import Puzzle
from PySide6 import QtCore, QtWidgets, QtGui


class PuzzlePropertiesWidget(PuzzlePropertiesWidgetUI):
    def __init__(self, *args, **kwargs):
        super(PuzzlePropertiesWidget, self).__init__(*args, **kwargs)
        self.puzzle: Puzzle = None

    def set_puzzle(self, puzzle: Puzzle):
        self.puzzle = puzzle
        self.number_spin.setValue(self.puzzle.number)
        self.title_input.setText(self.puzzle.title)
        self.type_combo.set_type(self.puzzle.type)
        self.bg_btm_id_spin.setValue(self.puzzle.bg_btm_id)
        self.bg_location_id_spin.setValue(self.puzzle.bg_location_id)
        self.location_id_spin.setValue(self.puzzle.location_id)
        self.reward_id_spin.setValue(self.puzzle.reward_id)
        self.tutorial_id_spin.setValue(self.puzzle.tutorial_id)
        for i in range(3):
            self.picarat_decay_spins[i].setValue(self.puzzle.picarat_decay[i])
        self.text_input.setPlainText(self.puzzle.text)
        self.correct_input.setPlainText(self.puzzle.correct_answer)
        self.incorrect_input.setPlainText(self.puzzle.incorrect_answer)
        self.hint_1_input.setPlainText(self.puzzle.hint1)
        self.hint_2_input.setPlainText(self.puzzle.hint2)
        self.hint_3_input.setPlainText(self.puzzle.hint3)
        self.bg_lang_checkbox.setChecked(self.puzzle.bg_lang)
        self.ans_bg_lang_checkbox.setChecked(self.puzzle.ans_bg_lang)
        self.flag_2_bit_checkbox.setChecked(self.puzzle.flag_bit2)
        self.flag_5_bit_checkbox.setChecked(self.puzzle.flag_bit5)
        self.judge_character_input.setValue(self.puzzle.judge_char)

    def number_spin_edit(self, value: int):
        self.puzzle.number = value

    def title_input_edit(self, value: str):
        self.puzzle.title = value

    def type_combo_edit(self, _index: int):
        self.puzzle.type = self.type_combo.get_type()

    def bg_btm_id_spin_edit(self, value: int):
        self.puzzle.bg_btm_id = value

    def bg_location_id_spin_edit(self, value: int):
        self.puzzle.bg_location_id = value

    def location_id_spin_edit(self, value: int):
        self.puzzle.location_id = value

    def reward_id_spin_edit(self, value: int):
        self.puzzle.reward_id = value

    def tutorial_id_spin_edit(self, value: int):
        self.puzzle.tutorial_id = value

    def picarat_decay_edit(self, idx: int, value: int):
        self.puzzle.picarat_decay[idx] = value

    def bg_lang_checkbox_edit(self, state: int):
        self.puzzle.bg_lang = state == QtCore.Qt.CheckState.Checked

    def ans_bg_lang_checkbox_edit(self, state: int):
        self.puzzle.ans_bg_lang = state == QtCore.Qt.CheckState.Checked

    def flag_2_bit_checkbox_edit(self, state: int):
        self.puzzle.flag_bit2 = state == QtCore.Qt.CheckState.Checked

    def flag_5_bit_checkbox_edit(self, state: int):
        self.puzzle.flag_bit5 = state == QtCore.Qt.CheckState.Checked

    def text_input_edit(self):
        self.puzzle.text = self.text_input.toPlainText()

    def correct_input_edit(self):
        self.puzzle.correct_answer = self.correct_input.toPlainText()

    def incorrect_input_edit(self):
        self.puzzle.incorrect_answer = self.incorrect_input.toPlainText()

    def hint_1_input_edit(self):
        self.puzzle.hint1 = self.hint_1_input.toPlainText()

    def hint_2_input_edit(self):
        self.puzzle.hint2 = self.hint_2_input.toPlainText()

    def hint_3_input_edit(self):
        self.puzzle.hint3 = self.hint_3_input.toPlainText()

    def judge_character_input_edit(self, value: int):
        self.puzzle.judge_char = value
