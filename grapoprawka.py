import pygame, sys, random, pygame.freetype, time
import os
from math import sqrt, sin, pi

screen_width = 1600
screen_height = 800
score_value = 0

# window center
os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (0, 30)

class Arrow(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def Draw(self):
        show_arrowimg(self.x, self.y)

class Food(object):
    def __init__(self):
        self.phase = random.uniform(0, 2 * pi)
        self.size = 30
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.x = random.randint(self.size, screen_width - self.size)
        self.y = random.randint(self.size, screen_height - self.size)
        self.eatten = False

    def Draw(self):
        if self.eatten:
            return
        z = t / 1000.0 * 2 * pi + self.phase
        n = 96
        q = ((sin(z) + 1) / 2.0 * (255 - n) + n)
        show_img(self.x - self.size/2 , self.y - self.size/2, q)
        #food = pygame.Rect(self.x - self.size/2, self.y - self.size/2, self.size, self.size)
        #pygame.draw.rect(screen, (self.color), food)

    def Eat(self):
        global score_value
        if not self.eatten:
            score_value += 1
        self.eatten = True

pygame.init()

foods = []
for i in range (0, 50):
    foods.append(Food())

screen = pygame.display.set_mode((screen_width, screen_height))

font = pygame.font.Font('freesansbold.ttf', 32)
foodimg = pygame.image.load('destroy.tga')
arrowimg = pygame.image.load('arrow.png')

textX = 10
textY = 10
fpsX = 1450
fpsY = 10


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_fps(x, y):
    showfps = font.render("FPS : " + str(fps), True, (255, 255, 255))
    screen.blit(showfps, (x, y))

def show_img(x, y, alpha):

    image = foodimg.copy()
    # this works on images with per pixel alpha too
    image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
    screen.blit(image, (x, y))

def show_arrowimg(x, y):
    screen.blit(arrowimg, (x, y))

clock = pygame.time.Clock()

arrow = Arrow(0, 0)

while True:
    show_arrowimg(arrow.x, arrow.y)
    t = pygame.time.get_ticks()
    show_score(textX, textY)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit(0)
    t2 = clock.tick()/1000.0
    v = 100
    s = v * t2
    fps = round(1/t2)
    show_fps(fpsX, fpsY)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        arrow.x += s
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        arrow.x -= s
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        arrow.y -= s
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        arrow.y += s

    #drawing

    for food in foods:
        food.Draw()

    for food in foods:
        if sqrt((arrow.x + 25 - food.x)*(arrow.x + 25 - food.x)+(arrow.y + 25 - food.y)*(arrow.y + 25 - food.y)) < 35:
            food.Eat()

    pygame.display.flip()
    screen.fill((0, 0, 0))
