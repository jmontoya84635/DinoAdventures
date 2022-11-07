from sys import exit

import pygame
from pygame import *

import methods
import vars
import asyncio


async def run():
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

    # Player variables
    doux_vel = 5
    doux_gravity = 0
    doux_direction = "RIGHT"
    mort_vel = 5
    mort_gravity = 0
    mort_direction = "RIGHT"

    # Animations
    class mort_animations:
        collision: False
        all = mort_sheet.animation_list(24)
        all_left = mort_sheet.animation_list(24, "LEFT")
        idle = all[0:4]
        run = all[4:10]
        kick = all[10:13]
        hurt = all[14:17]
        crouch = all[17:]
        idle_left = all_left[0:4]
        run_left = all_left[5:11]
        kick_left = all_left[10:13]
        hurt_left = all_left[14:17]
        crouch_left = all_left[17:]
        current_animation = idle
        frame = 0
        current_time = 0
        last_update = 0
        cooldown = 125
        last_Key = "RIGHT"

    class doux_animations:
        collision: False
        all = doux_sheet.animation_list(24)
        all_left = doux_sheet.animation_list(24, "LEFT")
        idle = all[0:4]
        run = all[4:10]
        kick = all[10:13]
        hurt = all[14:17]
        crouch = all[17:]
        idle_left = all_left[0:4]
        run_left = all_left[5:11]
        kick_left = all_left[10:13]
        hurt_left = all_left[14:17]
        crouch_left = all_left[17:]
        current_animation = idle
        frame = 0
        current_time = 0
        last_update = 0
        cooldown = 125
        last_Key = "RIGHT"

    # Player rectangles
    doux_rect0 = doux_animations.all[0].get_rect(bottomright=(50, 370))
    mort_rect0 = mort_animations.all[0].get_rect(bottomleft=(750, 370))

    while True:
        # Collisions
        doux_col_rect = Rect(doux_rect0.x + 10, doux_rect0.y + 10, 50, 55)
        mort_col_rect = Rect(mort_rect0.x + 10, mort_rect0.y + 10, 50, 55)

        # User input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                mort_animations.frame = 0
                doux_animations.frame = 0
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
            doux_rect0.x += mort_vel
            doux_animations.current_animation = doux_animations.run
            doux_animations.last_Key = "RIGHT"
        elif key[K_a]:
            doux_rect0.x -= mort_vel
            doux_animations.current_animation = doux_animations.run_left
            doux_animations.last_Key = "LEFT"
        elif key[K_q]:
            if doux_animations.frame < 3:
                if doux_animations.last_Key == "RIGHT":
                    doux_animations.current_animation = doux_animations.kick
                elif doux_animations.last_Key == "LEFT":
                    doux_animations.current_animation = doux_animations.kick_left
        else:
            if doux_animations.last_Key == "RIGHT":
                doux_animations.current_animation = doux_animations.idle
            elif doux_animations.last_Key == "LEFT":
                doux_animations.current_animation = doux_animations.idle_left

        if key[K_RIGHT]:
            mort_rect0.x += mort_vel
            mort_animations.current_animation = mort_animations.run
            mort_animations.last_Key = "RIGHT"
        elif key[K_LEFT]:
            mort_rect0.x -= mort_vel
            mort_animations.current_animation = mort_animations.run_left
            mort_animations.last_Key = "LEFT"
        else:
            if mort_animations.last_Key == "RIGHT":
                mort_animations.current_animation = mort_animations.idle
            elif mort_animations.last_Key == "LEFT":
                mort_animations.current_animation = mort_animations.idle_left

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
        screen.blit(sky, (0,0))
        for i in range(int(vars.Screen.width / vars.Grass.width)):
            screen.blit(grass, (0 + i * vars.Grass.width, 350))

        # Players

        screen.blit(mort_animations.current_animation[mort_animations.frame], mort_rect0)
        screen.blit(doux_animations.current_animation[doux_animations.frame], doux_rect0)

        mort_animations.current_time = pygame.time.get_ticks()
        if mort_animations.current_time - mort_animations.last_update >= mort_animations.cooldown:
            if mort_animations.frame + 1 < len(mort_animations.current_animation):
                mort_animations.frame += 1
            else:
                mort_animations.frame = 0
            mort_animations.last_update = mort_animations.current_time

        doux_animations.current_time = pygame.time.get_ticks()
        if doux_animations.current_time - doux_animations.last_update >= doux_animations.cooldown:
            if doux_animations.frame + 1 < len(doux_animations.current_animation):
                doux_animations.frame += 1
            else:
                doux_animations.frame = 0
            doux_animations.last_update = doux_animations.current_time
        # Fps
        fps_text = basic_font.render(str(fps), True, "Black")
        screen.blit(fps_text, (750, 0))
        clock.tick(60)
        fps = int(clock.get_fps())
        pygame.display.update()
        await asyncio.sleep(0)


asyncio.run(run())
