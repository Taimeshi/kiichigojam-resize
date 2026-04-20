import os
import sys
from pathlib import Path

VOID = (0, 0, 0, 0)
BG = (255, 255, 200)  # ffffc8
CURSOR_COLOR = (204, 190, 111)  # ccbe6f
BLACK = (50, 50, 50)  # 323232
WHITE = (255, 255, 255)  # ffffff
CREAM = (239, 223, 125)  # efdf7d
RED = (255, 97, 101)  # ff6165
BLUE = (92, 184, 255)  # 5cb8ff
BROWN = (141, 80, 37)  # 8d5025


DEFAULT_WIDTH = 600
DEFAULT_HEIGHT = 400
MIN_WIDTH = 300
MIN_HEIGHT = 200
MAX_WIDTH = 900
MAX_HEIGHT = 600

if getattr(sys, 'frozen', False):
    # exe / app のとき
    if sys.platform == "darwin":
        PATH = os.path.join(os.path.dirname(sys.executable), "..")  # .app
    else:
        PATH = os.path.dirname(sys.executable)  # .exe
else:
    # 普通に python 実行
    PATH = os.path.dirname(os.path.abspath(__file__))  # .py
