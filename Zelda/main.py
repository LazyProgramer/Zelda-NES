import pygame

import input_handler
from state_machine import *

from commandpad import COMMAND_ARROWS
from player import Player
from display_loader import Display_loader
from constants import WIDTH, HEIGHT, SCALE, BACKGROUND

GAME_EVENT = pygame.event.custom_type()

display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
clock = pygame.time.Clock()

input_handler = input_handler.InputHandler(COMMAND_ARROWS)

idle = Idle()
walk = Walk()

states = [walk, idle]
transitions = {
    "idle": Transition(walk, idle),
    "walk": Transition(idle, walk)
}

fsm = FSM(states, transitions)

player_1 = Player(display)
player_1.load_sprites()
display_loader = Display_loader()
pressed_keys = []

state_event = None

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
        state_event = "walk"
        display_loader.update_map(move_map)
    else:
        state_event = "idle"

    # Make background black
    display.fill(BACKGROUND)
    
    # Load current map and hub
    display_loader.load_map(display)
    display_loader.load_hud(display)

    # Load current player sprite
    player_1.load_player(display)
    
    fsm.update(state_event, display, player_1)

    # update window
    pygame.display.flip()
    clock.tick(15)

pygame.quit()