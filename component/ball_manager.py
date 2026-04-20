import numpy as np
import pygame as pg

import util
from consts import *
from component.ball import Ball
from component.group import Group
from effect import EffectManager, SpreadEffect


class BallManager:

    def __init__(self):
        self._balls: set[Ball] = set()
        self._groups: set[Group] = set()

    @property
    def ball_num(self) -> int:
        return len(self._balls)

    def update(self) -> None:
        for group in self._groups:
            group.update()

    def add_ball(self, ball: Ball) -> None:
        self._balls.add(ball)

    def add_group(self, group: Group) -> None:
        self._groups.add(group)
        for ball in group.balls:
            self.add_ball(ball)

    def draw(self, sf: pg.Surface, tmr: int) -> None:
        for group in self._groups:
            group.draw(sf)
        for ball in self._balls:
            util.draw.ball(sf, CREAM, ball.get_pos(sf), tmr)

    def knife(self, start_vec: np.ndarray, dir_vec: np.ndarray, sf: pg.Surface, effect_manager: EffectManager) -> int:
        ortho_vec = np.array([-dir_vec[1], dir_vec[0]])
        ortho_vec /= np.linalg.norm(ortho_vec)

        killed_count = 0
        for b in self._balls.copy():
            ball_vec = start_vec - b.get_pos(sf)
            distance = np.linalg.norm(ball_vec @ ortho_vec)
            if distance < 40:
                effect_manager.add(SpreadEffect(b.get_pos(sf)))
                self._balls.remove(b)
                killed_count += 1

        return killed_count

    def clear(self) -> None:
        self._balls.clear()
        self._groups.clear()
