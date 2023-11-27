import pygame
from constants import MYDIR, WIDTH, SCALE, MAP_HEIGHT, HUD_HEIGHT
from enemies import Octoroc

class Enemy_spawner:
    def __init__(self):
        self.enemies = []
        self.game_map = pygame.image.load(MYDIR+"/Sprites/Map.png").convert()

    def spawn_enemy(self, map_surface, display, observer):
        self.enemies = []
        enemy_spawners = []
        x = 0
        y = 0
        while y < MAP_HEIGHT:
            if map_surface.get_at((x,y))[:3] == (255, 0, 0):
                self.enemies.append(Octoroc(display, observer, (x * SCALE, (HUD_HEIGHT + y) * SCALE)))
                enemy_spawners.append((x,y))
            x += 1
            if x >= WIDTH:
                x = 0
                y += 1
        return enemy_spawners