import pygame as pg

from effect.effect import Effect


class EffectManager:

    def __init__(self):
        self._effects: set[Effect] = set()

    def add(self, e: Effect):
        self._effects.add(e)

    def update(self):
        for e in self._effects.copy():  # shallow copy
            e.update()
            if e.should_destroy:
                self._effects.remove(e)

    def draw(self, sf: pg.Surface):
        for e in self._effects:
            e.draw(sf)
