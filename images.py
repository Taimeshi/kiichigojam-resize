import pygame as pg
import os
from consts import PATH

"""
全てIcons8(icons8.com)の素材 (着色、拡大縮小を施したもの)を使用しています。
"""

_sprites = pg.image.load(os.path.join(PATH, "resources", "sprites.png")).convert_alpha()
icon = pg.image.load(os.path.join(PATH, "resources", "icon.ico"))

knife_img = _sprites.subsurface([0, 0, 40, 40])
restart_img = _sprites.subsurface([40, 0, 40, 40])
cursor_img = _sprites.subsurface([80, 0, 24, 24])

# knife_img = _load("knife.png")
# cursor_img = _load("cursor.png")
# restart_img = _load("restart.png")
