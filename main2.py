import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((1000,750))

background = pygame.image.load('back1.jpg')

pygame.display.set_caption("Tanuj's Space")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)                      

# Player
playerImg = pygame.image.load('001.png')
playerX = 370
playerY = 680
playerX_change = 0

# Enemies
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('retro.png'))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.7)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet1.png')
bulletX = 0
bulletY = 680
bulletY_change = 10
bullet_state = "ready"

##score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)

textX=10
textY=10

##game over text
over_font=pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score=font.render("Score: " + str(score_value),True,(0,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text=over_font.render("GAME OVER",True,(78,78,255))
    screen.blit(over_text, (300,380))

def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16, y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((enemyX - bulletX)**2 + (enemyY - bulletY)**2)
    return distance < 27

running = True
while running:

    screen.fill((255,255,255))
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                playerX_change = 0

    # Player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 936:
        playerX = 936

    # Enemy movement (FIXED INDENTATION)
    for i in range(num_of_enemies):

        ##Game over
        if enemyY[i]>300:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break    

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.7
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 936:
            enemyX_change[i] = -0.7
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 680
            bullet_state = "ready" 
            score_value+= 1
           
            enemyX[i] = random.randint(0,800)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i], i)   # FIXED ARGUMENTS

    # Bullet movement
    if bulletY <= 0:
        bulletY = 680
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
                                            