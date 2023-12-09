from constants import *
from commandpad import COMMAND_ARROWS

import pygame
import actors

from command import newEvent
from observer import Obeserver
from input_handler import InputHandler

from display_loader import Display_loader
from enemy_spawner import Enemy_spawner
from state import *

def main():
    display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
    clock = pygame.time.Clock()

    input_handler = InputHandler(COMMAND_ARROWS)
    pressed_keys = []
    current_event= 11

    display_loader = Display_loader()

    observer = Obeserver()
    player_1 = actors.Player(display, observer)
    enemy_spawner = Enemy_spawner()

    running = True 

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                pressed_keys.append(event.key)
            elif event.type == pygame.KEYUP:
                pressed_keys.remove(event.key)

        # Most recent pressed key is executed
        if pressed_keys:
            command = input_handler.handleInput(pressed_keys[-1])
            move_map, current_event = command().execute(player_1, current_event)
            display_loader.update_map(move_map)

            # Spawn enemies if player entered new area
            if move_map != (0,0):
                display_loader.enemy_spawners = enemy_spawner.spawn_enemy(display_loader.map_surface, display, observer)
        else:
            current_event = newEvent(current_event, 1)


        # Make background black
        display.fill(BACKGROUND)

        # Load current map and hub
        display_loader.load_map(display)
        display_loader.load_hud(display)

        # Load current player sprite
        player_1.load_hub()
        current_event = player_1.stateMachine(current_event)

        # Load enemies
        for enemy in enemy_spawner.enemies:
            if enemy.health <= 0:
                enemy_spawner.enemies.remove(enemy)
                if not enemy_spawner.enemies:
                    player_1.health += 1
            else:
                enemy.update()

        # Observer notifies actors of any collision
        observer.notify(player_1, enemy_spawner.enemies)

        # update window
        pygame.display.flip()
        clock.tick(15)

    pygame.quit()

if __name__ == "__main__":
    main()