import pygame

from player import Player

WIDTH, HEIGHT = 256, 256
SCALE = 3
GAME_EVENT = pygame.event.custom_type()

PLAYER_SPEED = 6
BACKGROUND = "white"
# BACKGROUND = "black"

"""
missing_area = (256,24)
HUD size = (256,56)
Pause size = (256,87)
map_area = (256,176)
map = (16x8)
map id given →→ then ↓↓

main_color = (252, 216, 168)
""" 
display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
clock = pygame.time.Clock()

game_map = pygame.image.load("Map.png").convert()
loaded_map_id = 120 #1800x1240 (8,8)
# Map coords (256*(x-1)+x,176*(y-1)-y)

hubs = pygame.image.load("HUD.png").convert()

player_1 = Player()

# main_surface = pygame.Surface(256*SCALE,256*SCALE).convert_alpha()

def load_map():
    map_surface = pygame.Surface((256,176)).convert_alpha()
    map_surface.blit(game_map, (0,0), (1800,1240,256,176))
    current_map = pygame.transform.scale(map_surface, (256*SCALE,176*SCALE))
    current_map.set_colorkey((0,128,0))
    display.blit(current_map, (0, 56*SCALE, 256*SCALE,176*SCALE))  

def load_hud():
    load_hud = pygame.Surface((256,56)).convert_alpha()
    load_hud.blit(hubs, (0,0), (258,11,256,56))
    hud = pygame.transform.scale(load_hud, (256*SCALE,56*SCALE))
    hud.set_colorkey((0,128,0))   
    display.blit(hud, (0, 0, 256*SCALE,56*SCALE))

running = True

while running:
    keys_pressed = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == GAME_EVENT:
            print(event.txt)

    if keys_pressed[pygame.K_UP]:
        player_1.player_move(0, -PLAYER_SPEED, display)
    elif keys_pressed[pygame.K_DOWN]:
        player_1.player_move(0, PLAYER_SPEED, display)
    elif keys_pressed[pygame.K_LEFT]:
        player_1.player_move(-PLAYER_SPEED, 0, display)
    elif keys_pressed[pygame.K_RIGHT]:
        player_1.player_move(PLAYER_SPEED, 0, display)

    display.fill(BACKGROUND)
    load_map()
    load_hud()
    player_1.load_player(display)
    # print(display.get_at((int(256*1.5),int(256*1.5)))[:3])

    # update window
    pygame.display.flip()
    clock.tick(15)

pygame.quit()