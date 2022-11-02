import pygame
from pygame import *
import methods
import vars
from sys import exit

# Initialise
pygame.init()
screen = pygame.display.set_mode((vars.Screen.width, vars.Screen.height))
pygame.display.set_caption('First Game')

# FPS
fps = 0
clock = pygame.time.Clock()
basic_font = pygame.font.Font(None, 50)
fps_text = basic_font.render(str(fps), False, "Black")


# Get images
sky = pygame.image.load(
    "Free Platform Game Assets/Platform Game Assets/Background/png/1920x1080/Background/Background.png").convert()
grass = pygame.image.load("Free Platform Game Assets/Platform Game Assets/Grass/Grass.png").convert()
grass = pygame.transform.scale(grass, (50, 50)).convert()
doux_sheet_image = pygame.image.load("dinoCharactersVersion1.1/sheets/DinoSprites - doux.png").convert_alpha()
doux_sheet = methods.SpriteSheet(doux_sheet_image)
mort_sheet_image = pygame.image.load("dinoCharactersVersion1.1/sheets/DinoSprites - mort.png").convert_alpha()
mort_sheet = methods.SpriteSheet(mort_sheet_image)

# Get frames
mort_frame_0 = mort_sheet.get_image(0, 24, 24, 3, vars.Colors.BLACK).convert_alpha()
mort_frame_0_left = pygame.transform.flip(mort_frame_0, True, False).convert_alpha()
doux_frame_0 = doux_sheet.get_image(0, 24, 24, 3, vars.Colors.BLACK).convert_alpha()
doux_frame_0_left = pygame.transform.flip(doux_frame_0, True, False).convert_alpha()

# Player variables
doux_vel = 5
doux_gravity = 0
doux_direction = "RIGHT"
mort_vel = 5
mort_gravity = 0
mort_direction = "RIGHT"


# Player rectangles
doux_rect0 = doux_frame_0.get_rect(bottomright=(50, 370))
mort_rect0 = mort_frame_0.get_rect(bottomleft=(750, 370))

while True:
    # User input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if doux_rect0.y == 295:
                    doux_gravity = -20
            if event.key == pygame.K_UP:
                if mort_rect0.y == 295:
                    mort_gravity = -20

    # Movement
    key = pygame.key.get_pressed()
    if key[K_d]:
        doux_rect0.x += doux_vel
        doux_direction = "RIGHT"
    elif key[K_a]:
        doux_rect0.x -= doux_vel
        doux_direction = "LEFT"
    if key[K_RIGHT]:
        mort_rect0.x += mort_vel
        mort_direction = "RIGHT"
    elif key[K_LEFT]:
        mort_rect0.x -= mort_vel
        mort_direction = "LEFT"

    # Gravity
    doux_gravity += 1
    doux_rect0.y += doux_gravity
    mort_gravity += 1
    mort_rect0.y += mort_gravity
    if doux_rect0.y >= 295:
        doux_rect0.y = 295
    if mort_rect0.y >= 295:
        mort_rect0.y = 295

    # Background Surfaces
    screen.blit(sky, (-100, -400))
    for i in range(int(vars.Screen.width / vars.Grass.width)):
        screen.blit(grass, (0 + i * vars.Grass.width, 350))

    # Players
    if doux_direction == "RIGHT":
        screen.blit(doux_frame_0, doux_rect0)
    else:
        screen.blit(doux_frame_0_left, doux_rect0)
    if mort_direction == "RIGHT":
        screen.blit(mort_frame_0, mort_rect0)
    else:
        screen.blit(mort_frame_0_left, mort_rect0)

    # Collisions
    if doux_rect0.colliderect(mort_rect0):
        print("collision")

    # Fps
    fps_text = basic_font.render(str(fps), True, "Black")
    screen.blit(fps_text, (750, 0))
    pygame.display.update()
    clock.tick()
    fps = int(clock.get_fps())
