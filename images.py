import pygame as pg
import os
from consts import RESOURCE_PATH

"""
全てIcons8の素材 (編集を加えたもの)を使用しています。
"""


def _load(filename: str) -> pg.Surface:
    return pg.image.load(os.path.join(RESOURCE_PATH, filename)).convert_alpha()


knife_img = _load("knife.png")
cursor_img = _load("cursor.png")
restart_img = _load("restart.png")
