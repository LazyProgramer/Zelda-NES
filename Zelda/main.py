import pygame

import input_handler

from commandpad import COMMAND_ARROWS
from constants import WIDTH, HEIGHT, SCALE, BACKGROUND

from player import Player
from display_loader import Display_loader
from enemies import Octoroc

GAME_EVENT = pygame.event.custom_type()

display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
clock = pygame.time.Clock()

input_handler = input_handler.InputHandler(COMMAND_ARROWS)

player_1 = Player(display)
display_loader = Display_loader()
pressed_keys = []

# octoroc_1 = Octoroc((WIDTH*SCALE/3,HEIGHT*SCALE/2))
# octoroc_2 = Octoroc((WIDTH*SCALE/4,HEIGHT*SCALE/2))
# octoroc_3 = Octoroc((WIDTH*SCALE/3,HEIGHT*SCALE/3))
# octoroc_4 = Octoroc((WIDTH*SCALE-WIDTH*SCALE/4,HEIGHT*SCALE-HEIGHT*SCALE/2))
# octoroc_5 = Octoroc((WIDTH*SCALE-WIDTH*SCALE/3,HEIGHT*SCALE-HEIGHT*SCALE/3))
# enemies = [octoroc_1,octoroc_2,octoroc_3,octoroc_4,octoroc_5]

octoroc = Octoroc((WIDTH*SCALE/3,HEIGHT*SCALE/3))
enemies = [octoroc]

running = True 

# TODO
# Movement needs more test runs
while running:
    # keys_pressed = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == GAME_EVENT:
            print(event.txt)

        # elif event.type == pygame.KEYDOWN:
            # key = event.key
        elif event.type == pygame.KEYDOWN:
            pressed_keys.append(event.key)
        elif event.type == pygame.KEYUP:
            pressed_keys.remove(event.key)

    # if True in keys_pressed:
        # command = input_handler.handleInput(key)
    if pressed_keys:
        command = input_handler.handleInput(pressed_keys[-1])
        move_map = command().execute(player_1)
        display_loader.update_map(move_map)

    # Make background black
    display.fill(BACKGROUND)
    
    # Load current map and hub
    display_loader.load_map(display)
    display_loader.load_hud(display)

    # Load current player sprite
    player_1.load_player(display)

    # Load enemie
    for enemy in enemies:
        enemy.update(display)
        enemy.load_enemie(display)

    # update window
    pygame.display.flip()
    clock.tick(15)

pygame.quit()