import pygame as pg

from component.ball import Ball


class StableBall(Ball):

    def __init__(self, x: int, y: int):
        self._x: int = x
        self._y: int = y

        super().__init__()

    def get_pos(self, sf: pg.Surface) -> tuple[int, int]:
        return int(self._x * (sf.get_width() / 600)), int(self._y * (sf.get_height() / 400))
