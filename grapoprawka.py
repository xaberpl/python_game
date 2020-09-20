import pygame, sys, random, pygame.freetype
import os
from math import sqrt, sin, pi

screen_width = 1600
screen_height = 800
score_value = 0

# window center
os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (0, 30)


class Food(object):
    def __init__(self):
        self.size = 30
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.x = random.randint(self.size, screen_width - self.size)
        self.y = random.randint(self.size, screen_height - self.size)

        self.eatten = False
    def Draw(self):
        if self.eatten:
            return

        food = pygame.Rect(self.x - self.size/2, self.y - self.size/2, self.size, self.size)
        pygame.draw.rect(screen, (self.color), food)

    def Eat(self):
        global score_value
        if not self.eatten:
            score_value += 1
        self.eatten = True



pygame.init()



foods = []
for i in range (0, 50):
    print(i)
    foods.append(Food())

screen = pygame.display.set_mode((screen_width, screen_height))


box = pygame.Rect(0, 0, 50, 50)
halfx = box.x/2

# Score

font = pygame.font.Font('freesansbold.ttf', 32)
foodimg = pygame.image.load('destroy.tga').convert_alpha()

textX = 10
testY = 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_img(x, y, alpha):


    image = foodimg.copy()
    # this works on images with per pixel alpha too
    image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
    screen.blit(image, (x, y))

clock = pygame.time.Clock()
delta = 0.0
max_tps = 200.0

while True:


    show_score(textX, testY)

    show_img(100, 100, 0)
    show_img(150, 100, 0)
    show_img(250, 100, 0)
    show_img(320, 100, 0)
    #print(q)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    #ticking
    delta += clock.tick()/1000.0
    while delta > 1 / max_tps:
        delta -= 1 / max_tps

        # wcisniecie klawisza sprwadzanie
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            box.x += 1
            print(clock)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            box.x -= 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            box.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            box.y += 1

    #drawing

    for food in foods:
        food.Draw()

    for food in foods:
        if sqrt((box.x + 25 - food.x)*(box.x + 25 - food.x)+(box.y + 25 - food.y)*(box.y + 25 - food.y)) < 35:
            food.Eat()
    pygame.draw.rect(screen, (0, 150, 255), box)

    pygame.display.flip()
    screen.fill((0, 0, 0))
