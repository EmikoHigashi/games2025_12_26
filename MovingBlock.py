import sys
import os
import math
# install pygame
# python -m pip install pygame
# use command prompt
import pygame

# GitHub Copilot

pygame.init()
HERE = os.path.dirname(os.path.abspath(__file__))

# Load images from the same folder as this script.
# Provide your own 'background.png' and 'airplane.png' next to this file.
def load_image(name, fallback_size=None, fill=(200, 200, 200)):
    path = os.path.join(HERE, name)
    if os.path.exists(path):
        return pygame.image.load(path).convert_alpha()
    # fallback: simple surface
    surf = pygame.Surface(fallback_size or (100, 100), pygame.SRCALPHA)
    surf.fill(fill)
    return surf

background = load_image("background.png", fallback_size=(800, 600), fill=(30, 120, 200))
airplane_img = load_image("airplane.png", fallback_size=(64, 64), fill=(255, 255, 255))

# Window size matches background
WIDTH, HEIGHT = background.get_width(), background.get_height()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airplane - arrow keys to move")

# Airplane state
pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
vel = pygame.Vector2(0, 0)
SPEED = 300  # pixels per second
ROTATE_ENABLED = True  # rotate airplane to face movement direction

clock = pygame.time.Clock()
orig_plane = airplane_img  # keep original for rotation

running = True
while running:
    dt = clock.tick(60) / 1000.0  # seconds elapsed since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Read held keys for smooth movement
    keys = pygame.key.get_pressed()
    move = pygame.Vector2(0, 0)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        move.x -= 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        move.x += 1
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        move.y -= 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        move.y += 1

    if move.length_squared() > 0:
        move = move.normalize()
        vel = move * SPEED
    else:
        vel = pygame.Vector2(0, 0)

    pos += vel * dt

    # keep inside screen
    plane_rect = orig_plane.get_rect(center=(pos.x, pos.y))
    if plane_rect.left < 0:
        pos.x = plane_rect.width / 2
    if plane_rect.right > WIDTH:
        pos.x = WIDTH - plane_rect.width / 2
    if plane_rect.top < 0:
        pos.y = plane_rect.height / 2
    if plane_rect.bottom > HEIGHT:
        pos.y = HEIGHT - plane_rect.height / 2

    # draw
    screen.blit(background, (0, 0))

    draw_img = orig_plane
    if ROTATE_ENABLED and vel.length_squared() > 0:
        # angle: pygame rotates anticlockwise, convert from vector direction
        angle = -math.degrees(math.atan2(vel.y, vel.x)) - 90
        draw_img = pygame.transform.rotozoom(orig_plane, angle, 1.0)

    draw_rect = draw_img.get_rect(center=(pos.x, pos.y))
    screen.blit(draw_img, draw_rect.topleft)

    pygame.display.flip()

pygame.quit()
sys.exit()