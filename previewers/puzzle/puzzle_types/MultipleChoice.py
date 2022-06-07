from ..PuzzlePlayer import PuzzlePlayer
from formats.puzzle import Puzzle
from formats.gds import GDSCommand
import pg_engine as pge


class MultipleChoiceButton(pge.Button):
    def __init__(self, is_solution, *args, **kwargs):
        super(MultipleChoiceButton, self).__init__(*args, **kwargs)
        self.center = [pge.Alignment.LEFT, pge.Alignment.TOP]
        self.is_solution: bool = is_solution
        self.not_pressed_tag = "off"
        self.pressed_tag = "on"


class MultipleChoice(PuzzlePlayer):
    def __init__(self, puzzle_data: Puzzle):
        self.buttons = []
        self.pressed_btn: MultipleChoiceButton = None

        super(MultipleChoice, self).__init__(puzzle_data)
        self.submit_btn.visible = False

    def run_gds_cmd(self, cmd: GDSCommand):
        if cmd.command == 0x14:  # add_button
            x, y, path, is_solution, _ = cmd.params
            btn = MultipleChoiceButton(is_solution == 1, position=[-256//2 + x, -192//2 + y])
            self.sprite_loader.load(f"data_lt2/ani/nazo/freebutton/{path}", btn, sprite_sheet=True)
            self.buttons.append(btn)

    def solution_submitted(self, dt):
        for button in self.buttons:
            if button.pressed(self.btm_camera, dt):
                self.pressed_btn = button
                button.animate(dt)
                return True
            button.animate(dt)
        return False

    def check_solution(self):
        return self.pressed_btn.is_solution

    def draw_base(self):
        super(MultipleChoice, self).draw_base()
        for button in self.buttons:
            button.draw(self.btm_camera)
