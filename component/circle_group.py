import pygame as pg
import numpy as np

from component.group import Group
from component.grouped_ball import GroupedBall
from consts import *


class CircleGroup(Group):

    def __init__(self, num: int, pos: tuple[int, int], radius: int, speed: int):
        super().__init__(num)
        for _ in range(num):
            self.balls.append(GroupedBall(self))
        self._pos = pos
        self._radius = radius
        self._speed = speed
        self._tmr: int = 0

    def update(self) -> None:
        self._tmr += self._speed

    def draw(self, sf: pg.Surface):
        pos = (self._pos[0] * (sf.get_width() / 600), self._pos[1] * (sf.get_height() / 400))
        radius = self._radius * ((sf.get_width() / 600) + (sf.get_height() / 400)) / 2

        for i in range(12):
            pg.draw.arc(sf, CREAM,
                        [pos[0] - radius, pos[1] - radius,
                         radius * 2, radius * 2],
                        np.deg2rad(self._tmr + i * 30), np.deg2rad(self._tmr + i * 30 + 15),
                        3)

    def get_ball_pos(self, sf: pg.Surface, ball: GroupedBall) -> tuple[int, int]:
        pos = (self._pos[0] * (sf.get_width() / 600), self._pos[1] * (sf.get_height() / 400))
        radius = self._radius * ((sf.get_width() / 600) + (sf.get_height() / 400)) / 2
        idx = self.balls.index(ball)
        deg = self._tmr + (360 / self._num) * idx
        rad = np.deg2rad(deg)
        return pos[0] + np.cos(rad) * radius, pos[1] - np.sin(rad) * radius
