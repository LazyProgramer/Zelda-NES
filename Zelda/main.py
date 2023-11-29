import pygame

import input_handler
import actors

from commandpad import COMMAND_ARROWS
from constants import WIDTH, HEIGHT, SCALE, BACKGROUND

from observer import Obeserver

from display_loader import Display_loader
from enemy_spawner import Enemy_spawner

GAME_EVENT = pygame.event.custom_type()

display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
clock = pygame.time.Clock()

input_handler = input_handler.InputHandler(COMMAND_ARROWS)

observer = Obeserver()
# player_1 = Player(display, observer)
display_loader = Display_loader()
pressed_keys = []
array = {} # will contain move_map and new state

enemy_spawner = Enemy_spawner()

current_event = "walkIdle"


# player_1 = Player(display, observer)
# player_1.load_sprites()

player_1 = actors.Player(display, observer)

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
        move_map, current_event = command().execute(player_1, current_event)
        display_loader.update_map(move_map)

        if move_map != (0,0):
            display_loader.enemy_spawners = enemy_spawner.spawn_enemy(display_loader.map_surface, display, observer)


    # Make background black
    display.fill(BACKGROUND)
    
    # Load current map and hub
    display_loader.load_map(display)
    display_loader.load_hud(display)

    # Load current player sprite
    player_1.load_hub()
    player_1.update(current_event)
    
    current_event = player_1.stateMachine(current_event)
    # fsm.update(state_event, player_1)
    # fsm.update(current_event, display, player_1)

    # Load enemies
    for enemy in enemy_spawner.enemies:
        if enemy.health <= 0:
            enemy_spawner.enemies.remove(enemy)
            if not enemy_spawner.enemies:
                player_1.health += 1
        else:
            enemy.update()
            # enemy.load_enemie()

    observer.notify(player_1, enemy_spawner.enemies)
    
    # update window
    pygame.display.flip()
    clock.tick(15)

pygame.quit()