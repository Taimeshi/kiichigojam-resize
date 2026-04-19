from abc import ABCMeta, abstractmethod
import pygame as pg


class Ball(metaclass=ABCMeta):

    def __init__(self) -> None:
        self.broken: bool = False

    @abstractmethod
    def get_pos(self, sf: pg.Surface) -> tuple[int, int]:
        ...
