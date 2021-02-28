import pygame as pg
import PygameEngine.Sprite
import PygameEngine.Screen


class Camera:
    def __init__(self):
        self.position = [0, 0]
        self.cam_alignment = [PygameEngine.Sprite.Sprite.ALIGNMENT_CENTER, PygameEngine.Sprite.Sprite.ALIGNMENT_CENTER]
        self.display_port: pg.rect.Rect = None

        self.scale = 1

    def draw(self, group: pg.sprite.AbstractGroup, dirty_all=False):
        self.check_display_port()
        for sprite in group.sprites():
            if isinstance(sprite, PygameEngine.Sprite.Sprite):
                sprite: PygameEngine.Sprite.Sprite
                sprite.cam_updated = False
                if sprite.cam_scale != self.scale and self.scale != 1 and sprite.world_rect.w != 0:
                    sprite.cam_scale = self.scale
                    sprite.scale_by_factor([1, 1])
                    sprite.cam_updated = True
                if sprite.current_camera is not self:
                    sprite.current_camera = self
                if dirty_all:
                    if sprite.dirty < 1:
                        sprite.dirty = 1
                self.transform_world_into_screen(sprite)

    def check_display_port(self):
        screen_size = PygameEngine.Screen.Screen.screen_size()
        if self.display_port is None or not isinstance(self.display_port, pg.Rect):
            self.display_port = pg.Rect(0, 0, screen_size[0], screen_size[1])

    def transform_world_into_screen(self, sprite: PygameEngine.Sprite.Sprite):
        prev_rect = sprite.rect
        sprite.rect = sprite.world_rect.copy()
        # sprite.rect.x *= self.scale
        # sprite.rect.y *= self.scale

        if sprite.draw_alignment[0] == PygameEngine.Sprite.Sprite.ALIGNMENT_CENTER:
            sprite.rect.x -= sprite.rect.w // 2
        elif sprite.draw_alignment[0] == PygameEngine.Sprite.Sprite.ALIGNMENT_LEFT:
            sprite.rect.x -= sprite.rect.w
        if sprite.draw_alignment[1] == PygameEngine.Sprite.Sprite.ALIGNMENT_CENTER:
            sprite.rect.y -= sprite.rect.h // 2
        elif sprite.draw_alignment[1] == PygameEngine.Sprite.Sprite.ALIGNMENT_BOTTOM:
            sprite.rect.y -= sprite.rect.h

        sprite.rect.x, sprite.rect.y = self.world_to_screen(sprite.rect.x, sprite.rect.y, is_world=sprite.is_world)
        sprite.rect.w *= self.scale
        sprite.rect.h *= self.scale
        self.clip_in_cam(sprite)

        sprite.rect.x = int(sprite.rect.x)
        sprite.rect.y = int(sprite.rect.y)
        if sprite.rect != prev_rect:
            sprite.cam_updated = True
            if sprite.dirty < 1:
                sprite.dirty = 1

    def clip_in_cam(self, sprite: PygameEngine.Sprite.Sprite):
        if sprite.source_rect_pre is None:
            sprite.source_rect = pg.Rect(0, 0, sprite.rect.w, sprite.rect.h)
        else:
            sprite.source_rect = sprite.source_rect_pre.copy()
            sprite.source_rect.x *= self.scale
            sprite.source_rect.y *= self.scale
            sprite.source_rect.w *= self.scale
            sprite.source_rect.h *= self.scale

        source_rect_screen = sprite.source_rect.copy()
        source_rect_screen.x = sprite.rect.x
        source_rect_screen.y = sprite.rect.y

        if source_rect_screen.x < self.display_port.x:
            difference = self.display_port.x - source_rect_screen.x
            sprite.source_rect.x += difference
            sprite.source_rect.w -= difference
            sprite.rect.x += difference
            sprite.rect.w -= difference
        if source_rect_screen.x + source_rect_screen.w > self.display_port.x + self.display_port.w:
            difference = (source_rect_screen.x + source_rect_screen.w) - (self.display_port.x + self.display_port.w)
            sprite.source_rect.w -= difference
            sprite.rect.w -= difference

        if source_rect_screen.y < self.display_port.y:
            difference = self.display_port.y - source_rect_screen.y
            sprite.source_rect.y += difference
            sprite.source_rect.h -= difference
            sprite.rect.y += difference
            sprite.rect.h -= difference
        if source_rect_screen.y + source_rect_screen.h > self.display_port.y + self.display_port.h:
            difference = (source_rect_screen.y + source_rect_screen.h) - (self.display_port.y + self.display_port.h)
            sprite.source_rect.h -= difference
            sprite.rect.h -= difference

        sprite.source_rect.w = max(sprite.source_rect.w, 0)
        sprite.source_rect.h = max(sprite.source_rect.h, 0)

    def draw_line(self, line_x1, line_y1, line_x2, line_y2, color=pg.Color(255, 255, 255), is_world=True):
        if is_world:
            line_x1, line_y1 = self.world_to_screen(line_x1, line_y1)
            line_x2, line_y2 = self.world_to_screen(line_x2, line_y2)

        x1_check = line_x1 < self.display_port.x + 1 or line_x1 > self.display_port.x - 1 + self.display_port.w - 1
        y1_check = line_y1 < self.display_port.y + 1 or line_y1 > self.display_port.y - 1 + self.display_port.h - 1
        x2_check = line_x2 < self.display_port.x + 1 or line_x2 > self.display_port.x - 1 + self.display_port.w - 1
        y2_check = line_y2 < self.display_port.y + 1 or line_y2 > self.display_port.y - 1 + self.display_port.h - 1

        if x1_check or y1_check or x2_check or y2_check:
            return pg.Rect(0, 0, 0, 0)

        pg.draw.line(PygameEngine.Screen.Screen.screen(), color=color, start_pos=[line_x1, line_y1],
                     end_pos=[line_x2, line_y2])

        rect = pg.Rect(0, 0, 0, 0)
        rect.x = min(line_x1, line_x2) - 1
        rect.y = min(line_y1, line_y2) - 1
        rect.w = max(line_x1, line_x2) - rect.x + 2
        rect.h = max(line_y1, line_y2) - rect.y + 2

        return rect

    def world_to_screen(self, x1, y1, is_world=True):
        x1 *= self.scale
        y1 *= self.scale
        if is_world:
            x1 += self.position[0] * self.scale
            y1 += self.position[1] * self.scale

        if self.cam_alignment[0] == PygameEngine.Sprite.Sprite.ALIGNMENT_RIGHT:
            x1 += self.display_port.x
        elif self.cam_alignment[0] == PygameEngine.Sprite.Sprite.ALIGNMENT_CENTER:
            x1 += self.display_port.x + (self.display_port.w // 2)
        elif self.cam_alignment[0] == PygameEngine.Sprite.Sprite.ALIGNMENT_LEFT:
            x1 += self.display_port.x + self.display_port.w
        if self.cam_alignment[1] == PygameEngine.Sprite.Sprite.ALIGNMENT_BOTTOM:
            y1 += self.display_port.y
        elif self.cam_alignment[1] == PygameEngine.Sprite.Sprite.ALIGNMENT_CENTER:
            y1 += self.display_port.y + (self.display_port.h // 2)
        elif self.cam_alignment[1] == PygameEngine.Sprite.Sprite.ALIGNMENT_TOP:
            y1 += self.display_port.y + self.display_port.h
        return x1, y1

    def world_to_screen_rect(self, rect: pg.Rect, is_world=True):
        rect = rect.copy()
        rect.x *= self.scale
        rect.y *= self.scale
        rect.w *= self.scale
        rect.h *= self.scale
        if is_world:
            rect.x += self.position[0] * self.scale
            rect.y += self.position[1] * self.scale

        if self.cam_alignment[0] == PygameEngine.Sprite.Sprite.ALIGNMENT_RIGHT:
            rect.x += self.display_port.x
        elif self.cam_alignment[0] == PygameEngine.Sprite.Sprite.ALIGNMENT_CENTER:
            rect.x += self.display_port.x + (self.display_port.w // 2)
        elif self.cam_alignment[0] == PygameEngine.Sprite.Sprite.ALIGNMENT_LEFT:
            rect.x += self.display_port.x + self.display_port.w
        if self.cam_alignment[1] == PygameEngine.Sprite.Sprite.ALIGNMENT_BOTTOM:
            rect.y += self.display_port.y
        elif self.cam_alignment[1] == PygameEngine.Sprite.Sprite.ALIGNMENT_CENTER:
            rect.y += self.display_port.y + (self.display_port.h // 2)
        elif self.cam_alignment[1] == PygameEngine.Sprite.Sprite.ALIGNMENT_TOP:
            rect.y += self.display_port.y + self.display_port.h

        if rect.x < self.display_port.x:
            difference = self.display_port.x - rect.x
            rect.x += difference
            rect.w -= difference
        if rect.x + rect.w > self.display_port.x + self.display_port.w:
            difference = (rect.x + rect.w) - (self.display_port.x + self.display_port.w)
            rect.w -= difference

        if rect.y < self.display_port.y:
            difference = self.display_port.y - rect.y
            rect.y += difference
            rect.h -= difference
        if rect.y + rect.h > self.display_port.y + self.display_port.h:
            difference = (rect.y + rect.h) - (self.display_port.y + self.display_port.h)
            rect.h -= difference

        rect.w = max(rect.w, 0)
        rect.h = max(rect.h, 0)

        return rect

    def screen_to_world(self, x1, y1, is_world=True):
        if is_world:
            x1 -= self.position[0]
            y1 -= self.position[1]

        if self.cam_alignment[0] == PygameEngine.Sprite.Sprite.ALIGNMENT_RIGHT:
            x1 -= self.display_port.x
        elif self.cam_alignment[0] == PygameEngine.Sprite.Sprite.ALIGNMENT_CENTER:
            x1 -= self.display_port.x + (self.display_port.w // 2)
        elif self.cam_alignment[0] == PygameEngine.Sprite.Sprite.ALIGNMENT_LEFT:
            x1 -= self.display_port.x + self.display_port.w
        if self.cam_alignment[1] == PygameEngine.Sprite.Sprite.ALIGNMENT_BOTTOM:
            y1 -= self.display_port.y
        elif self.cam_alignment[1] == PygameEngine.Sprite.Sprite.ALIGNMENT_CENTER:
            y1 -= self.display_port.y + (self.display_port.h // 2)
        elif self.cam_alignment[1] == PygameEngine.Sprite.Sprite.ALIGNMENT_TOP:
            y1 -= self.display_port.y + self.display_port.h

        x1 /= self.scale
        y1 /= self.scale

        return x1, y1
