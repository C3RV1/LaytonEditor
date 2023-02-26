from typing import List

from formats.gds import GDSCommand
from formats import conf
from ..PuzzlePlayer import PuzzlePlayer
from formats.puzzle import Puzzle
import k4pg
import pygame as pg


class SlideTile(k4pg.Sprite):
    PIXELS_PER_SEC = 256

    def __init__(self, board: 'SlideBoard', tile_pos, *args, **kwargs):
        super(SlideTile, self).__init__(*args, **kwargs)
        self.board: 'SlideBoard' = board
        self.colliders = []
        self.tile_pos = pg.Vector2(tile_pos)
        self.original_tile_pos = pg.Vector2(tile_pos)
        # Real position of the object
        self.internal_pos = pg.Vector2(0, 0)
        self.update_pos()
        # This position is visual - used for interpolation
        self.position = pg.Vector2(self.internal_pos)
        self.center.update(k4pg.Alignment.LEFT, k4pg.Alignment.TOP)
        self.inp = k4pg.Input()
        self.interacting = False
        self.interact_off = pg.Vector2(0, 0)

    def reset(self):
        self.tile_pos.update(self.original_tile_pos)
        self.update_pos()

    def get_world_colliders(self):
        # Transform tile colliders to world pixel colliders
        for collider in self.colliders:
            collider: pg.Rect
            pos, size = pg.Vector2(collider.x, collider.y), pg.Vector2(collider.size)
            pos *= self.board.tile_size.elementwise()
            pos += self.internal_pos
            size *= self.board.tile_size.elementwise()
            yield pg.Rect(pos.x, pos.y, size.x, size.y)

    def update_pos(self):
        # Transform tile pos to pixel pos
        self.tile_pos.x = round(self.tile_pos.x)
        self.tile_pos.y = round(self.tile_pos.y)
        self.internal_pos = self.tile_pos * self.board.tile_size.elementwise() + self.board.pos

    def update(self, cam: k4pg.Camera, dt: float):
        if not self.interacting:
            # Interpolate position
            move = self.internal_pos - self.position
            move.x = min(max(move.x, -self.PIXELS_PER_SEC * dt), self.PIXELS_PER_SEC * dt)
            move.y = min(max(move.y, -self.PIXELS_PER_SEC * dt), self.PIXELS_PER_SEC * dt)
            self.position += move

            # Check if we should interact
            if self.inp.get_mouse_down(1):
                mouse_pos = pg.Vector2(self.inp.get_mouse_pos())
                mouse_pos = cam.from_screen(mouse_pos)
                for collider in self.get_world_colliders():
                    if collider.collidepoint(mouse_pos.x, mouse_pos.y):
                        self.interacting = True
                        self.interact_off = self.internal_pos - mouse_pos
        else:
            mouse_pos = self.inp.get_mouse_pos()
            mouse_pos = pg.Vector2(cam.from_screen(mouse_pos))

            # Move in steps towards the destination
            self.move_steps(mouse_pos + self.interact_off, dt)

            # Internal position does already interpolate here
            self.position.update(self.internal_pos)

            # Check if we should stop interaction
            if self.inp.get_mouse_up(1):
                self.interacting = False
                self.update_pos()
        return self.interacting

    def draw(self, cam: k4pg.Camera):
        super(SlideTile, self).draw(cam)
        if conf.DEBUG_PUZZLE:
            for collider in self.get_world_colliders():
                k4pg.draw.rect(cam, pg.Color(0, 255, 0), collider, width=2)

    def move_steps(self, position_expected: pg.Vector2, dt: float):
        board = self.board.get_board_rect()

        def check_collision():
            for collider in self.get_world_colliders():
                if not board.contains(collider):
                    return True
                for collider2 in self.board.get_all_colliders_except(self):
                    if collider.colliderect(collider2):
                        return True
            return False

        self.tile_pos = (self.internal_pos - self.board.pos) / self.board.tile_size.elementwise()
        self.tile_pos.x = round(self.tile_pos.x)
        self.tile_pos.y = round(self.tile_pos.y)
        change = max(min(position_expected.x - self.internal_pos.x, self.PIXELS_PER_SEC * dt),
                     -self.PIXELS_PER_SEC * dt)
        self.internal_pos.x += change
        if check_collision():
            self.internal_pos.x = self.tile_pos.x * self.board.tile_size.x + self.board.pos.x
        change = max(min(position_expected.y - self.internal_pos.y, self.PIXELS_PER_SEC * dt),
                     -self.PIXELS_PER_SEC * dt)
        self.internal_pos.y += change
        if check_collision():
            self.internal_pos.y = self.tile_pos.y * self.board.tile_size.y + self.board.pos.y


