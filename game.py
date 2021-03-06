import pygame, sys, random, pygame.freetype, time
import os
import math

INT_INFINITY = 999999999

screen_width = 1600
screen_height = 800

# window center
os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (0, 30)

class Arrow(object):
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
    def Draw(self):
        show_arrowimg(self.x, self.y, self.angle)

class Food(object):
    def __init__(self):
        self.phase = random.uniform(0, 2 * math.pi)
        self.size = 30
        self.x = random.randint(self.size, screen_width - self.size)
        self.y = random.randint(self.size, screen_height - self.size)
        self.eatten = False

    def Draw(self):
        if self.eatten:
            return
        t = pygame.time.get_ticks()
        z = t / 1000.0 * 2 * math.pi + self.phase
        n = 96
        q = ((math.sin(z) + 1) / 2.0 * (255 - n) + n)
        show_img(self.x - self.size/2 , self.y - self.size/2, q)

    def Eat(self):
        global score_value
        if not self.eatten:
            score_value += 1
        self.eatten = True

pygame.init()

foods = []

screen = pygame.display.set_mode((screen_width, screen_height))

font = pygame.font.Font('freesansbold.ttf', 32)
foodimg = pygame.image.load('destroy.tga')
arrowimg = pygame.image.load('arrow.png')

textX = 10
textY = 10
fpsX = 1450
fpsY = 10
timeX = 720
timeY = 10
highscoreX = 1330
highscoreY = 760
timestamp = 0


def Move(dx, dy):
    global arrow
    arrow.x += dx
    arrow.y += dy
    if arrow.x > screen_width - 64 or arrow.x < 0:
        arrow.x -= dx
    if arrow.y > screen_height - 64 or arrow.y < 0:
        arrow.y -= dy

def check_file_exist():
    return os.path.isfile("highscore.txt")

def save_to_file(x):
    highscorelist = open("highscore.txt", "w+")
    highscorelist.write(str(x))
    highscorelist.close()

def read_from_file():
    global highscore
    if not check_file_exist():
        return
    highscorelist = open("highscore.txt", "r")
    highscore = float(highscorelist.read())
    highscorelist.close()

def getRoundTime():
    global timestamp
    return pygame.time.get_ticks() / 1000 - timestamp

def isEnded():
    global score_value
    return score_value >= len(foods)

def reset_game():
    global score_value
    global foods
    global stopwatch
    score_value = 0
    stopwatch = 0
    foods.clear()
    for i in range(0, 4):
        foods.append(Food())

def show_score(x, y):
    score = font.render("SCORE : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_fps(x, y, fps):
    showfps = font.render("FPS : " + str(fps), True, (255, 255, 255))
    screen.blit(showfps, (x, y))

def show_time(x, y):
    global timestamp
    if not isEnded():
        showtime = font.render("TIME : " + str(round(getRoundTime(), 2)), True, (255, 255, 255))
    else:
        showtime = font.render("TIME : " + str(round(TimeToCollect, 2)), True, (255, 200, 0))
    screen.blit(showtime, (x, y))

def show_highscore(x, y):
        showhighscore = font.render("Highscore : " + str(highscore), True, (255, 255, 255))
        screen.blit(showhighscore, (x, y))

def show_img(x, y, alpha):

    image = foodimg.copy()
    # this works on images with per pixel alpha too
    image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
    screen.blit(image, (x, y))

def show_arrowimg(x, y, angle):
    pos = (x, y)
    w, h = foodimg.get_size()
    pivot = pygame.math.Vector2(w / 2, -h / 2)
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
    origin = (pos[0] + min_box[0] - pivot_move[0], pos[1] - max_box[1] + pivot_move[1])
    rotated_image = pygame.transform.rotate(arrowimg, angle)
    screen.blit(rotated_image, origin)

clock = pygame.time.Clock()
arrow = Arrow(0, 0, 0)
highscore =  INT_INFINITY

reset_game()

def game_loop():
    read_from_file()
    global timestamp
    global highscore
    global TimeToCollect
    game_over = False
    while not game_over:
        #timer
        start_ticking = pygame.time.get_ticks() / 1000

        if not isEnded():
            stopwatch = round(start_ticking, 2) - timestamp #hmiscore
        else:
            TimeToCollect = round(stopwatch, 2)
            if stopwatch < highscore:
                highscore = round(stopwatch, 2)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                timestamp = pygame.time.get_ticks() / 1000
                reset_game()

        show_arrowimg(arrow.x, arrow.y, arrow.angle)
        show_score(textX, textY)

        t2 = clock.tick()/1000.0
        v = 300
        s = v * t2
        fps = round(1/t2)
        show_fps(fpsX, fpsY, fps)

        show_time(timeX, timeY)

        show_highscore(highscoreX, highscoreY)

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                save_to_file(highscore)
                sys.exit(0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            dx = s * math.sin(math.radians(arrow.angle - 90))
            dy = s * math.cos(math.radians(arrow.angle - 90))
            Move(-dx, -dy)
        if keys[pygame.K_a]:
            dx = s * math.sin(math.radians(arrow.angle + 90))
            dy = s * math.cos(math.radians(arrow.angle + 90))
            Move(-dx, -dy)
        if  keys[pygame.K_w] or keys[pygame.K_UP]:
            dx = s * math.sin(math.radians(arrow.angle))
            dy = s * math.cos(math.radians(arrow.angle))
            Move(-dx, -dy)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dx = s * math.sin(math.radians(arrow.angle))
            dy = s * math.cos(math.radians(arrow.angle))
            Move(dx, dy)
        if keys[pygame.K_LEFT]:
            arrow.angle += 1
        if keys[pygame.K_RIGHT]:
            arrow.angle -= 1


        #drawing
        for food in foods:
            food.Draw()

        for food in foods:
            if math.sqrt((arrow.x + 25 - food.x)*(arrow.x + 25 - food.x)+(arrow.y + 25 - food.y)*(arrow.y + 25 - food.y)) < 35:
                food.Eat()

        pygame.display.flip()

        screen.fill((0, 0, 0))
game_loop()