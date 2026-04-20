import pygame as pg

from component.ball import Ball
import component
# from component.group import Group  # 循環参照


class GroupedBall(Ball):

    def __init__(self, group: 'component.group.Group'):
        self._group = group  # やめたい
        super().__init__()

    def get_pos(self, sf: pg.Surface) -> tuple[int, int]:
        return self._group.get_ball_pos(sf, self)
