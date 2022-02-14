import pygame
import os
import random

BLACK = (0,0,0)
WIDTH,HEIGHT = 1280,800
BWIDTH,BHEIGHT = 150,107
EWIDTH,EHEIGHT = 30,38 
CWIDTH,CHEIGHT = 88,125
FPS = 60
BTVEL = 18
EVEL = 6

EGG_CATCH = pygame.USEREVENT+1
EGG_DROP = pygame.USEREVENT+2

ROD = pygame.Rect(0, (10+CHEIGHT-5), WIDTH,7)
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
BG_IMG =pygame.transform.scale(pygame.image.load(os.path.join("EGGBAS Assets","Background.png")), (WIDTH,HEIGHT)) 
CHICKEN_IMG = pygame.transform.scale(pygame.image.load(os.path.join("EGGBAS Assets","Chicken.png")),(CWIDTH,CHEIGHT)) 
EGG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("EGGBAS Assets","Egg.png")), (EWIDTH,EHEIGHT))
BASKET_IMG = pygame.transform.scale(pygame.image.load(os.path.join("EGGBAS Assets","Basket.png")), (BWIDTH,BHEIGHT))

def draw_window(basket,eggs,new_egg,lives,points):
    WIN.blit(BG_IMG, (0,0))
    for new_egg in eggs:
        WIN.blit(EGG_IMG, (new_egg.x,new_egg.y))
    pygame.draw.rect(WIN, BLACK, ROD)
    WIN.blit(CHICKEN_IMG, (10,10))
    WIN.blit(CHICKEN_IMG, (WIDTH-CWIDTH-10,10))
    WIN.blit(CHICKEN_IMG, (407,10))
    WIN.blit(CHICKEN_IMG, (804,10))
    WIN.blit(BASKET_IMG, (basket.x,basket.y))
    pygame.display.update()

def basketm(keys_pressed,basket):
    if keys_pressed[pygame.K_LEFT] and basket.x-BTVEL>10:
        basket.x-=BTVEL
    if keys_pressed[pygame.K_RIGHT] and basket.x + BWIDTH+BTVEL<WIDTH-10:
        basket.x+=BTVEL

def catchdrop(basket, new_egg, eggs, EGG_CATCH, EGG_DROP,EVEL):
        for new_egg in eggs:
            new_egg.y+=(EVEL)
            if basket.colliderect(new_egg):
                pygame.event.post(pygame.event.Event(EGG_CATCH))
                eggs.remove(new_egg)

            if new_egg.y+EVEL+EHEIGHT>=basket.y+BHEIGHT/2:
                pygame.event.post(pygame.event.Event(EGG_DROP))

                eggs.remove(new_egg)

def main():
    basket = pygame.Rect(WIDTH/2-BWIDTH/2,HEIGHT-BHEIGHT-10 , BWIDTH, BHEIGHT)
    clock = pygame.time.Clock()
    eggs = []
    neweggsx = [36,1216,433,830]
    neweggsy = 10 + CHEIGHT//2
    new_egg = pygame.Rect(random.choice(neweggsx), 72, EWIDTH, EHEIGHT)
    lives = 3
    points = 0
    run = True
    
    while run:
        clock.tick(FPS)
        for event  in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False    
            if event.type == EGG_CATCH:
                points+=10
                print("Your points: ",points)
            if event.type == EGG_DROP:
                lives -=1
                print("Lives left: ",lives)

        if len(eggs)<1:
            new_egg = pygame.Rect(random.choice(neweggsx), 72, EWIDTH, EHEIGHT)
            eggs.append(new_egg)

        if lives <=0:
            print("Game Over")
            run = False

        keys_pressed = pygame.key.get_pressed()
        basketm(keys_pressed,basket) 
        catchdrop(basket, new_egg, eggs, EGG_CATCH, EGG_DROP,EVEL)        
        draw_window(basket,eggs,new_egg,lives,points)
    pygame.quit()


if __name__ == "__main__":
    main()
