# importing the necessary modules
import pygame
import os # ???
"""
The OS module in Python provides a way of using operating system dependent
functionality.
The functions that the OS module provides allows you to interface with the
underlying operating system that Python is running on - be that Windows, Mac or
Linux.
"""
import random # for spawning the egg at random 
# getting the font need in the game
pygame.font.init()

# defining the fixedd values
BLACK = (0,0,0) # colour for the WIRE
WIDTH,HEIGHT = 1280,800 # size of the window
BWIDTH,BHEIGHT = 150,107 # size of the basket
EWIDTH,EHEIGHT = 30,38 # size of egg
CWIDTH,CHEIGHT = 88,125 # size of chiken
FPS = 60 # setting fps to reduce hardware overload
BTVEL = 19 # speed of basket

# creating event for the drop and catch moment
EGG_CATCH = pygame.USEREVENT+1
EGG_DROP = pygame.USEREVENT+2

# printing EGGBASS on the game window
EGGBASS = pygame.display.set_caption("EGGBASS")
# the wire where chicken sit
WIRE = pygame.Rect(0, (10+CHEIGHT-5), WIDTH,7)
# defining the size of the game window

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
                                # pygame.RESIZABLE)
# trying to make a resizable window (Not working riight now)

# pygame. {resizng the image} - transform.scale( {???} - pygame.image.load({calling the path} - os.path.join( {the path} - "EGGBAS Assets","Background.png")), {l,b taken from the defined ones} (WIDTH,HEIGHT))
BG_IMG =pygame.transform.scale(pygame.image.load(os.path.join("EGGBAS Assets","Background.png")), (WIDTH,HEIGHT)) 
CHICKEN_IMG = pygame.transform.scale(pygame.image.load(os.path.join("EGGBAS Assets","Chicken.png")),(CWIDTH,CHEIGHT))
EGG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("EGGBAS Assets","Egg.png")), (EWIDTH,EHEIGHT))
BASKET_IMG = pygame.transform.scale(pygame.image.load(os.path.join("EGGBAS Assets","Basket.png")), (BWIDTH,BHEIGHT))
# we are using the comicsans font and 40 font size
LFONT = pygame.font.SysFont("comicsans", 40)
PFONT = pygame.font.SysFont("comicsans", 40)
EFONT =pygame.font.SysFont("comicans", 100)


def draw_window(basket,eggs,new_egg,lives,points):
    # bliting the background image at 0,0
    WIN.blit(BG_IMG, (0,0))
    # everytime a egg is created,we'll blit it on the screen
    for new_egg in eggs:
        WIN.blit(EGG_IMG, (new_egg.x,new_egg.y))

    pygame.draw.rect(WIN, BLACK, WIRE)
    # blitting chicken images  
    WIN.blit(CHICKEN_IMG, (10,10))
    WIN.blit(CHICKEN_IMG, (WIDTH-CWIDTH-10,10))
    WIN.blit(CHICKEN_IMG, (407,10))
    WIN.blit(CHICKEN_IMG, (804,10))
    #blitting the basket image
    WIN.blit(BASKET_IMG, (basket.x,basket.y))
    #creating lives text to be printed on screen 
    lives_text = LFONT.render("Lives = "+str(lives), 1, (0,255,0))
    #blitting the lives text
    WIN.blit(lives_text, (WIDTH-lives_text.get_width()-10,10))
    #creating points text to be printed on screen
    points_text = PFONT.render("Points ="+str(points), 1, (0,0,255))
    #blitting the points text
    WIN.blit(points_text, (0,10))
    # updating the window after all changes
    pygame.display.update()

#function for movement of basket
def basket_movement(keys_pressed,basket):
    if keys_pressed[pygame.K_LEFT] and basket.x-BTVEL>10:
        #whenever left key is pressed the basket will move towards left 
        basket.x-=BTVEL
    if keys_pressed[pygame.K_RIGHT] and basket.x + BWIDTH+BTVEL<WIDTH-10:
        #whenever right key is pressed the basket will move towards right 
        basket.x+=BTVEL


#function for checking if the egg is caught or dropped
def catchdrop(basket,eggs, EGG_CATCH, EGG_DROP,EVEL):
        for new_egg in eggs:
            new_egg.y+=(EVEL)
            if basket.colliderect(new_egg):
                #if the egg touches the basket, we will call the eggcatch function and remove that egg from eggs list
                pygame.event.post(pygame.event.Event(EGG_CATCH))
                eggs.remove(new_egg)
                
            if new_egg.y+EHEIGHT+EVEL>=basket.y+BHEIGHT/2:
                #if the egg doesn't touch the basket and passes the half of basket we will call the eggdrop  function and remove it from eggs list
                pygame.event.post(pygame.event.Event(EGG_DROP))
                eggs.remove(new_egg)

#function to display things when game is over
def end(ending,points):
    #creating text that will be displayed at the end
    end_text = EFONT.render(ending, 1, (255,0,0))
    #blitting the text
    WIN.blit(end_text, (WIDTH/2-end_text.get_width()/2,HEIGHT/2-end_text.get_height()/2))
    #creating score text
    score = PFONT.render("Score : "+str(points),1,(0,0,255))
    #blitting score text
    WIN.blit(score,(WIDTH/2-score.get_width()/2,HEIGHT/2-score.get_height()/2+end_text.get_height()+5) )
    #updating the changes on the window
    pygame.display.update()
    # adding delay so that the screen just doesn't flash
    pygame.time.delay(3000)


def main():
    #creating basket rectangle
    basket = pygame.Rect(WIDTH/2-BWIDTH/2,HEIGHT-BHEIGHT-10 , BWIDTH, BHEIGHT)
    
    clock = pygame.time.Clock()
    eggs = []
    
    #creating a list for x postition of the new eggs to be created
    neweggsx = [36,1216,433,830]
    
    neweggsy = 10 + CHEIGHT//2
    
    lives = 3
    points = 0
    EVEL = 6


    run = True
    while run:
        #setting frame rate
        clock.tick(FPS)

        for event  in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == EGG_CATCH:
                points+=10
            if event.type == EGG_DROP:
                lives -=1

        #whenever there is no egg in eggs list,creating an egg and adding it to the list
        if len(eggs)<1:
            new_egg = pygame.Rect(random.choice(neweggsx), neweggsy, EWIDTH, EHEIGHT)
            eggs.append(new_egg)
        
        #changing the speeds as per score
        if 100<= points <200:
            EVEL=7
            BTVEL = 20
        if 200 <= points < 300:
            EVEL = 8
            BTVEL = 21
        if 300 <= points < 400:
            EVEL = 9
            BTVEL = 22
        if 400 <= points <= 500:
            EVEL = 10
            BTVEL = 23
        if 500 <= points:
            EVEL = 11
            BTVEL = 24

        ending = " "
        if lives <=0:
            ending = "GAME OVER :("
            run = False
        if ending!=" ":
            end(ending,points)      

        keys_pressed = pygame.key.get_pressed()
        basket_movement(keys_pressed,basket) 
        catchdrop(basket, eggs, EGG_CATCH, EGG_DROP,EVEL)        
        draw_window(basket,eggs,new_egg,lives,points)
    main()

if __name__ == "__main__":
    main()