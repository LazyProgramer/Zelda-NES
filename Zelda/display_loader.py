import pygame
from constants import WIDTH,MAP_HEIGHT,HUD_HEIGHT,SCALE,MYDIR,BACKGROUND,GREEN
from enemies import Octoroc

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
        
        self.enemy_spawners = []

        self.map_coords = (8,8)
        self.map_surface = None
        self.update_map_surface()


    def update_map(self, new_map):
        self.map_coords = (self.map_coords[0] + new_map[0],self.map_coords[1] + new_map[1])
        self.update_map_surface()

    def update_map_surface(self):
        map_x = WIDTH*(self.map_coords[0]-1)+self.map_coords[0]
        map_y = MAP_HEIGHT*(self.map_coords[1]-1)+self.map_coords[1]
        self.map_surface = pygame.Surface((WIDTH,MAP_HEIGHT)).convert_alpha()
        self.map_surface.blit(self.game_map, (0,0), (map_x,map_y,WIDTH,MAP_HEIGHT))

    def load_map(self, display):
        for coords in self.enemy_spawners:
            self.map_surface.set_at(coords, (252, 216, 168))
        current_map = pygame.transform.scale(self.map_surface, (WIDTH*SCALE,MAP_HEIGHT*SCALE))
        current_map.set_colorkey(GREEN)
        display.blit(current_map, (0, HUD_HEIGHT*SCALE, WIDTH*SCALE,MAP_HEIGHT*SCALE)) 

    def load_hud(self, display):
        load_hud = pygame.Surface((WIDTH,HUD_HEIGHT)).convert_alpha()
        load_hud.blit(self.hubs, (0,0), (258,11,WIDTH,HUD_HEIGHT))
        hud = pygame.transform.scale(load_hud, (WIDTH*SCALE,HUD_HEIGHT*SCALE))
        hud.set_colorkey(GREEN)   
        display.blit(hud, (0, 0, WIDTH*SCALE,HUD_HEIGHT*SCALE))

    def load_hearths(self, display):
        for x in range(16):
            load_heath = pygame.Surface((8,8)).convert_alpha()
            load_heath.blit(self.hubs, (0,0), (645,117,8,8))
            load_heath = pygame.transform.scale(load_heath, (8*SCALE,8*SCALE))
            display.blit(load_heath, ((434-258+8*(x%8))*SCALE,(43-11+8*(x//8))*SCALE, 8*SCALE,8*SCALE))