import os
import sys
import random
from time import sleep
import pygame as pg

WIDTH, HEIGHT = 1100, 650
MOVEMENT = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    check_bound関数
    引数：オブジェクトRect
    戻り値：（横軸のはみ出しbool判定, 縦軸のはみ出しbool判定）

    画面内なら1, 画面外なら0を返す
    """
    x, y = 1, 1
    if obj_rct.left < 0 or obj_rct.right > WIDTH:
        x = 0
    if obj_rct.top < 0 or obj_rct.bottom > HEIGHT:
        y = 0
        
    return (x, y)
       
        
def gameover_Event(screen: pg.Surface) -> None:
    event_screen = pg.Surface((WIDTH, HEIGHT)) 
    pg.draw.rect(event_screen, (0,0,0), (0,0,WIDTH,HEIGHT))
    event_screen.set_alpha(100)
    
    #テキスト
    fnt = pg.font.Font(None, 80)
    txt = fnt.render("GameOver", True, (255, 255, 255))
    txt_rec = txt.get_rect()
    txt_rec.center = WIDTH*0.5, HEIGHT*0.5
    event_screen.blit(txt, txt_rec) #描画
    
    #画像
    event_img = pg.transform.rotozoom(pg.image.load("fig/0.png"), 0, 0.9)
    img_rct = event_img.get_rect()
    img_rct.center = txt_rec.centerx * 1.4, txt_rec.centery
    event_screen.blit(event_img, img_rct) #描画
    img_rct.center = txt_rec.centerx * 0.6, txt_rec.centery
    event_screen.blit(event_img, img_rct) #描画
    
    #画面反映
    screen.blit(event_screen, [0,0])
    pg.display.update()
    sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    #爆弾の大きさ
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0,0,0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    
    #爆弾の加速度
    bb_accs = [a for a in range(1, 11)]

    return (bb_imgs, bb_accs)

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
    
    bb_imgs, bb_accs = init_bb_imgs()   
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            print("GameOver")
            gameover_Event(screen)
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
        
        #加速適応
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        
        bb_rct.move_ip(avx, avy)
        
        #時間により拡大・加速判定
        bb_img = bb_imgs[min(tmr//500, 9)]
        #Rect更新
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        
        pg.display.update()
        tmr += 1
        clock.tick(50)
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
