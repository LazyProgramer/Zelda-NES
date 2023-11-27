import pygame

import input_handler

from commandpad import COMMAND_ARROWS
from constants import WIDTH, HEIGHT, SCALE, BACKGROUND

from observer import Obeserver

from player import Player
from display_loader import Display_loader
from enemies import Octoroc
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

# octoroc_1 = Octoroc((WIDTH*SCALE/3,HEIGHT*SCALE/2))
# octoroc_2 = Octoroc((WIDTH*SCALE/4,HEIGHT*SCALE/2))
# octoroc_3 = Octoroc((WIDTH*SCALE/3,HEIGHT*SCALE/3))
# octoroc_4 = Octoroc((WIDTH*SCALE-WIDTH*SCALE/4,HEIGHT*SCALE-HEIGHT*SCALE/2))
# octoroc_5 = Octoroc((WIDTH*SCALE-WIDTH*SCALE/3,HEIGHT*SCALE-HEIGHT*SCALE/3))
# enemies = [octoroc_1,octoroc_2,octoroc_3,octoroc_4,octoroc_5]

# octoroc = Octoroc(display, observer, (WIDTH*SCALE/3,HEIGHT*SCALE/3))
enemies = []
enemy_spawner = Enemy_spawner()

current_event = "walkIdle"

"""idle = Idle()
walk = Walk()
attack = Fight()
damaged = Damaged()

states = [walk, idle, attack, damaged]
transitions = {    
    "idleWalk": Transition(idle, walk),
    "idleAttack": Transition(idle, attack),    
    "idleDamaged": Transition(idle, damaged),
    "walkIdle": Transition(walk, idle),
    "walkAttack": Transition(walk, attack),
    "walkDamaged": Transition(walk, damaged),
    "attackIdle": Transition(attack, idle),
    "attackWalk": Transition(attack, walk),
    "attackDamaged": Transition(attack, damaged),
    "damagedIdle": Transition(damaged, idle),
    "damagedWalk": Transition(damaged, walk),
    "damagedAttack": Transition(damaged, attack)
}

fsm = FSM(states, transitions)"""

player_1 = Player(display, observer)
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
        move_map, current_event = command().execute(player_1, current_event)
        print(current_event)
        display_loader.update_map(move_map)

        if move_map != (0,0):
            display_loader.enemy_spawners = enemy_spawner.spawn_enemy(display_loader.map_surface, display, observer)


    # Make background black
    display.fill(BACKGROUND)
    
    # Load current map and hub
    display_loader.load_map(display)
    display_loader.load_hud(display)

    # Load current player sprite
    player_1.load_player()
    player_1.load_hub()
    player_1.update(display)
    
    player_1.stateMachine(current_event)
    # fsm.update(state_event, player_1)
    # fsm.update(current_event, display, player_1)

    # Load enemies
    for enemy in enemy_spawner.enemies:
        if enemy.health <= 0:
            enemy_spawner.enemies.remove(enemy)
        else:
            enemy.update()
            # enemy.load_enemie()

    observer.notify(player_1, enemy_spawner.enemies)
    
    # update window
    pygame.display.flip()
    clock.tick(15)

pygame.quit()