class SlideBoard:
    def __init__(self):
        self.tiles: List[SlideTile] = []
        self.tile_size = pg.Vector2(0, 0)
        self.pos = pg.Vector2(0, 0)
        self.size = pg.Vector2(0, 0)
        self.occlusions = []

    def get_board_rect(self):
        return pg.Rect(self.pos.x, self.pos.y,
                       self.size.x * self.tile_size.x,
                       self.size.y * self.tile_size.y)

    def get_all_colliders_except(self, tile_except):
        for tile in self.tiles:
            if tile is tile_except:
                continue
            for collider in tile.get_world_colliders():
                yield collider
        for occlusion in self.occlusions:
            yield occlusion

    def setup(self, pos_x, pos_y, tiles_x, tiles_y, tile_size_x, tile_size_y):
        self.pos.update(pos_x - (256 // 2), pos_y - (192 // 2))
        self.size.update(tiles_x, tiles_y)
        self.tile_size.update(tile_size_x, tile_size_y)

    def add_occlusion(self, x, y, w, h):
        x *= self.tile_size.x
        x += self.pos.x
        y *= self.tile_size.y
        y += self.pos.y
        w *= self.tile_size.x
        h *= self.tile_size.y
        self.occlusions.append(pg.Rect(x, y, w, h))

    def add_tile(self, tile):
        self.tiles.append(tile)

    def tile_add_collider(self, collider: pg.Rect):
        self.tiles[-1].colliders.append(collider)


class Slide(PuzzlePlayer):
    def __init__(self, puzzle_data: Puzzle):
        self.board = SlideBoard()
        self.solutions = {}
        self.tilemap = ""
        self.interacting_tile_pos = pg.Vector2(0, 0)
        self.interacting_tile = None

        super(Slide, self).__init__(puzzle_data)
        self.submit_btn.visible = False

        self.move_count = 0
        self.move_counters = []
        current_x = 113 - 256 // 2
        for i in range(4):
            move_counter_digit = k4pg.Sprite(position=pg.Vector2(current_x, 11 - 192 // 2),
                                             center=pg.Vector2(k4pg.Alignment.LEFT, k4pg.Alignment.TOP))
            self.sprite_loader.load("data_lt2/ani/nazo/common/counter_number.arc", move_counter_digit, True)
            move_counter_digit.set_tag("0")
            current_x += 6
            self.move_counters.append(move_counter_digit)

    def update_move_counter(self):
        move_count_copy = self.move_count
        for i in range(4):
            move_counter = self.move_counters[3 - i]
            move_counter.set_tag(str(move_count_copy % 10))
            move_count_copy //= 10

    def run_gds_cmd(self, cmd: GDSCommand):
        if cmd.command == 0x4e:  # Setup
            pos_x, pos_y, tiles_x, tiles_y, tile_size_x, tile_size_y = cmd.params
            self.board.setup(pos_x, pos_y, tiles_x, tiles_y, tile_size_x, tile_size_y)
        elif cmd.command == 0x4f:  # Add Occlusion
            tile_x, tile_y, tile_w, tile_h = cmd.params
            self.board.add_occlusion(tile_x, tile_y, tile_w, tile_h)
        elif cmd.command == 0x50:  # Set Solution
            tile_idx, sol_x, sol_y = cmd.params
            self.solutions[tile_idx] = (sol_x, sol_y)
        elif cmd.command == 0x51:  # Set Tilemap
            self.tilemap = f"data_lt2/ani/nazo/slide/{cmd.params[0]}"
        elif cmd.command == 0x52:  # Add Tile
            _unk, anim, _anim2, tile_x, tile_y = cmd.params
            tile = SlideTile(self.board, pg.Vector2(tile_x, tile_y))
            self.sprite_loader.load(self.tilemap, tile, True)
            tile.set_tag(anim)
            self.board.add_tile(tile)
        elif cmd.command == 0x53:  # Add Tile Collider
            tile_x, tile_y, tile_w, tile_h = cmd.params
            self.board.tile_add_collider(pg.Rect(tile_x, tile_y, tile_w, tile_h))

    def update_submitted(self, dt):
        if self.interacting_tile is None:
            for tile in self.board.tiles:
                tile_pos = pg.Vector2(tile.tile_pos)
                if tile.update(self.btm_camera, dt):
                    self.interacting_tile = tile
                    self.interacting_tile_pos = tile_pos
                    break
        else:
            if not self.interacting_tile.update(self.btm_camera, dt):
                if self.interacting_tile_pos != self.interacting_tile.tile_pos:
                    self.move_count += 1
                    self.update_move_counter()
                self.interacting_tile = None
                for solution_t, solution_pos in self.solutions.items():
                    solution_tile = self.board.tiles[solution_t]
                    if solution_tile.tile_pos != solution_pos:
                        return False
                return True
        return super(Slide, self).update_submitted(dt)

    def check_solution(self):
        return True

    def restart(self):
        for tile in self.board.tiles:
            tile.reset()
            self.move_count = 0
            self.update_move_counter()

    def draw_base(self):
        super(Slide, self).draw_base()
        for tile in self.board.tiles:
            tile.draw(self.btm_camera)
        for move_counter in self.move_counters:
            move_counter.draw(self.btm_camera)
        if conf.DEBUG_PUZZLE:
            for occlusion in self.board.occlusions:
                k4pg.draw.rect(self.btm_camera, pg.Color(255, 0, 0), occlusion, width=2)
