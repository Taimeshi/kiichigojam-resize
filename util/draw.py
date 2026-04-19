import math

import pygame as pg
import numpy as np
from math import cos, sin


def _rotate(vec: np.ndarray, deg: float) -> np.ndarray:
    x = np.deg2rad(deg)
    rot = np.array([[cos(x), -sin(x)], [sin(x), cos(x)]])
    return np.dot(rot, vec)


def arrow(sf: pg.Surface,
          start: tuple[int, int] | np.ndarray, end: tuple[int, int] | np.ndarray,
          color: tuple[int, int, int],
          width: int = 5, deg: float = 45, arrow_size: int = 20,
          head: tuple[bool, bool] = (True, True), guide: bool = False) -> None:
    pg.draw.line(sf, color, start, end, width)

    v = np.array([end[0] - start[0], end[1] - start[1]])
    v = v / np.linalg.norm(v) * arrow_size
    v1 = _rotate(v, deg)
    v2 = _rotate(v, -deg)

    if head[0]:
        pg.draw.line(sf, color, start, (start[0] + v1[0], start[1] + v1[1]), width)
        pg.draw.line(sf, color, start, (start[0] + v2[0], start[1] + v2[1]), width)
    if head[1]:
        pg.draw.line(sf, color, end, (end[0] - v1[0], end[1] - v1[1]), width)
        pg.draw.line(sf, color, end, (end[0] - v2[0], end[1] - v2[1]), width)

    if guide:
        v3 = np.array([v[1], -v[0]]) / np.linalg.norm(v) * arrow_size
        pg.draw.line(sf, color,
                     [start[0] - v3[0], start[1] - v3[1]], (start[0] + v3[0], start[1] + v3[1]), width)
        pg.draw.line(sf, color,
                     [end[0] - v3[0], end[1] - v3[1]], (end[0] + v3[0], end[1] + v3[1]), width)


def ball(sf: pg.Surface, color: tuple[int, int, int], pos: tuple[int, int] | np.ndarray, tmr: int) -> None:
    pg.draw.circle(sf, color, pos, 10)

    r = 17
    for i in range(3):
        pg.draw.arc(sf, color, (pos[0] - r, pos[1] - r, r * 2, r * 2),
                    np.deg2rad(-tmr * 2 + i * 120), np.deg2rad(-tmr * 2 + i * 120 + 90), 3)


def dashed_line(sf: pg.Surface, start: tuple[int, int] | np.ndarray, end: tuple[int, int] | np.ndarray,
                color: tuple[int, int, int], width: int = 5, dash_length: int = 10) -> None:
    v = np.array([end[0] - start[0], end[1] - start[1]])
    n: int = math.ceil(np.linalg.norm(v) / dash_length)
    v_u = v / np.linalg.norm(v)
    for i in range(n-1):
        if i % 2 == 0:
            pg.draw.line(sf, color,
                         start + v_u * (dash_length * i), start + v_u * (dash_length * (i + 1)), width)
    if n % 2 == 1:
        pg.draw.line(sf, color, start + v_u * (dash_length * (n-1)), end, width)
