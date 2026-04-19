import pygame as pg

from component.ball import Ball
# from component.group import Group  # 良くない気がする


class GroupedBall(Ball):

    def __init__(self, group):
        self._group = group
        super().__init__()

    def get_pos(self, sf: pg.Surface) -> tuple[int, int]:
        return self._group.get_ball_pos(sf, self)
