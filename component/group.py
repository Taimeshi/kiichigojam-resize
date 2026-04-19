from abc import ABCMeta, abstractmethod
import pygame as pg

from component.grouped_ball import GroupedBall


class Group(metaclass=ABCMeta):

    def __init__(self, num: int):
        self.balls: list[GroupedBall] = []
        self._num: int = num

    @abstractmethod
    def update(self) -> None:
        ...

    @abstractmethod
    def draw(self, sf: pg.surface.Surface) -> None:
        ...

    @abstractmethod
    def get_ball_pos(self, sf: pg.Surface, ball: GroupedBall) -> tuple[int, int]:
        ...
