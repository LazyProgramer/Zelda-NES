import pygame
import random
from constants import WIDTH, HEIGHT, SCALE, MYDIR, OCTOROC_SIZE, OCTOROC_SPEED, OCTOROC_HITBOX, SET_COLOR, ROCK_SIZE, ROCK_SPPED

class Projectile:
    def __init__(self):
        self.sprites = pygame.image.load(MYDIR+"/Sprites/Enemies.png")

    def get_sprites(self):
        return self.sprites

class Rock(Projectile):
    def __init__(self, location, direction):
        self.location = location
        self.direction = direction

        self.hitbox = (0,0,0,0)

        self.state = 0

    def update(self, display):
        self.location = (self.location[0] + self.direction[0]*ROCK_SPPED, self.location[1] + self.direction[1]*ROCK_SPPED)
        
        self.hitbox = (self.location[0], self.location[1]+2*SCALE, self.location[0]+6*SCALE, self.location[1]+10*SCALE)

        self.load_rock(display)

        # pygame.draw.rect(display, "black", (self.hitbox[0], self.hitbox[1], SCALE, SCALE))
        # pygame.draw.rect(display, "black", (self.hitbox[2], self.hitbox[3], SCALE, SCALE))

    def crashed(self):
        if self.state == 1:
            return True
        if 0 < self.location[0] < 600 and 0 < self.location[1] < 600:
            return False
        return True
    
        # self.location[0] + 4, self.location[1] # UP: - 2| DOWN: - 4
        # (self.location[0], self.location[1] + 7)
    
    def load_rock(self, display):
        rock_sprite = pygame.Surface((ROCK_SIZE[0],ROCK_SIZE[1])).convert_alpha()
        rock_sprite.blit(Projectile().sprites, (0,0), (69,11,ROCK_SIZE[0],ROCK_SIZE[1]))
        rock_sprite = pygame.transform.scale(rock_sprite, (ROCK_SIZE[0]*SCALE,ROCK_SIZE[1]*SCALE))
        rock_sprite.set_colorkey(SET_COLOR)
        display.blit(rock_sprite, (self.location[0], self.location[1], ROCK_SIZE[0]*SCALE,ROCK_SIZE[1]*SCALE))