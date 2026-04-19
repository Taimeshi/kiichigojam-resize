from abc import ABCMeta, abstractmethod
import pygame as pg


class Effect(metaclass=ABCMeta):

    @property
    @abstractmethod
    def should_destroy(self) -> bool:
        ...

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def draw(self, sf):
        ...
