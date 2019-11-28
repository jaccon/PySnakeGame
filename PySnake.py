#!/usr/bin/env python
# Developed by @Jaccon
# http://github.com/jaccon

import pygame
import sys
import time
import random
from pygame.locals import *

# Controller Settings
pygame.init() 
pygame.joystick.init()

try:
	j = pygame.joystick.Joystick(0) # create a joystick instance
	j.init() # init instance
	print ("Enabled joystick: {0}".format(j.get_name()))
except pygame.error:
	print ("no joystick found.")

controller = pygame.JOYAXISMOTION
left = j.get_axis(0)
right = j.get_axis(0)
up = j.get_axis(1)
down = j.get_axis(1)
# Controller Settings

pygame.display.set_caption('Hard Snake')
fpsClock=pygame.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GAME_BACKGROUND = (64, 18, 139)
APPLE_COLOR = (255,0,0)
SNAKE_COLOR = (255,255,255)
FPS = 30
FONT_SIZE = 15
SCORE_COLOR = (255, 255, 255)
GAME_SOUNDTRACK = "assets/snake.mp3"

pygame.mixer.init()
pygame.mixer.music.load(GAME_SOUNDTRACK)
pygame.mixer.music.play()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((64, 18, 139))
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 40)

GRIDSIZE=20
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
        self.color = (SNAKE_COLOR)

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
        self.color = (APPLE_COLOR)
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

        block_size = 20
        lead_x_change = 0
        lead_y_change = 0

        for event in pygame.event.get():
            
            if event.type == QUIT:
                print('goodbye')
                pygame.quit()
                sys.exit()
                 
            elif event.type == pygame.JOYAXISMOTION:
                if j.get_axis(1) <= -1:
                    snake.point(UP)
                elif j.get_axis(1) >= 0.5:
                    snake.point(DOWN)
                elif j.get_axis(0) <= -1:
                    snake.point(LEFT)
                elif j.get_axis(0) >= 0.5:
                    snake.point(RIGHT)

        surface.fill((GAME_BACKGROUND))
        snake.move()
        check_eat(snake, apple)
        snake.draw(surface)
        apple.draw(surface)
        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render(" SCORE: " + str(snake.length), 1, (SCORE_COLOR))
        textpos = text.get_rect()
        textpos.centerx = 50
        surface.blit(text, textpos)
        screen.blit(surface, (10,10))

        pygame.display.flip()
        pygame.display.update()
        fpsClock.tick(FPS + snake.length/3)