import os
import sys
import random
import pygame as pg

WIDTH, HEIGHT = 1100, 650
MOVEMENT = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

"""
check_bound関数
引数：オブジェクトRect
戻り値：（横軸のはみ出しbool判定, 縦軸のはみ出しbool判定）

画面内なら1, 画面外なら0を返す
"""
def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    x, y = 1, 1
    if obj_rct.left < 0 or obj_rct.right > WIDTH:
        x = 0
    if obj_rct.top < 0 or obj_rct.bottom > HEIGHT:
        y = 0
        
    return (x, y)
       
        

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    #背景
    bg_img = pg.image.load("fig/pg_bg.jpg")    

    #こうかとん
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    #爆弾
    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0,0,0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx,  vy = 5, 5
    
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        
        #こうかとん
        sum_mv = [0, 0]
        for key, mv in MOVEMENT.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        #爆弾
        screen.blit(bb_img, bb_rct)
        jdg = check_bound(bb_rct)
        if jdg != (True, True):
            if not jdg[0]:
                vx *= -1
            if not jdg[1]:
                vy *= -1
        bb_rct.move_ip(vx, vy)
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
