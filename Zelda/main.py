import pygame

import input_handler

from commandpad import COMMAND_ARROWS
from player import Player
from constants import WIDTH, HEIGHT, MAP_HEIGHT, HUD_HEIGHT, SCALE, PLAYER_SPEED, BACKGROUND

GAME_EVENT = pygame.event.custom_type()

"""
missing_area = (WIDTH,24)
HUD size = (WIDTH,HUD_HEIGHT)
Pause size = (WIDTH,87)
map_area = (WIDTH,MAP_HEIGHT)
map = (16x8)
map id given →→ then ↓↓

main_color = (252, 216, 168)
""" 
display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
clock = pygame.time.Clock()

input_handler = input_handler.InputHandler(COMMAND_ARROWS)

game_map = pygame.image.load("Zelda/Sprites/Map.png").convert()
global move_map
move_map = (0,0)
loaded_map_id = (8,8)
# Inicial map: 1800x1240 (8,8)
# Map coords (WIDTH*(x-1)+x,MAP_HEIGHT*(y-1)+y)

hubs = pygame.image.load("Zelda/Sprites/HUD.png").convert()

player_1 = Player(display)

# main_surface = pygame.Surface(WIDTH*SCALE,WIDTH*SCALE).convert_alpha()

def update_map(new_map):
    global move_map
    move_map = (0,0)
    # print(move_map)
    return (loaded_map_id[0] + new_map[0],loaded_map_id[1] + new_map[1])

def load_map(x, y):
    map_x = WIDTH*(x-1)+x
    map_y = MAP_HEIGHT*(y-1)+y
    map_surface = pygame.Surface((WIDTH,MAP_HEIGHT)).convert_alpha()
    map_surface.blit(game_map, (0,0), (map_x,map_y,WIDTH,MAP_HEIGHT))
    current_map = pygame.transform.scale(map_surface, (WIDTH*SCALE,MAP_HEIGHT*SCALE))
    current_map.set_colorkey((0,128,0))
    display.blit(current_map, (0, HUD_HEIGHT*SCALE, WIDTH*SCALE,MAP_HEIGHT*SCALE))  

def load_hud():
    load_hud = pygame.Surface((WIDTH,HUD_HEIGHT)).convert_alpha()
    load_hud.blit(hubs, (0,0), (258,11,WIDTH,HUD_HEIGHT))
    hud = pygame.transform.scale(load_hud, (WIDTH*SCALE,HUD_HEIGHT*SCALE))
    hud.set_colorkey((0,128,0))   
    display.blit(hud, (0, 0, WIDTH*SCALE,HUD_HEIGHT*SCALE))

running = True

while running:
    keys_pressed = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == GAME_EVENT:
            print(event.txt)

    # if event.type == pygame.KEYDOWN:
    #     command = input_handler.handleInput(event.key)
    #     move_map = command().execute(player_1)

    # TODO
    # change way of key press working multiple times
    # change how unpressing 1 key can stop all movement
    if True in keys_pressed:
        command = input_handler.handleInput(event.key)
        move_map = command().execute(player_1)
        
    # if keys_pressed[pygame.K_UP]:
    #     move_map = player_1.player_move(0, -PLAYER_SPEED, display)
    # elif keys_pressed[pygame.K_DOWN]:
    #     move_map = player_1.player_move(0, PLAYER_SPEED, display)
    # elif keys_pressed[pygame.K_LEFT]:
    #     move_map = player_1.player_move(-PLAYER_SPEED, 0, display)
    # elif keys_pressed[pygame.K_RIGHT]:
    #     move_map = player_1.player_move(PLAYER_SPEED, 0, display)


    display.fill(BACKGROUND)
    
    loaded_map_id = update_map(move_map)
    load_map(loaded_map_id[0],loaded_map_id[1])
    load_hud()
    player_1.load_player(display)
    # print(display.get_at((int(WIDTH*1.5),int(WIDTH*1.5)))[:3])

    # update window
    pygame.display.flip()
    clock.tick(15)

pygame.quit()