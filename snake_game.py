#
# 贪吃蛇游戏：Snake.py
#
# 重点在于记录蛇的运行轨迹！采用列表，每移动一次，添加蛇头当前位置，弹出末尾处元素。只有吃了树莓才不弹出，蛇的长度增加！

import pygame
import sys
import time
import random
from pygame.locals import *

# 初始化
WIDTH = 200
HEIGHT = 300
CELLSIZE = 20

pygame.init()
fpsClock = pygame.time.Clock()
playSurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Go!')
#image = pygame.image.load('game.ico')
#pygame.display.set_icon(image)

# 定义颜色变量
redColor = pygame.Color(255, 0, 0)
blackColor = pygame.Color(0, 0, 0)
whiteColor = pygame.Color(255, 255, 255)
greyColor = pygame.Color(150, 150, 150)
LightColor = pygame.Color(220, 220, 220)

def gameOver(playSurface, score):
    gameOverFont = pygame.font.Font('freesansbold.ttf', 30)
    gameOverSurf = gameOverFont.render('Game Over', True, greyColor)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (int(WIDTH/2), int(HEIGHT/2))
    playSurface.blit(gameOverSurf, gameOverRect)

    scoreFont = pygame.font.Font('freesansbold.ttf', 20)
    scoreSurf = scoreFont.render('SCORE: ' + str(score), True, greyColor)
    scoreRect = scoreSurf.get_rect()
    scoreRect.midtop = (int(WIDTH/2), int(HEIGHT/4))
    playSurface.blit(scoreSurf, scoreRect)
    pygame.display.flip()

    time.sleep(3)
    pygame.quit()
    sys.exit()

def SetBerryPosition():
    x = random.randrange(1, WIDTH / CELLSIZE)
    y = random.randrange(1, HEIGHT / CELLSIZE)
    return [int(x * CELLSIZE), int(y * CELLSIZE)]

# 定义初始位置
snakePosition = [100, 100]
snakeSegments = [[100, 100], [80, 100], [60, 100]]
raspberryPosition = SetBerryPosition()
raspberrySpawned = 1
direction = 'right'
changeDirection = direction
score = 0

while True:
    # 键盘判断蛇的运动：
    for event in pygame.event.get():
        #print(event.type)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == ord('d'):
                changeDirection = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                changeDirection = 'left'
            if event.key == K_UP or event.key == ord('w'):
                changeDirection = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                changeDirection = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    # 不能反向运动：符合条件才能改变方向，否则方向不变继续前进
    if changeDirection == 'right' and not direction == 'left':
        direction = changeDirection
    if changeDirection == 'left' and not direction == 'right':
        direction = changeDirection
    if changeDirection == 'up' and not direction == 'down':
        direction = changeDirection
    if changeDirection == 'down' and not direction == 'up':
        direction = changeDirection

    # 转弯操作：
    if direction == 'right':
        snakePosition[0] += 20
    if direction == 'left':
        snakePosition[0] -= 20
    if direction == 'up':
        snakePosition[1] -= 20
    if direction == 'down':
        snakePosition[1] += 20

    # 加入蛇头当前位置
    #print(snakePosition, snakeSegments)
    snakeSegments.insert(0, list(snakePosition))

    # 判断是否吃到树莓：
    if snakePosition[0] == raspberryPosition[0] and snakePosition[1] == raspberryPosition[1]:
        raspberrySpawned = 0
    else:
        # 没有吃到树莓，则继续移动snake，弹出尾部，前面已加入当前头部到snakeSegment：
        snakeSegments.pop()

    # 重新生成树莓：
    if raspberrySpawned == 0:
        raspberryPosition = SetBerryPosition()
        raspberrySpawned = 1
        score += 1

    # 刷新显示：
    playSurface.fill(blackColor)
    for position in snakeSegments[1:]:
        # 显示蛇：
        pygame.draw.rect(playSurface, whiteColor, Rect(position[0], position[1], CELLSIZE, CELLSIZE))
    # 显示蛇头：
    pygame.draw.rect(playSurface, LightColor, Rect(snakePosition[0], snakePosition[1], CELLSIZE, CELLSIZE))
    # 显示树莓：
    pygame.draw.rect(playSurface, redColor, Rect(raspberryPosition[0], raspberryPosition[1], CELLSIZE, CELLSIZE))
    pygame.display.flip()

    # 判断是否死亡：
    if snakePosition[0] > WIDTH-CELLSIZE or snakePosition[0] < 0:
        gameOver(playSurface, score)
    if snakePosition[1] > HEIGHT-CELLSIZE or snakePosition[1] < 0:
        gameOver(playSurface, score)
    # 蛇头和自身交叉也死亡！
    for snakeBody in snakeSegments[1:]:
        if snakePosition[0] == snakeBody[0] and snakePosition[1] == snakeBody[1]:
            gameOver(playSurface, score)

    # 控制游戏速度：
    if len(snakeSegments) < 40:
        speed = 2 + len(snakeSegments) // 4
    else:
        speed = 16

    fpsClock.tick(speed)

