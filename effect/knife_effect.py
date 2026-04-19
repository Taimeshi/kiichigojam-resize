import numpy as np
import pygame as pg

from effect import Effect
from consts import *


class KnifeEffect(Effect):

    def __init__(self, start_vector: np.ndarray, end_vector: np.ndarray):
        self._start_v = start_vector
        self._dir_v = end_vector - start_vector
        self._ortho_v = np.array([-self._dir_v[1], self._dir_v[0]])
        self._ortho_v /= np.linalg.norm(self._ortho_v)
        self._tmr: int = 0

    @property
    def should_destroy(self) -> bool:
        return self._tmr >= 30

    def draw(self, sf: pg.Surface):
        if self.should_destroy:
            return
        alpha = 255
        tmp_sf = pg.Surface(sf.get_size(), pg.SRCALPHA)
        tmp_sf.fill(VOID)

        if self._tmr < 10:
            pg.draw.line(tmp_sf, WHITE,
                         self._start_v, self._start_v + self._dir_v * (self._tmr / 10),
                         self._tmr)
        elif self._tmr < 30:
            alpha = 255 - min(255, (self._tmr-10) * 20)
            tmp = (self._tmr - 10) * 5
            pg.draw.line(tmp_sf, WHITE,
                         self._start_v, self._start_v + self._dir_v,
                         10)
            pg.draw.line(tmp_sf, CREAM,
                         self._start_v + self._ortho_v * tmp,
                         self._start_v + self._dir_v + self._ortho_v * tmp, 10)
            pg.draw.line(tmp_sf, CREAM,
                         self._start_v - self._ortho_v * tmp,
                         self._start_v + self._dir_v - self._ortho_v * tmp, 10)

        tmp_sf.set_alpha(alpha)
        sf.blit(tmp_sf, [0, 0])

    def update(self):
        self._tmr += 1

