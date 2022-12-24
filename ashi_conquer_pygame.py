import pygame
import math
import random
from pygame import mixer

# initialize pygame 
pygame.init()

# creating a window
screen = pygame.display.set_mode((1001, 1001))

#bgimg
background = pygame.image.load('14658088_5509862.png')

#bgsnd
mixer.music.load('space_music.wav')
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# changing title, icon
pygame.display.set_caption("Ashi Conquer")
icon = pygame.image.load('world.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('spaceship.png')
playerX = 468
playerY = 926
playerX_change = 0
playerY_change = 0

def player(x,y):
    screen.blit(playerImg, (x, y))
    
# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_count = 10

for i in range(enemy_count):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(64, 937))
    enemyY.append(random.randint(64, 300))
    enemyX_change.append(1)
    enemyY_change.append(0.1)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = playerX
bulletY = playerY
bulletY_change = 5
bullet_state = "ready"

# warning
warnImg = pygame.image.load('warning.png')
warnX = 468
warnY = 150

# asteroides
rockImg = []
rockX = []
rockY = []
rockY_change = []
rock_count = 21

for i in range(rock_count):
    rockImg.append(pygame.image.load('asteroid.png'))
    rockX.append(random.randint(128, 873))
    rockY.append(-100)
    rockY_change.append(-5)

def rock(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def warning_sign(x, y):
    screen.blit(warnImg, (x, y))
    
warn_txt = pygame.font.Font('freesansbold.ttf', 16)

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

fired_bullets = 0
bu_fnt = pygame.font.Font('freesansbold.ttf', 16)

textX1 = 10
textY1 = 50

accuracy = pygame.font.Font('freesansbold.ttf', 32)

# KOtxt
KOfnt = pygame.font.Font('freesansbold.ttf', 106)

def accuracy_per():
    accuracy_txt = accuracy.render("Accuracy: " + str(score_value / fired_bullets) + "%", True, (163, 255, 231))
    screen.blit(accuracy_txt, (0, 360))

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (163, 255, 231))
    screen.blit(score, (x, y))

def game_over_txt():
    KO = KOfnt.render("GAME OVER! mleM", True, (163, 255, 231))
    screen.blit(KO, (0, 250.25))

def warntxt():
    wrn = warn_txt.render("ENEMY IN PLAYER TERITORRY AREA.", True, (163, 255, 231))
    screen.blit(wrn, (350, 214))

def f_bu(x, y):
    fibu = bu_fnt.render("Bullets fired: " + str(fired_bullets), True, (163, 255, 231))
    screen.blit(fibu, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
    
# an event/game loop to keep window running until asked to stop
running = True
while running:
    # screen bgimg
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bullet_state == ""

            running = False
    
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -1
            if event.key == pygame.K_d:
                playerX_change = 1
            if event.key == pygame.K_w:
                playerY_change = -1
            if event.key == pygame.K_s:
                playerY_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    b_fire = mixer.Sound('fire.wav')
                    b_fire.set_volume(0.75)
                    b_fire.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    fired_bullets += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w or event.key == pygame.K_s:
                playerX_change = 0
                playerY_change = 0
    
    # boundaries for sprites and movements
    playerX += playerX_change
    playerY += playerY_change
    
    if playerX < 0:
        playerX = 0
    elif playerX > 937:
        playerX = 937
    elif playerY < 701:
        playerY = 701
    elif playerY > 926:
        playerY = 926
    elif playerX > 937 and playerY > 926:
        playerX = 920
        playerY = 910
    elif playerX > 937 and playerY < 701:
        playerX = 920
        playerY = 690
    elif playerX < 0 and playerY > 926:
        playerX = 10
        playerY = 910
    elif playerX < 0 and playerY < 701:
        playerX = 10
        playerY = 690
    
    for i in range (enemy_count):
        
        # KO
        if enemyY[i] > playerY:
            for j in range(enemy_count):
                enemyY[j] = 2147483647
                bullet_state=""
            for i in range(rock_count):
                rockY_change = -1
                rockY = 2147483647
            game_over_txt()
            accuracy_per()
            
            break
        
        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] += 0.25
        elif enemyX[i] >= 951:
            enemyX_change[i] -= 0.25
        elif enemyY[i] <= 64:
            enemyY_change[i] += 0.025
        elif enemyY[i] >= 701:
            warn = mixer.Sound('warn.wav')
            warn.set_volume(0.1)
            warn.play()
            warning_sign(warnX, warnY)
            warntxt()
        
    for i in range (rock_count):
        rockY[i] += rockY_change[i]
        if rockY[i] >= 1200:
            rockY[i] == -100

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision and bullet_state == "fire":
            b_boom = mixer.Sound('boom.wav')
            b_boom.set_volume(1.0)
            b_boom.play()
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(64, 937)
            enemyY[i] = random.randint(64, 300)
            
        # print the enemies
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    if bulletY <= 64:
        bulletY = playerY
        bullet_state = "ready"
        

        
    # print the player
    player(playerX, playerY)
    
    # print score
    show_score(textX, textY)
    
    # show bullets fired
    f_bu(textX1, textY1)
    
    # update changes added to the loop
    pygame.display.update()
