import pygame
import random
import math
from pygame import mixer

# initializing  mode
pygame.init()
clock = pygame.time.Clock()
# screen creation
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('space.png')

# background music
mixer.music.load('background.wav')
mixer.music.play(-1)
# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerXChange = 0
playerYChange = 0

# enemy
numOfEnemies = 6
enemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))  # position of enemy should appear  random
    enemyY.append(random.randint(50, 150))  # position of enemy should appear random
    enemyXChange.append(4)
    enemyYChange.append(40)

# Bullet
# ready - you cant't see the bullet
# fire -  you can see the bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0  # 0, because we want the bullet to move with the spaceship
bulletY = 480  # 480, because our spaceship is at 480 pixel
bulletXChange = 0
bulletYChange = 10
bulletState = "ready"

# Scoring part
scoreVal = 0
font = pygame.font.Font('freesansbold.ttf', 32)  # 32 is size of the text
textX = 10
textY = 10

overFont = pygame.font.Font('freesansbold.ttf', 64)


def gameOverText():
    overText = overFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overText, (240, 250))


def showScore(x, y):
    score = font.render("Score : " + str(scoreVal), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):  # a function
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance <= 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))  # to set the background color R G B
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChange -= 5
            if event.key == pygame.K_RIGHT:
                playerXChange += 5
            if event.key == pygame.K_SPACE:
                if bulletState is "ready":
                    bulletSound = mixer.Sound('laser.wav')
                    bulletSound.play()
                    bulletX = playerX  # gets the current x coordinate of the spaceship as it  reloads
                    fireBullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0
    # Player Movement
    playerX += playerXChange
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 736 because size of spaceship is 64X64 so,800-64=736
        playerX = 736

    # enemy movement,multiple enemies
    for i in range(numOfEnemies):
        # Game Over condition
        if enemyY[i] > 440:
            gameoversound=mixer.Sound('gameover.wav')
            gameoversound.play()
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            gameOverText()
            break
        enemyX[i] += enemyXChange[i]
        if enemyX[i] <= 0:
            enemyXChange[i] = 4
            enemyY[i] += enemyYChange[i]
        elif enemyX[i] >= 736:  # 736 because size of spaceship is 64X64 so,800-64=736
            enemyXChange[i] = -4
            enemyY[i] += enemyYChange[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collisionSound = mixer.Sound('collision.wav')
            collisionSound.play()
            bulletY = 480  # reset the bullet to the spaceship
            bulletState = "ready"  # reset the state of the bullet for another chance
            scoreVal += 1
            enemyX[i] = random.randint(0, 735)  # so that the enemy respawns at a random position after being hit
            enemyY[i] = random.randint(50, 150)  # so that the enemy respawns at a random position after being hit
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    # to shoot multiple bullets
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"
    if bulletState is "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletYChange
    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
