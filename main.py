# pygameのウェルカムメッセージを無効化
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as pg

import math
import numpy as np
import sys
from enum import Enum, auto

from consts import *
import util
import effect as ef
from component import StableBall, CircleGroup, BallManager, MovingCircleGroup, PendulumGroup

class Index(Enum):
    TITLE = auto()
    GAME = auto()
    RESULT = auto()


def clamp_size(w, h):
    return (
        max(MIN_WIDTH, min(MAX_WIDTH, w)),
        max(MIN_HEIGHT + 50, min(MAX_HEIGHT + 50, h)),
    )


def main():
    global sc
    main_sf = pg.Surface((DEFAULT_WIDTH, DEFAULT_HEIGHT), pg.SRCALPHA)
    cl = pg.time.Clock()
    tmr = 0
    mouse_count = 0
    pg.mouse.set_visible(False)
    ft_path = os.path.join(PATH, "resources", "nicomoji-plus_v2-5.ttf")
    ft = pg.font.Font(ft_path, 25)
    ft_large = pg.font.Font(ft_path, 30)
    ft_exlarge = pg.font.Font(ft_path, 60)
    ft_title = pg.font.Font(ft_path, 90)
    index = Index.TITLE

    score: int = 0
    phase: int = 0
    knife_remaining: int = 3
    ball_manager = BallManager()
    effect_manager = ef.EffectManager()
    start_pos: tuple[int, int] = (0, 0)
    end_pos: tuple[int, int] = (0, 0)
    transit_count: int = 1

    with open(os.path.join(PATH, "best_score"), "r") as f:
        try:
            best_score = int(f.read())
        except ValueError:
            print("Best Score must be an integer.")
            best_score = 0

    while True:
        tmr += 1
        mouse_up = False
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif e.type == pg.VIDEORESIZE:
                if transit_count > 0 or index != Index.GAME:  # ゲームプレイ時のみリサイズを許可
                    sc = pg.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pg.RESIZABLE)
                    main_sf = pg.Surface((DEFAULT_WIDTH, DEFAULT_HEIGHT - 50), pg.SRCALPHA)
                else:
                    sc = pg.display.set_mode(clamp_size(e.w, e.h), pg.RESIZABLE)
                    main_sf = pg.Surface((sc.get_width(), sc.get_height() - 50), pg.SRCALPHA)
            # elif e.type == pg.MOUSEBUTTONDOWN:  # デバッグ用
            #     if pg.key.get_pressed()[pg.K_LSHIFT]:
            #         print(pg.mouse.get_pos())
            elif e.type == pg.MOUSEBUTTONUP and e.button == 1:
                mouse_up = True
        if pg.mouse.get_pressed()[0]:
            mouse_count += 1
        else:
            mouse_count = 0
        m_x, m_y = pg.mouse.get_pos()
        sc.fill(CREAM)
        main_sf.fill(BG)

        if index == Index.TITLE:
            main_sf.fill(CREAM)

            # 文字の描画
            title_txt = ft_title.render(f"「RESIZE」", True, BG)
            main_sf.blit(title_txt, ((DEFAULT_WIDTH - title_txt.get_width()) // 2, 50))
            txt1 = ft_large.render("Click Mouse to Start", True, BG)
            txt2 = ft_large.render(f"Best Score: {best_score}", True, BG)
            main_sf.blit(txt1, ((DEFAULT_WIDTH - txt1.get_width()) // 2, 200))
            main_sf.blit(txt2, ((DEFAULT_WIDTH - txt2.get_width()) // 2, 250))

            if mouse_count == 1:
                # 画面遷移
                phase = 0
                transit_count = 59
                index = Index.GAME

        elif index == Index.GAME:
            if transit_count > 0:
                transit_count += 1
            if transit_count > 100:
                transit_count = 0

            # ステータスバー(？)の描画
            util.draw.ball(sc, BG, (25, 25), 0)
            ball_txt = ft.render(f": {ball_manager.ball_num}/9", True, BG)
            sc.blit(ball_txt, (50, 10))

            sc.blit(restart_img, (145, 5))
            if mouse_count == 1:
                if 145 <= m_x <= 145 + restart_img.get_width() and 5 <= m_y < 5 + restart_img.get_height():
                    # タイトルに戻る
                    index = Index.TITLE
                    ball_manager.clear()
                    score = 0
                    sc = pg.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pg.RESIZABLE)
                    main_sf = pg.Surface((DEFAULT_WIDTH, DEFAULT_HEIGHT - 50), pg.SRCALPHA)
                    pg.display.set_caption("RESIZE")
                    continue

            if main_sf.get_width() > 530:
                score_txt = ft.render(f"score: {str(score).zfill(6)}", True, BG)
                sc.blit(score_txt, (190, 10))
            pg.display.set_caption(f"Phase: {phase}/4, Score: {str(score).zfill(6)}")
            for i in range(knife_remaining):
                sc.blit(knife_img, [main_sf.get_width() - 50 - i * 30, 5])
            # ----------------

            # ウィンドウの幅、高さの描画
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
            util.draw.arrow(main_sf, (5, h - 20), (w - 5, h - 20), CREAM)
            main_sf.blit(txt_w, ((w - txt_w.get_width()) // 2, h - 30 - txt_w.get_height()))

            txt_h = ft.render(str(h), True, h_color)
            util.draw.arrow(main_sf, (w - 20, 5), (w - 20, h - 5), CREAM)
            main_sf.blit(txt_h, (w - 30 - txt_h.get_width(), (h - txt_h.get_height()) // 2))
            # ----------------

            # ゲームロジック
            if mouse_count == 1:
                start_pos = m_x, m_y - 50
            if mouse_count > 0:
                # 始点の描画
                pg.draw.line(main_sf, CREAM,
                             [start_pos[0], start_pos[1] - 10],
                             [start_pos[0], start_pos[1] + 10], 3)
                pg.draw.line(main_sf, CREAM,
                             [start_pos[0] - 10, start_pos[1]],
                             [start_pos[0] + 10, start_pos[1]], 3)

                # カーソルが始点と十分離れたなら軌跡予測を描画
                end_pos = m_x, m_y - 50
                if (start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2 > 2500:
                    dir_vec = np.array([start_pos[0] - end_pos[0], start_pos[1] - end_pos[1]], dtype=float)
                    dir_vec /= np.linalg.norm(dir_vec)
                    start_vec = np.array(start_pos)
                    util.draw.dashed_line(main_sf,
                                          start_vec - dir_vec * 1000, start_vec + dir_vec * 1000, CREAM, width=4)

            if transit_count == 0:  # 画面遷移中は無効
                if mouse_up and (start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2 > 2500:
                    # ナイフを飛ばす
                    dir_vec = np.array([start_pos[0] - end_pos[0], start_pos[1] - end_pos[1]], dtype=float)
                    dir_vec /= np.linalg.norm(dir_vec)
                    start_vec = np.array(start_pos)
                    effect_manager.add(ef.KnifeEffect(start_vec - dir_vec * 1000, start_vec + dir_vec * 1000))

                    killed = ball_manager.knife(start_vec, dir_vec, main_sf, effect_manager)
                    score += int((killed ** 1.2) * (main_sf.get_width() + main_sf.get_height()) * math.sqrt(phase))
                    knife_remaining -= 1
                    if knife_remaining == 0 or ball_manager.ball_num == 0:  # フェーズ終了
                        # ボーナススコア
                        if ball_manager.ball_num == 0:
                            score += int(10000 * math.sqrt(phase) * (1 + knife_remaining))
                        transit_count = 1  # 遷移開始

            if transit_count > 0:
                # 遷移のアニメーション
                if transit_count < 60:
                    x1 = main_sf.get_width() - transit_count ** 2
                    x2 = main_sf.get_width()
                else:
                    x1 = 0
                    x2 = main_sf.get_width() - (transit_count - 60) ** 2
                pg.draw.rect(main_sf, CREAM, [x1, 0, x2 - x1, main_sf.get_height()])

                # 次のフェーズに初期化
                if transit_count == 60:
                    phase += 1
                    knife_remaining = 3
                    ball_manager.clear()
                    match phase:  # いつか独自ファイルに分離したい
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
                            ball_manager.add_group(MovingCircleGroup(6, (300, 200), 150, 2))
                            ball_manager.add_group(PendulumGroup((300, 50), 100, 70, 3))
                            ball_manager.add_group(PendulumGroup((300, 50), 150, 70, 2))
                            ball_manager.add_group(PendulumGroup((300, 50), 200, 70, 1))
                        case 5:  # リザルトに移行
                            index = Index.RESULT
                            sc = pg.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pg.RESIZABLE)
                            main_sf = pg.Surface((DEFAULT_WIDTH, DEFAULT_HEIGHT - 50), pg.SRCALPHA)
            # ----------------

        elif index == Index.RESULT:
            main_sf.fill(CREAM)

            # テキストの描画
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
                # ベストスコア更新
                if best_score < score:
                    best_score = score
                    with open(os.path.join(PATH, "best_score"), "w") as f:
                        f.write(str(best_score))
                index = Index.TITLE
                score = 0
                pg.display.set_caption("RESIZE")

        # その他
        effect_manager.update()
        effect_manager.draw(main_sf)
        ball_manager.update()
        ball_manager.draw(main_sf, tmr)

        sc.blit(main_sf, (0, 50))
        sc.blit(cursor_img, [m_x, m_y])

        # if pg.key.get_pressed()[pg.K_TAB]:  # デバッグ用
        #     pg.image.save(sc, f"screenshot_{tmr}.png")

        pg.display.flip()
        cl.tick(60)


if __name__ == "__main__":
    pg.init()
    sc = pg.display.set_mode(clamp_size(DEFAULT_WIDTH, DEFAULT_HEIGHT + 50), pg.RESIZABLE)
    pg.display.set_caption("RESIZE")
    from images import *  # convert_alpha()のためにこの位置でインポート
    main()