'''

#!/usr/bin/python
# -*- coding: UTF-8 -*-
#作者：黄哥
#链接：https://www.zhihu.com/question/55873159/answer/146647646
#来源：知乎
#著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

import random
import pygame
import sys
from pygame.locals import *

Snakespeed = 3
Window_Width = 200
Window_Height = 300
Cell_Size = 20  # Width and height of the cells
# Ensuring that the cells fit perfectly in the window. eg if cell size was
# 10 and window width or windowheight were 15 only 1.5 cells would fit.
assert Window_Width % Cell_Size == 0, "Window width must be a multiple of cell size."
# Ensuring that only whole integer number of cells fit perfectly in the window.
assert Window_Height % Cell_Size == 0, "Window height must be a multiple of cell size."
Cell_W = int(Window_Width / Cell_Size)  # Cell Width
Cell_H = int(Window_Height / Cell_Size)  # Cellc Height

White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)  # Defining element colors for the program.
Green = (0, 255, 0)
DARKGreen = (0, 155, 0)
DARKGRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
Red_DARK = (150, 0, 0)
BLUE = (0, 0, 255)
BLUE_DARK = (0, 0, 150)

BGCOLOR = Black  # Background color

UP = 'up'
DOWN = 'down'      # Defining keyboard keys.
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  # Syntactic sugar: index of the snake's head

def main():
    global SnakespeedCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    SnakespeedCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((Window_Width, Window_Height))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake Go')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

def runGame():
    # Set a random start point.
    startx = random.randint(3, Cell_W - 5)
    starty = random.randint(3, Cell_H - 5)
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the Snake has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == Cell_W or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == Cell_H:
            return  # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return  # game over

        # check if Snake has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation()  # set a new apple somewhere
        else:
            del wormCoords[-1]  # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'],
                       'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'],
                       'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD][
                'x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD][
                'x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        SnakespeedCLOCK.tick(Snakespeed)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, White)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (Window_Width - 200, Window_Height - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 50)
    titleSurf1 = titleFont.render('Snake!', True, White, DARKGreen)
    degrees1 = 0
    #degrees2 = 0

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (Window_Width / 2, Window_Height / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return

        pygame.display.update()
        SnakespeedCLOCK.tick(Snakespeed)
        degrees1 += 3  # rotate by 3 degrees each frame
        #degrees2 += 7  # rotate by 7 degrees each frame ?

def terminate():
    pygame.quit()
    sys.exit()

def getRandomLocation():
    return {'x': random.randint(0, Cell_W - 1), 'y': random.randint(0, Cell_H - 1)}

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 50)
    gameSurf = gameOverFont.render('Game', True, White)
    overSurf = gameOverFont.render('Over', True, White)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (Window_Width / 2, 10)
    overRect.midtop = (Window_Width / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, White)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (Window_Width - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * Cell_Size
        y = coord['y'] * Cell_Size
        wormSegmentRect = pygame.Rect(x, y, Cell_Size, Cell_Size)
        pygame.draw.rect(DISPLAYSURF, DARKGreen, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(
            x + 4, y + 4, Cell_Size - 8, Cell_Size - 8)
        pygame.draw.rect(DISPLAYSURF, Green, wormInnerSegmentRect)

def drawApple(coord):
    x = coord['x'] * Cell_Size
    y = coord['y'] * Cell_Size
    appleRect = pygame.Rect(x, y, Cell_Size, Cell_Size)
    pygame.draw.rect(DISPLAYSURF, Red, appleRect)

def drawGrid():
    for x in range(0, Window_Width, Cell_Size):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, Window_Height))
    for y in range(0, Window_Height, Cell_Size):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (Window_Width, y))

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
'''