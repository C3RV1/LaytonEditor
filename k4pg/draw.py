from typing import List, Union, Tuple

from .Camera import Camera
import pygame as pg


def rect(cam: Camera, color: pg.Color, rect_: Union[pg.Rect, List],
         width=0, border_radius=0, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1,
         border_bottom_right_radius=-1, use_world=True):
    rect_ = pg.Rect(rect_)
    cam.set_surf_clip()
    pos = pg.Vector2(rect_.x, rect_.y)
    pos = cam.to_screen(pos, use_world=use_world)
    rect_.x = pos.x
    rect_.y = pos.y
    rect_.w *= cam.zoom.x
    rect_.h *= cam.zoom.y
    return pg.draw.rect(cam.surf, color, rect_, width=width, border_radius=border_radius,
                        border_top_left_radius=border_top_left_radius,
                        border_top_right_radius=border_top_right_radius,
                        border_bottom_left_radius=border_bottom_left_radius,
                        border_bottom_right_radius=border_bottom_right_radius)


def polygon(cam: Camera, color: pg.Color,
            points: Union[List[Union[Tuple, List, pg.Vector2]], Tuple[Union[Tuple, List, pg.Vector2]]],
            width=0, use_world=True):
    cam.set_surf_clip()
    screen_points = []
    for point in points:
        screen_points.append(cam.to_screen(pg.Vector2(point), use_world=use_world))
    return pg.draw.polygon(cam.surf, color, screen_points, width=width)


def circle(cam: Camera, color: pg.Color, center: Union[pg.Vector2, List, Tuple], radius: Union[int, float],
           width=0, draw_top_right=0, draw_top_left=0, draw_bottom_left=0, draw_bottom_right=0,
           use_world=True):
    cam.set_surf_clip()
    center = cam.to_screen(pg.Vector2(center), use_world=use_world)
    radius_x = radius * cam.zoom.x
    radius_y = radius * cam.zoom.y
    if radius_x == radius_y:
        return pg.draw.circle(cam.surf, color, center, radius_x, width=width, draw_top_right=draw_top_right,
                              draw_top_left=draw_top_left, draw_bottom_left=draw_bottom_left,
                              draw_bottom_right=draw_bottom_right)
    else:
        rect_ = pg.Rect(center.x - radius_x, center.y - radius_y, radius_x*2, radius_y*2)
        return pg.draw.ellipse(cam.surf, color, rect_, width=width)


def ellipse(cam: Camera, color: pg.Color, rect_: Union[pg.Rect, List[int]], width=0, use_world=True):
    rect_ = pg.Rect(rect_)
    cam.set_surf_clip()
    pos = pg.Vector2(rect_.x, rect_.y)
    pos = cam.to_screen(pos, use_world=use_world)
    rect_.x = pos.x
    rect_.y = pos.y
    rect_.w *= cam.zoom.x
    rect_.h *= cam.zoom.y
    return pg.draw.ellipse(cam.surf, color, rect_, width=width)


def arc(cam: Camera, color: pg.Color, rect_: Union[pg.Rect, List[int]], start_angle: float, stop_angle: float,
        width=1, use_world=True):
    rect_ = pg.Rect(rect_)
    cam.set_surf_clip()
    pos = pg.Vector2(rect_.x, rect_.y)
    pos = cam.to_screen(pos, use_world=use_world)
    rect_.x = pos.x
    rect_.y = pos.y
    rect_.w *= cam.zoom.x
    rect_.h *= cam.zoom.y
    return pg.draw.arc(cam.surf, color, rect_, start_angle, stop_angle, width=width)


def line(cam: Camera, color: pg.Color, start_pos: Union[pg.Vector2, List, Tuple],
         end_pos: Union[pg.Vector2, List, Tuple], width=1, use_world=True):
    cam.set_surf_clip()
    start_pos = pg.Vector2(start_pos)
    start_pos = cam.to_screen(start_pos, use_world=use_world)
    end_pos = pg.Vector2(end_pos)
    end_pos = cam.to_screen(end_pos, use_world=use_world)
    return pg.draw.line(cam.surf, color, start_pos, end_pos, width=width)


def lines(cam: Camera, color: pg.Color, closed: bool,
          points: Union[List[Union[Tuple, List, pg.Vector2]], Tuple[Union[Tuple, List, pg.Vector2]]],
          width=1, use_world=True, ):
    changed_rect: Union[pg.Rect, None] = None
    for i in range(len(points) - (0 if closed else 1)):
        point_1 = points[i]
        point_2 = points[(i + 1) % len(points)]
        rect_ = line(cam, color, point_1, point_2, use_world=use_world, width=width)
        if changed_rect is None:
            changed_rect = rect_
        else:
            changed_rect.union_ip(rect_)
    if changed_rect is None:
        changed_rect = pg.Rect(0, 0, 0, 0)
    return changed_rect


def aaline(cam: Camera, color: pg.Color, start_pos: Union[pg.Vector2, List, Tuple],
           end_pos: Union[pg.Vector2, List, Tuple], blend=1, use_world=True):
    cam.set_surf_clip()
    start_pos = pg.Vector2(start_pos)
    start_pos = cam.to_screen(start_pos, use_world=use_world)
    end_pos = pg.Vector2(end_pos)
    end_pos = cam.to_screen(end_pos, use_world=use_world)
    return pg.draw.aaline(cam.surf, color, start_pos, end_pos, blend=blend)


def aalines(cam: Camera, color: pg.Color, closed: bool,
            points: Union[List[Union[Tuple, List, pg.Vector2]], Tuple[Union[Tuple, List, pg.Vector2]]],
            blend=1, use_world=True):
    changed_rect: Union[pg.Rect, None] = None
    for i in range(len(points) - (0 if closed else 1)):
        point_1 = points[i]
        point_2 = points[(i + 1) % len(points)]
        rect_ = aaline(cam, color, point_1, point_2, use_world=use_world, blend=blend)
        if changed_rect is None:
            changed_rect = rect_
        else:
            changed_rect.union_ip(rect_)
    if changed_rect is None:
        changed_rect = pg.Rect(0, 0, 0, 0)
    return changed_rect
