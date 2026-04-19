from component.ball import Ball
import pygame as pg


class StableBall(Ball):

    def __init__(self, x: int, y: int):
        self._x: int = x
        self._y: int = y

        super().__init__()

    def get_pos(self, sf: pg.Surface):
        return self._x * (sf.get_width() / 600), self._y * (sf.get_height() / 400)
