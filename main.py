import pygame
import random
import sounddevice as sd
import numpy as np

# -----------------------------
# All constantes
# -----------------------------
width = 400
height = 300
scale = 30
pygame.init()  
scr = pygame.display.set_mode((width,height))

WHITE = (255,255,255)
ground = height//1.3
voice_limite = 4
global volume
volume = 0
global score
score = 0

font = pygame.font.SysFont("arial", 20)

# -----------------------------
# All classes
# -----------------------------
class Obstacle:
    instances=[]
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = ground + y
        self.size = size*scale
        self.color = color
        Obstacle.instances.append(self)
    
    def draw(self):
        pygame.draw.rect(scr, self.color, pygame.Rect(self.x,self.y - self.size,scale,self.size))

    def move(self):
        self.x -= 2

        if (self.x < 0):
            player.score += 1
            self.die()

        if (collision(self, player)):
            player.score = 0
            self.die()
            #print("loose")

    def die(self):
        Obstacle.instances.remove(self)
        
        i = random.randint(1,3)
        color = (0,0,0)
        if (i == 1):
            color = (0,255,0)
            Obstacle(width, 0, i, color)
        if (i == 2):
            color = (255,0,0)
            Obstacle(width, 0, i, color)
        if (i == 3):
            color = (0,0,255)
            Obstacle(width, -scale*3, 1, color)
        
        
class Player:
    def __init__(self, color):
        self.x = scale
        self.y = ground
        self.color = color
        self.size = scale*2
        self.state = 0
        self.score = 0
        

    def draw(self):
        pygame.draw.rect(scr, self.color, pygame.Rect(self.x, self.y - self.size, scale, self.size))
        v = volume
        if (v > voice_limite and self.state == 0):
            self.jump(v)
            
        self.gravity()
    
    def gravity(self):
        if (self.y < ground):
            self.y += 1.5
        else:
            self.state = 0

        
    def jump(self, v):
        if ((self.y < ground - scale * 4) == False):
            self.y -= v

        

        
class Map:
    def __init__(self):
        self.size = 4
        self.score = 0

    def draw(self):
        pygame.draw.rect(scr, (255,255,255), pygame.Rect(0,ground,width,5))

# -----------------------------
# main functions
# -----------------------------


def drawObstacles():
    for element in Obstacle.instances:
        element.draw()
        element.move()
    
def collision(a, b):
    return (a.x < b.x + scale and a.x + scale > b.x and a.y < b.y + a.size and a.size + a.y > b.y)

def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    global volume
    volume = volume_norm

# -----------------------------
# Init
# -----------------------------

player = Player((255,0,255))
my_map = Map()
obstacle = Obstacle(width, 0, 1, (0,255,0))

# -----------------------------
# Main loop
# -----------------------------

run = True
with sd.Stream(callback=print_sound):
    while(run):
        pygame.time.delay(10)
        pygame.draw.rect(scr, (0,0,0), pygame.Rect(0,0,width, height))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        my_map.draw()
        player.draw()
        drawObstacles()
        score = str(player.score)
        textimage = font.render(score, True, (255,255,255))
        scr.blit(textimage, (4,4))

        pygame.display.update()

# closes the pygame window 
pygame.quit()