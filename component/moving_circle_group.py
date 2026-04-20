from typing import override

import pygame as pg
import numpy as np

from component import CircleGroup
from component.grouped_ball import GroupedBall
from consts import *


class MovingCircleGroup(CircleGroup):

    def __init__(self, num: int, pos: tuple[int, int], default_radius: int, speed: int):
        super().__init__(num, pos, default_radius, speed)
        self._default_radius = default_radius
        for _ in range(num):
            self.balls.append(GroupedBall(self))

    @override
    @property
    def _radius(self) -> int:
        return self._default_radius + int(np.sin(self._tmr / 50) * 40)
