import pygame
from constants import WIDTH,MAP_HEIGHT,HUD_HEIGHT,SCALE,MYDIR

"""
missing_area = (WIDTH,24)
HUD size = (WIDTH,HUD_HEIGHT)
Pause size = (WIDTH,87)
map_area = (WIDTH,MAP_HEIGHT)
map = (16x8)
map id given →→ then ↓↓

main_color = (252, 216, 168)
""" 

class Display_loader:
    def __init__(self):        
        self.game_map = pygame.image.load(MYDIR+"/Sprites/Map.png").convert()
        self.hubs = pygame.image.load(MYDIR+"/Sprites/HUD.png").convert()
        self.map_coords = (1,7)

    def update_map(self, new_map):
        self.map_coords = (self.map_coords[0] + new_map[0],self.map_coords[1] + new_map[1])

    def load_map(self, display):
        map_x = WIDTH*(self.map_coords[0]-1)+self.map_coords[0]
        map_y = MAP_HEIGHT*(self.map_coords[1]-1)+self.map_coords[1]
        map_surface = pygame.Surface((WIDTH,MAP_HEIGHT)).convert_alpha()
        map_surface.blit(self.game_map, (0,0), (map_x,map_y,WIDTH,MAP_HEIGHT))
        current_map = pygame.transform.scale(map_surface, (WIDTH*SCALE,MAP_HEIGHT*SCALE))
        current_map.set_colorkey((0,128,0))
        display.blit(current_map, (0, HUD_HEIGHT*SCALE, WIDTH*SCALE,MAP_HEIGHT*SCALE)) 

    def load_hud(self, display):
        load_hud = pygame.Surface((WIDTH,HUD_HEIGHT)).convert_alpha()
        load_hud.blit(self.hubs, (0,0), (258,11,WIDTH,HUD_HEIGHT))
        hud = pygame.transform.scale(load_hud, (WIDTH*SCALE,HUD_HEIGHT*SCALE))
        hud.set_colorkey((0,128,0))   
        display.blit(hud, (0, 0, WIDTH*SCALE,HUD_HEIGHT*SCALE))