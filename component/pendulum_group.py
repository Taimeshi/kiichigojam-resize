import pygame as pg
import numpy as np

from component.group import Group
from component.grouped_ball import GroupedBall
from consts import *


class PendulumGroup(Group):

    def __init__(self, pos: tuple[int, int], length: int, max_angle: int, speed: int):
        super().__init__(1)
        self.balls.append(GroupedBall(self))
        self._pos = pos
        self._length = length
        self._max_angle = max_angle
        self._speed = speed
        self._tmr: int = 0

    def _get_resized_pos(self, sf: pg.Surface) -> tuple[int, int]:
        return int(self._pos[0] * (sf.get_width() / 600)), int(self._pos[1] * (sf.get_height() / 400))

    def update(self) -> None:
        self._tmr += self._speed

    def draw(self, sf: pg.Surface) -> None:
        pos = self._get_resized_pos(sf)
        length = self._length * ((sf.get_width() / 600) + (sf.get_height() / 400)) / 2

        pg.draw.circle(sf, CREAM, pos, 5)
        rad = np.deg2rad(np.sin(self._tmr / 50) * self._max_angle)
        pg.draw.line(sf, CREAM, pos,
                     (int(pos[0] + np.sin(rad) * length), int(pos[1] + np.cos(rad) * length)), 2)

    def get_ball_pos(self, sf: pg.Surface, ball: GroupedBall) -> tuple[int, int]:
        pos = self._get_resized_pos(sf)
        length = self._length * ((sf.get_width() / 600) + (sf.get_height() / 400)) / 2

        rad = np.deg2rad(np.sin(self._tmr / 50) * self._max_angle)
        return int(pos[0] + np.sin(rad) * length), int(pos[1] + np.cos(rad) * length)
