# disable pygame welcome message
import math
import os

from component.circle_group2 import CircleGroup2
from component.pendulum_group import PendulumGroup

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame as pg
import numpy as np
import sys
from enum import Enum, auto

from consts import *
import util
import effect as ef
from component import StableBall, CircleGroup, BallManager


class Index(Enum):
    TUTORIAL = auto()
    GAME = auto()
    RESULT = auto()


def clamp_size(w, h):
    return (
        max(MIN_WIDTH, min(MAX_WIDTH, w)),
        max(MIN_HEIGHT + 50, min(MAX_HEIGHT + 50, h)),
    )


def main():
    global sc
    cl = pg.time.Clock()
    tmr = 0
    mouse_count = 0
    pg.mouse.set_visible(False)
    ft = pg.font.Font(os.path.join(RESOURCE_PATH, "nicomoji-plus_v2-5.ttf"), 25)
    ft_large = pg.font.Font(os.path.join(RESOURCE_PATH, "nicomoji-plus_v2-5.ttf"), 30)
    ft_exlarge = pg.font.Font(os.path.join(RESOURCE_PATH, "nicomoji-plus_v2-5.ttf"), 60)
    ft_title = pg.font.Font(os.path.join(RESOURCE_PATH, "nicomoji-plus_v2-5.ttf"), 100)
    main_sf = pg.Surface((DEFAULT_WIDTH, DEFAULT_HEIGHT), pg.SRCALPHA)
    effect_manager = ef.EffectManager()
    index = Index.TUTORIAL

    knife_remaining: int = 3
    ball_manager = BallManager()
    start_pos: tuple[int, int] = (0, 0)
    end_pos: tuple[int, int] = (0, 0)
    score: int = 0
    phase: int = 0
    with open(os.path.join(os.path.dirname(__file__), "best_score"), "r") as f:
        best_score = int(f.read())

    transit_count: int = 1

    while True:
        tmr += 1
        mouse_up = False
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif e.type == pg.VIDEORESIZE:
                if transit_count > 0 or index != Index.GAME:
                    sc = pg.display.set_mode(sc.get_size(), pg.RESIZABLE)
                sc = pg.display.set_mode(clamp_size(e.w, e.h), pg.RESIZABLE)
                main_sf = pg.Surface((sc.get_width(), sc.get_height() - 50), pg.SRCALPHA)
            elif e.type == pg.MOUSEBUTTONDOWN:  # for debug
                if pg.key.get_pressed()[pg.K_LSHIFT]:
                    print(pg.mouse.get_pos())
            elif e.type == pg.MOUSEBUTTONUP and e.button == 1:
                mouse_up = True
        if pg.mouse.get_pressed()[0]:
            mouse_count += 1
        else:
            mouse_count = 0
        m_x, m_y = pg.mouse.get_pos()
        sc.fill(CREAM)
        main_sf.fill(BG)

        if index == Index.TUTORIAL:
            if main_sf.get_width() != DEFAULT_WIDTH or main_sf.get_height() != DEFAULT_HEIGHT:
                sc = pg.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT + 50), pg.RESIZABLE)
                main_sf = pg.Surface((DEFAULT_WIDTH, DEFAULT_HEIGHT), pg.SRCALPHA)
            main_sf.fill(CREAM)

            title_txt = ft_title.render(f"RESIZE", True, BG)
            main_sf.blit(title_txt, ((DEFAULT_WIDTH - title_txt.get_width()) // 2, 50))

            txt1 = ft_large.render("Click Mouse to Start", True, BG)
            txt2 = ft_large.render(f"Best Score: {best_score}", True, BG)
            main_sf.blit(txt1, ((DEFAULT_WIDTH - txt1.get_width()) // 2, 200))
            main_sf.blit(txt2, ((DEFAULT_WIDTH - txt2.get_width()) // 2, 250))

            if mouse_count == 1:
                phase = 0
                transit_count = 59
                index = Index.GAME
        elif index == Index.GAME:
            if transit_count > 0:
                transit_count += 1
            if transit_count > 100:
                transit_count = 0

            # draw status bar
            util.draw.ball(sc, BG, (25, 25), 0)
            ball_txt = ft.render(f": {ball_manager.ball_num}/9", True, BG)
            sc.blit(ball_txt, (50, 10))

            sc.blit(restart_img, (145, 5))
            if mouse_count == 1:
                if 145 <= m_x <= 145 + restart_img.get_width() and 5 <= m_y < 5 + restart_img.get_height():
                    index = Index.TUTORIAL
                    ball_manager.clear()
                    score = 0
                    continue

            if main_sf.get_width() > 530:
                score_txt = ft.render(f"score: {str(score).zfill(6)}", True, BG)
                sc.blit(score_txt, (190, 10))
            pg.display.set_caption(f"Phase: {phase}/4, Score: {str(score).zfill(6)}")

            for i in range(knife_remaining):
                sc.blit(knife_img, [main_sf.get_width() - 50 - i * 30, 5])
            # ----------------

            # show width and height
            w, h = main_sf.get_size()
            w_color = CREAM
            if w == MIN_WIDTH:
                w_color = BLUE
            elif w == MAX_WIDTH:
                w_color = RED
            h_color = CREAM
            if h == MIN_HEIGHT:
                h_color = BLUE
            elif h == MAX_HEIGHT:
                h_color = RED
            txt_w = ft.render(str(w), True, w_color)
            txt_h = ft.render(str(h), True, h_color)

            util.draw.arrow(main_sf, (5, h - 20), (w - 5, h - 20), CREAM)
            main_sf.blit(txt_w, ((w - txt_w.get_width()) // 2, h - 30 - txt_w.get_height()))

            util.draw.arrow(main_sf, (w - 20, 5), (w - 20, h - 5), CREAM)
            main_sf.blit(txt_h, (w - 30 - txt_h.get_width(), (h - txt_h.get_height()) // 2))
            # ----------------

            # game logic
            if mouse_count == 1:
                start_pos = m_x, m_y - 50
            if mouse_count > 0:
                end_pos = m_x, m_y - 50
                # draw starting point
                pg.draw.line(main_sf, CREAM,
                             [start_pos[0], start_pos[1] - 10],
                             [start_pos[0], start_pos[1] + 10], 3)
                pg.draw.line(main_sf, CREAM,
                             [start_pos[0] - 10, start_pos[1]],
                             [start_pos[0] + 10, start_pos[1]], 3)

                # draw knife trajectory
                if (start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2 > 2500:
                    dir_vec = np.array([start_pos[0] - end_pos[0], start_pos[1] - end_pos[1]], dtype=float)
                    dir_vec /= np.linalg.norm(dir_vec)
                    start_vec = np.array(start_pos)
                    util.draw.dashed_line(main_sf,
                                          start_vec - dir_vec * 1000, start_vec + dir_vec * 1000, CREAM, width=4)

            if transit_count == 0:
                if mouse_up and (start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2 > 2500:
                    dir_vec = np.array([start_pos[0] - end_pos[0], start_pos[1] - end_pos[1]], dtype=float)
                    dir_vec /= np.linalg.norm(dir_vec)
                    start_vec = np.array(start_pos)
                    effect_manager.add(ef.KnifeEffect(start_vec - dir_vec * 1000, start_vec + dir_vec * 1000))
                    killed = ball_manager.knife(start_vec, dir_vec, main_sf, effect_manager)
                    score += int(killed ** 1.1 * (main_sf.get_width() + main_sf.get_height()) * math.sqrt(phase))
                    knife_remaining -= 1
                    if knife_remaining == 0 or ball_manager.ball_num == 0:
                        score += int(knife_remaining * 10000 * math.sqrt(phase))
                        if ball_manager.ball_num == 0:
                            score += int(10000 * math.sqrt(phase))
                        transit_count = 1

            if transit_count > 0:
                if transit_count < 60:
                    x1 = main_sf.get_width() - transit_count ** 2
                    x2 = main_sf.get_width()
                else:
                    x1 = 0
                    x2 = main_sf.get_width() - (transit_count - 60) ** 2
                pg.draw.rect(main_sf, CREAM, [x1, 0, x2 - x1, main_sf.get_height()])

                if transit_count == 60:
                    phase += 1
                    knife_remaining = 3
                    ball_manager.clear()
                    match phase:
                        case 1:
                            ball_manager.add_ball(StableBall(100, 100))
                            ball_manager.add_ball(StableBall(200, 300))
                            ball_manager.add_ball(StableBall(245, 200))
                            ball_manager.add_ball(StableBall(400, 100))
                            ball_manager.add_ball(StableBall(500, 150))
                            ball_manager.add_ball(StableBall(450, 250))
                            ball_manager.add_ball(StableBall(500, 350))
                            ball_manager.add_ball(StableBall(30, 150))
                            ball_manager.add_ball(StableBall(250, 100))
                        case 2:
                            ball_manager.add_ball(StableBall(200, 300))
                            ball_manager.add_group(CircleGroup(5, (400, 200), 100, 1))
                            ball_manager.add_group(CircleGroup(3, (150, 150), 40, 4))
                        case 3:
                            ball_manager.add_group(PendulumGroup((300, 100), 150, 50, 1))
                            ball_manager.add_group(PendulumGroup((450, 70), 100, 50, 3))
                            ball_manager.add_group(PendulumGroup((150, 70), 100, 50, 3))
                            ball_manager.add_group(CircleGroup(4, (300, 250), 70, 1))
                            ball_manager.add_ball(StableBall(100, 300))
                            ball_manager.add_ball(StableBall(500, 300))
                        case 4:
                            ball_manager.add_group(CircleGroup2(6, (300, 200), 150, 2))
                            ball_manager.add_group(PendulumGroup((300, 50), 100, 70, 3))
                            ball_manager.add_group(PendulumGroup((300, 50), 150, 70, 2))
                            ball_manager.add_group(PendulumGroup((300, 50), 200, 70, 1))
                        case 5:
                            index = Index.RESULT
                # ----------------
        elif index == Index.RESULT:
            if main_sf.get_width() != DEFAULT_WIDTH or main_sf.get_height() != DEFAULT_HEIGHT:
                sc = pg.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT + 50), pg.RESIZABLE)
                main_sf = pg.Surface((DEFAULT_WIDTH, DEFAULT_HEIGHT), pg.SRCALPHA)
            main_sf.fill(CREAM)

            txt1 = ft_exlarge.render(f"GAME CLEAR!", True, BG)
            txt2 = ft_large.render(f"Your Score is... {score}", True, BG)
            if best_score < score:
                txt3 = ft_large.render(f"Best Score Updated!!!", True, BG)
            else:
                txt3 = ft_large.render(f"Best Score... {best_score}", True, BG)

            main_sf.blit(txt1, ((main_sf.get_width() - txt1.get_width()) // 2, 100))
            main_sf.blit(txt2, ((main_sf.get_width() - txt2.get_width()) // 2, 200))
            main_sf.blit(txt3, ((main_sf.get_width() - txt3.get_width()) // 2, 250))

            if mouse_count == 1:
                index = Index.TUTORIAL
                if best_score < score:
                    best_score = score
                    with open(os.path.join(os.path.dirname(__file__), "best_score"), "w") as f:
                        f.write(str(best_score))

        # other
        effect_manager.update()
        effect_manager.draw(main_sf)
        ball_manager.update()
        ball_manager.draw(main_sf, tmr)

        sc.blit(main_sf, (0, 50))
        sc.blit(cursor_img, [m_x, m_y])
        pg.display.flip()
        cl.tick(60)


if __name__ == "__main__":
    pg.init()
    sc = pg.display.set_mode(clamp_size(DEFAULT_WIDTH, DEFAULT_HEIGHT + 50), pg.RESIZABLE)
    pg.display.set_caption("RESIZE")
    from images import *
    main()
