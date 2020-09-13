import pygame
import time
import random
import sys

pygame.init()
win = pygame.display.set_mode((288,512))
pygame.display.set_caption("Flappy bird")
birdimg = pygame.image.load("bird.png") # Loading images
pygame.display.set_icon(birdimg)
clock = pygame.time.Clock()
bg = pygame.image.load("bg.png")
start = pygame.transform.scale(pygame.image.load("start.png"), (150,52))
gameover = pygame.transform.scale(pygame.image.load("gameover.png"), (288,512))
mouse = pygame.mouse

def isOn(x, y, width, height, pos): # Function for the mouse position
    if pos[0] >= x and pos[0] <= x + width:
        if pos[1] >= y and pos[1] <= y + height:
            return True
    return False

class bird:
    def __init__(self, x, y):
        self.bird1 = pygame.transform.scale(pygame.image.load("bird1.png"), (34,24))
        self.bird2 = pygame.transform.scale(pygame.image.load("bird2.png"), (34,24))
        self.bird3 = pygame.transform.scale(pygame.image.load("bird3.png"), (34,24))
        self.birdpics = [self.bird1, self.bird2, self.bird3]
        self.x = x
        self.y = y
        self.width = 34
        self.height = 24
        self.moveCount = 0
        self.jumpCount = 7
        self.isJump = False
        self.image = self.birdpics[self.moveCount]
        self.score = 0

    def draw(self, win): 
        self.moveCount += 1
        if self.moveCount >= len(self.birdpics):
            self.moveCount = 0
        self.image = self.birdpics[self.moveCount]
        win.blit(self.image, (self.x,self.y))

    def fall(self):
        if self.y <= 365 :
            self.y += 8

    def jump(self):
        if self.jumpCount > -7:
            self.y -= 18
        else:
            self.jumpCount = 7
        if self.y < 0:
            self.y = 0

    def new_score(self, pipe):
        if self.x == pipe.x and not(pipe1.CheckCollide(bird)): 
            self.score += 1
        return self.score
        
class base:
    base = pygame.image.load("base.png")
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self,win): # Base moves across the screen
        if self.x > -48:
            self.x -= 4
        else:
            self.x = 0
        win.blit(self.base, (self.x,self.y))
        
class pipe:
    def __init__(self, x, y):
        self.bottom = pygame.transform.scale(pygame.image.load("pipe.png"), (52,145))
        self.top = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("pipe.png"), (52,155)), 180)
        self.x = x
        self.y = y
        self.width = 52
        self.height = 145

    def resize(self): # Two pipes, opposite eachother, changes size
        self.height = random.randint(100,275)
        self.bottom = pygame.transform.scale(pygame.image.load("pipe.png"), (52,self.height))
        self.top = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("pipe.png"), (52,300-self.height)), 180)
        self.y = 400 - self.height

    def draw(self, win):
        if self.x > -52:
            self.x -= 5
        else:
            self.x = 400
            self.resize()
        win.blit(self.bottom, (self.x,self.y))
        win.blit(self.top, (self.x,0)) 
        self.rect1 = pygame.Rect((self.x,self.y),(self.width,self.height))
        self.rect2 = pygame.Rect((self.x,0),(self.width,300-self.height))
            
    def CheckCollide(self, bird):  # did bird collide with pipe
        birdrect = pygame.Rect(bird.x, bird.y, bird.width, bird.height)
        if birdrect.colliderect(self.rect1) or birdrect.colliderect(self.rect2):
                return True  # bird hit either pipe
        return False


bird = bird(125,185)
base = base(0, 400)
pipe1 = pipe(300, 255)
pipe2 = pipe(520, 255)

def redraw_window():
    win.fill((255,255,255))
    win.blit(bg, (0,0))
    base.draw(win)
    bird.draw(win)
    pipe1.draw(win)
    pipe2.draw(win)
    bird.new_score(pipe1)
    bird.new_score(pipe2)
    score = font.render("Score: " + str(bird.score), 1, (0,0,0) )
    win.blit(score, (5,10))

begin = True
run = False
end = False
font = pygame.font.SysFont("ComicSansms", 20, True)
while begin: # start screen to prompt user to click start
    clock.tick(18)
    left_pressed, middle_pressed, right_pressed = mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    win.blit(bg, (0,0))
    bird.draw(win)
    win.blit(start,(70,410))
    for event in pygame.event.get():
        if left_pressed:
            if isOn(70,410,150,52,pos):
                begin = False
                run = True
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

while run: # main loop
    clock.tick(18)
    redraw_window()
    left_pressed, middle_pressed, right_pressed = mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    if left_pressed: # bird jumps if mouse is left clicked
        bird.jump()
    else:
        bird.fall()

    if pipe1.CheckCollide(bird) or pipe2.CheckCollide(bird):
        run = False
        end = True # game over screen

    redraw_window()
    pygame.display.update()
    
with open("Highscores.txt", "a") as highscore: # saves scores to highscore
    highscore.write("\n")
    highscore.write(str(bird.score))

num_list = []
with open("Highscores.txt","r")as f:
    for line in f.readlines():
        num_list.append(int(line))
 
highest = max(num_list) # finds the highest score
    
while end:
    clock.tick(18)
    win.blit(gameover, (0,0)) # gameover screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    CurrentScore = font.render("Final Score: " + str(bird.score), 1, (201,201,88)) # displays final score and highest score
    win.blit(CurrentScore, (30,270))
    HighestScore = font.render("Highest Score: " + str(highest), 1, (201,201,88))
    win.blit(HighestScore, (30, 300))
    pygame.display.update()
pygame.quit()