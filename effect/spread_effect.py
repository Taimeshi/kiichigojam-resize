import random
import numpy as np
import pygame as pg

from effect import Effect
from consts import *


class _Particle:

    def __init__(self, pos: np.ndarray, dir_vec: np.ndarray, size: int):
        self.pos = pos
        self.dir_vec = dir_vec
        self.size = size


class SpreadEffect(Effect):

    def __init__(self, pos: tuple[int, int]):
        self._tmr: int = 0
        self._particles: set[_Particle] = set()
        for _ in range(20):
            rad = random.random() * np.pi * 2
            dir_vec = np.array([np.cos(rad), np.sin(rad)]) * (random.random() * 5 + 1)
            self._particles.add(_Particle(np.array(pos, dtype=float), dir_vec, random.randint(2, 5)))

    @property
    def should_destroy(self) -> bool:
        return self._tmr > 255 / 10

    def update(self) -> None:
        self._tmr += 1
        for p in self._particles:
            p.pos += p.dir_vec

    def draw(self, sf: pg.Surface) -> None:
        tmp_sf = pg.surface.Surface(sf.get_size(), pg.SRCALPHA)
        tmp_sf.fill(VOID)

        for p in self._particles:
            pg.draw.circle(tmp_sf, CREAM, p.pos, p.size)

        tmp_sf.set_alpha(max(255 - self._tmr * 10, 0))
        sf.blit(tmp_sf, [0, 0])
