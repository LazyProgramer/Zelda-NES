import pygame
import random
from constants import WIDTH, HEIGHT, SCALE, MYDIR, OCTOROC_SIZE, OCTOROC_SPEED, OCTOROC_HITBOX

class Enemy:
    def __init__(self):
        self.sprites = pygame.image.load(MYDIR+"/Sprites/Enemies.png")

    def get_sprites(self):
        return self.sprites
    
    def chace_player(self):
        pass

# -----------------------------------------------------------

class Octoroc:
    def __init__(self, location = (WIDTH*SCALE/3,HEIGHT*SCALE/2)):
        self.location = location
        self.health = 3

        self.moves_in_same_direction = 0
        self.current_direction = (1, 0)
        self.directions = [(0, -1),(0, 1),(-1, 0),(1, 0)]

    def update(self, display):
        if self.moves_in_same_direction > 10:
            self.moves_in_same_direction = 0
            self.current_direction = random.choice(self.directions)

        # self.change_direction()

        if self.check_next_position(self.current_direction[0], self.current_direction[1], display):
            # Move to next position
            self.location = (self.location[0] + self.current_direction[0]*OCTOROC_SPEED, self.location[1] + self.current_direction[1]*OCTOROC_SPEED)
            self.moves_in_same_direction += 1

    def check_next_position(self, x, y, display):
        l = ((x + y)+1)/2
        m = 1
        n = 0

        if x != 0:
            m = 0
            n = 1

        # Funny calculation to have 1 if statement instead of 8
        for i in range(int(self.location[n]), int(self.location[n]+OCTOROC_HITBOX)):
            if display.get_at(((int((self.location[m]+x)*n + i*m + OCTOROC_HITBOX*l*n)),
                               (int((self.location[m]+y)*m + i*n + OCTOROC_HITBOX*l*m))))[:3] != (252, 216, 168):
                self.moves_in_same_direction = 40
                return False
            
        return True
    
    def load_enemie(self, display):
        enemie_sprite = pygame.Surface((16,16)).convert_alpha()
        enemie_sprite.blit(Enemy().get_sprites(), (0,0), (1,11,16,16))
        enemie_sprite = pygame.transform.scale(enemie_sprite, (16*3,16*3))
        enemie_sprite.set_colorkey((116,116,116))
        display.blit(enemie_sprite, (self.location[0], self.location[1], 16*3,16*3))  

    # Not sure if better then pure random after 10 moves
    def change_direction(self):
        weights = [0.5,0.5,0.5,0.5]
        id = self.directions.index(self.current_direction)
        next_mov_id = (id+1)%4
        weights[id] = 20 - self.moves_in_same_direction / 4
        weights[next_mov_id] = self.moves_in_same_direction / 4
        print(weights)
        new_direction = random.choices(self.directions, weights=weights)[0]
        if self.current_direction != new_direction:
            self.current_direction = new_direction
            self.moves_in_same_direction = 0
     