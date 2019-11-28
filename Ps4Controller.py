import pygame
import os

pygame.init()
pygame.joystick.init()

controller = pygame.joystick.Joystick(0)
controller.init()

axis = {}
button = {}
hat = {}

for i in range(controller.get_numaxes()):
	axis[i] = 0.0
for i in range(controller.get_numbuttons()):
	button[i] = False
for i in range(controller.get_numhats()):
	hat[i] = (0, 0)

AXIS_LEFT_STICK_X = 0
AXIS_LEFT_STICK_Y = 1
AXIS_RIGHT_STICK_X = 2
AXIS_RIGHT_STICK_Y = 3
AXIS_R2 = 4
AXIS_L2 = 5
BUTTON_SQUARE = 0
BUTTON_CROSS = 1
BUTTON_CIRCLE = 2
BUTTON_TRIANGLE = 3
BUTTON_L1 = 4
BUTTON_R1 = 5
BUTTON_L2 = 6
BUTTON_R2 = 7
BUTTON_SHARE = 8
BUTTON_OPTIONS = 9
BUTTON_LEFT_STICK = 10
BUTTON_RIGHT_STICK = 11
BUTTON_PS = 12
BUTTON_PAD = 13
HAT_1 = 0

quit = False
while quit == False:

    for event in pygame.event.get():

        if event.type == pygame.JOYAXISMOTION:
            axis[event.axis] = round(event.value,3)
        elif event.type == pygame.JOYBUTTONDOWN:
            button[event.button] = True
        elif event.type == pygame.JOYBUTTONUP:
            button[event.button] = False
        elif event.type == pygame.JOYHATMOTION:
        	hat[event.hat] = event.value

    quit = button[BUTTON_PS]

    os.system('cls')
    print "PS4 Python Controller"
    print "====================="
    print("Left stick X:", axis[AXIS_LEFT_STICK_X])
    print("Left stick Y:", axis[AXIS_LEFT_STICK_Y])
    print("Right stick X:", axis[AXIS_RIGHT_STICK_X])
    print("Right stick Y:", axis[AXIS_RIGHT_STICK_Y])
    print("L2 strength:", axis[AXIS_L2])
    print("R2 strength:", axis[AXIS_R2],"\n")
    print("Botao Quadrado:", button[BUTTON_SQUARE])
    print("Cross:", button[BUTTON_CROSS])
    print("Botao Bolinha:", button[BUTTON_CIRCLE])
    print("Button Trin:", button[BUTTON_TRIANGLE])
    print("L1:", button[BUTTON_L1])
    print("R1:", button[BUTTON_R1])
    print("L2:", button[BUTTON_L2])
    print("R2:", button[BUTTON_R2])
    print("Share:", button[BUTTON_SHARE])
    print("Options:", button[BUTTON_OPTIONS])
    print("Left stick press:", button[BUTTON_LEFT_STICK])
    print("Right stick press:", button[BUTTON_RIGHT_STICK])
    print("PS:", button[BUTTON_PS])
    print("Touch Pad:", button[BUTTON_PAD],"\n")
    print("Hat X:", hat[HAT_1][0])
    print("Hat Y:", hat[HAT_1][1],"\n")
    print("Aperte o botao PS para sair:", quit)
    clock = pygame.time.Clock()
    clock.tick(30)

    #!/usr/bin/env python

import pygame
import sys
import time
import random

from pygame.locals import *

FPS = 5
pygame.init()
fpsClock=pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((255,255,255))
clock = pygame.time.Clock()

pygame.key.set_repeat(1, 40)

GRIDSIZE=10
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)
    
screen.blit(surface, (0,0))

def draw_box(surf, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRIDSIZE, GRIDSIZE))
    pygame.draw.rect(surf, color, r)

class Snake(object):
    def __init__(self):
        self.lose()
        self.color = (0,0,0)

    def get_head_position(self):
        return self.positions[0]

    def lose(self):
        self.length = 1
        self.positions =  [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def point(self, pt):
        if self.length > 1 and (pt[0] * -1, pt[1] * -1) == self.direction:
            return
        else:
            self.direction = pt

    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = (((cur[0]+(x*GRIDSIZE)) % SCREEN_WIDTH), (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.lose()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
    
    def draw(self, surf):
        for p in self.positions:
            draw_box(surf, self.color, p)

class Apple(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (255,0,0)
        self.randomize()

    def randomize(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRIDSIZE, random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)

    def draw(self, surf):
        draw_box(surf, self.color, self.position)

def check_eat(snake, apple):
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize()

if __name__ == '__main__':
    snake = Snake()
    apple = Apple()
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    snake.point(UP)
                elif event.key == K_DOWN:
                    snake.point(DOWN)
                elif event.key == K_LEFT:
                    snake.point(LEFT)
                elif event.key == K_RIGHT:
                    snake.point(RIGHT)


        surface.fill((255,255,255))
        snake.move()
        check_eat(snake, apple)
        snake.draw(surface)
        apple.draw(surface)
        font = pygame.font.Font(None, 36)
        text = font.render(str(snake.length), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = 20
        surface.blit(text, textpos)
        screen.blit(surface, (0,0))

        pygame.display.flip()
        pygame.display.update()
        fpsClock.tick(FPS + snake.length/3)
