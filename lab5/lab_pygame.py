import pygame
import sys
import random, math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CS 108 Pygame")

clock = pygame.time.Clock()
FPS   = 60

x, y   = 400, 300
vx, vy = 6, 6
particles = []
color_mode = 0
gravity = True

class Particle:
    def __init__(self, x, y, mode=0):

        angle  = random.uniform(0, 2 * math.pi)
        speed  = random.uniform(1, 4)
        self.x  = x
        self.y  = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life     = 1.0               # 1.0 = fully alive
        self.decay    = random.uniform(0.01, 0.03)
        self.radius   = random.randint(3, 8)
        if mode == 0:   # purple nebula
            self.color = (random.randint(150,255), random.randint(50,150), random.randint(200,255))
        elif mode == 1: # fire
            self.color = (random.randint(200,255), random.randint(50,150), 0)
        elif mode == 2: # ice
            self.color = (0, random.randint(150,255), random.randint(200,255))

    def update(self, mx=0, my=0, attract=False):
        if attract:
            dx = mx - self.x
            dy = my - self.y
            dist = math.sqrt(dx**2 + dy**2) + 1
            self.vx += (dx / dist) * 0.5
            self.vy += (dy / dist) * 0.5

        self.vx *= 0.98        # drag
        if gravity:
            self.vy +=0.05
        self.vy *= 0.98
        self.x  += self.vx
        self.y  += self.vy
        self.life -= self.decay

    def draw(self, surface):
        if self.life <= 0:
            return
        alpha  = int(self.life * 255)
        radius = int(self.radius * self.life)
        color  = (
            int(self.color[0] * self.life),
            int(self.color[1] * self.life),
            int(self.color[2] * self.life),
        )
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), max(1, radius))

    def is_dead(self):
        return self.life <= 0

while True:
    
    # 1. Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                color_mode = (color_mode + 1) % 3
            if event.key == pygame.K_g:
                gravity = not gravity
        


    # 2. Update state

    mx, my = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()

    if pygame.mouse.get_pressed()[0]:
        for _ in range(20):
            particles.append(Particle(mx, my, mode=color_mode))
    
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        color_mode = (color_mode + 1) % 3

    right_held = pygame.mouse.get_pressed()[2]
    for p in particles:
        p.update(mx, my, attract=right_held)

    # clamp to window
    x = max(0, min(WIDTH,  x))
    y = max(0, min(HEIGHT, y))

    for p in particles:
        p.update()
        particles = [p for p in particles if not p.is_dead()]

    # 3. Draw
    screen.fill((30, 30, 46))

    for p in particles:
        p.draw(screen)
    pygame.display.flip()           # push frame to screen
    clock.tick(FPS)                 # cap at 60 FPS