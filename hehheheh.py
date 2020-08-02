'''Pygame is our game engine'''
import math
import random
import pygame
from pygame import mixer

pygame.init()


screen = pygame.display.set_mode((800, 600))


#Title and Icon
pygame.display.set_caption("Leo Attacker")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#background
background = pygame.image.load('background.jpg')

#background music
mixer.music.load('backgroundm.mp3')
mixer.music.play(-1)



#create the PLayer
playerImg = pygame.image.load('ship2.png')
PLAYERX = 365
PLAYERY = 500
PLAYERX_CHANGE = 0


#create the Monster
monsterImg = pygame.image.load('monster.png')
MONSTERX = []
MONSTERY = []
MONSTERX_CHANGE = []
MONSTERY_CHANGE = 60
j = 20
for i in range(j):
    MONSTERX.append(random.randint(50, 700))
    MONSTERY.append(random.randint(50, 150))
    MONSTERX_CHANGE.append(1)


#create the bullet
bulletImg = pygame.image.load('bullet.png')
BULLETX = 0
BULLETY = 0

def player(x_values, y_values):
    '''Draw the player'''
    screen.blit(playerImg, (x_values, y_values))


def monster(x_values, y_values):
    '''Draw the monster'''
    screen.blit(monsterImg, (x_values, y_values))


def bullet(x_values, y_values):
    '''Draw the bullet'''
    screen.blit(bulletImg, (x_values, y_values))


#gameover text
font2 = pygame.font.Font('freesansbold.ttf', 64)
def gameover_text():
    '''draw gameover'''
    gameovertext = font2.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gameovertext, (365, 250))


#score
SCORE_VALUE = 0
font = pygame.font.Font('freesansbold.ttf', 32)
TEXTX = 10
TEXTY = 10

def show_score(x_values, y_values):
    '''draw the score'''
    score = font.render("Score: " + str(SCORE_VALUE), True, (255, 255, 255))
    screen.blit(score, (x_values, y_values))


#check if right is press first
RIGHT = False


#game loop
RUNNING = True
BULLET = False
while RUNNING:
    #RGB
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    #game over
    for i in range(j):
        if MONSTERY[i] > 450:
            for k in range(j):
                MONSTERY[k] = 1000
            gameover_text()
            break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            PLAYERX = 365
            PLAYERY = 500
            PLAYERX_CHANGE = 0
            MONSTERX = []
            MONSTERY = []
            MONSTERX_CHANGE = []
            MONSTERY_CHANGE = 60
            j = 20
            for i in range(j):
                MONSTERX.append(random.randint(50, 700))
                MONSTERY.append(random.randint(50, 150))
                MONSTERX_CHANGE.append(1)
            BULLETX = 0
            BULLETY = 0
            SCORE_VALUE = 0
        if keys[pygame.K_z]:
            if not BULLET:
                BULLETX = PLAYERX + 16
                BULLETY = PLAYERY - 50
                BULLET = True
        if keys[pygame.K_LEFT]:
            PLAYERX_CHANGE = -2
            if not RIGHT:
                if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
                    PLAYERX_CHANGE = 2
        elif keys[pygame.K_RIGHT]:
            PLAYERX_CHANGE = 2
            RIGHT = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PLAYERX_CHANGE = 0
                RIGHT = False

    #boundaries
    PLAYERX += PLAYERX_CHANGE
    if PLAYERX > 750:
        PLAYERX = 700
    elif PLAYERX < 0:
        PLAYERX = 50


    for i in range(j):
        MONSTERX[i] += MONSTERX_CHANGE[i]
    for i in range(j):
        if MONSTERX[i] >= 700:
            MONSTERX[i] = 700
            MONSTERY[i] += MONSTERY_CHANGE
            MONSTERX_CHANGE[i] = MONSTERX_CHANGE[i] * -1
        elif MONSTERX[i] <= 50:
            MONSTERX[i] = 50
            MONSTERY[i] += MONSTERY_CHANGE
            MONSTERX_CHANGE[i] = MONSTERX_CHANGE[i] * -1

    #update location
    player(PLAYERX, PLAYERY)
    for i in range(j):
        monster(MONSTERX[i], MONSTERY[i])
    if BULLET:
        BULLETY -= 3
        bullet(BULLETX, BULLETY)
    if BULLETY == 0:
        BULLETY = 0
        BULLETX = 0
        BULLET = False

    for i in range(j):
        if math.sqrt(math.pow(BULLETX-MONSTERX[i], 2)+math.pow(BULLETY-MONSTERY[i], 2)) <= 27:
            killsound = mixer.Sound('killsound.wav')
            killsound.play()
            BULLET = False
            BULLETY = PLAYERY - 30
            SCORE_VALUE += 1
            MONSTERX[i] = random.randint(50, 700)
            MONSTERY[i] = random.randint(50, 150)

    show_score(TEXTX, TEXTY)
    pygame.display.update()
