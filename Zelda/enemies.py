import pygame
import random
from constants import WIDTH, HEIGHT, SCALE, MYDIR, OCTOROC_SIZE, OCTOROC_SPEED, OCTOROC_HITBOX, SET_COLOR

class Enemy:
    def __init__(self):
        self.sprites = pygame.image.load(MYDIR+"/Sprites/Enemies.png")

    def get_sprites(self):
        return self.sprites
    
    def chace_player(self):
        pass

# -----------------------------------------------------------

class Octoroc:
    def __init__(self, display, observer, location = (WIDTH*SCALE/3,HEIGHT*SCALE/2)):
        self.location = location
        self.health = 3

        self.change_direction = 0
        self.current_direction = (1, 0)
        self.directions = [(0, -1),(0, 1),(-1, 0),(1, 0)]
        
        self.display = display
        self.observer = observer

        self.hitbox = []

    def update(self):
        # if damaged():
        #     pass

        # Change direction, bigger chance to change the more he keeps moving in the same direction
        if self.change_direction > random.random():
            self.change_direction = -0.05
            self.current_direction = random.choice(self.directions)

        # Verify if next position is in bounds and incricese chance to change direction
        if self.check_next_position(self.current_direction[0], self.current_direction[1]):
            # Move to next position
            self.location = (self.location[0] + self.current_direction[0]*OCTOROC_SPEED, self.location[1] + self.current_direction[1]*OCTOROC_SPEED)
            self.change_direction += 0.05

        self.hitbox = (self.location[0], self.location[1],self.location[0]+OCTOROC_HITBOX, self.location[1]+OCTOROC_HITBOX)

        # # Check hitbox
        # pygame.draw.rect(self.display, "black", (self.hitbox[0], self.hitbox[1], 3, 3))
        # pygame.draw.rect(self.display, "black", (self.hitbox[2], self.hitbox[3], 3, 3))

        # Give observer current position
        self.observer.update_enemy(self.hitbox)
        # print(self.observer.overlap(self.hitbox))

    def check_next_position(self, x, y):
        l = ((x + y)+1)/2
        m = 1
        n = 0

        if x != 0:
            m = 0
            n = 1

        # Funny calculation to have 1 if statement instead of 8
        for i in range(int(self.location[n]), int(self.location[n]+OCTOROC_HITBOX)):
            if self.display.get_at(((int((self.location[m]+x)*n + i*m + OCTOROC_HITBOX*l*n)),
                               (int((self.location[m]+y)*m + i*n + OCTOROC_HITBOX*l*m))))[:3] != (252, 216, 168):
                self.change_direction = 1
                return False
            
        return True
    
    def damaged(self):
        pass    

    def load_enemie(self):
        enemie_sprite = pygame.Surface((OCTOROC_SIZE,OCTOROC_SIZE)).convert_alpha()
        enemie_sprite.blit(Enemy().get_sprites(), (0,0), (1,11,OCTOROC_SIZE,OCTOROC_SIZE))
        enemie_sprite = pygame.transform.scale(enemie_sprite, (OCTOROC_SIZE*SCALE,OCTOROC_SIZE*SCALE))
        enemie_sprite.set_colorkey(SET_COLOR)
        self.display.blit(enemie_sprite, (self.location[0], self.location[1], OCTOROC_SIZE*SCALE,OCTOROC_SIZE*SCALE))  

        # # Get player sprite
        # enemie_sprite.blit(Enemy().get_sprites(), (0,0), (35 - 34 * self.current_direction[1],11,OCTOROC_SIZE,OCTOROC_SIZE))
        # enemie_sprite = pygame.transform.scale(enemie_sprite, (OCTOROC_SIZE*SCALE,OCTOROC_SIZE*SCALE))

        # if self.current_direction[0] < 0:
        #     enemie_sprite = pygame.transform.flip(enemie_sprite, True, False)
        # elif self.current_direction[1] > 0:
        #     enemie_sprite = pygame.transform.flip(enemie_sprite, False, True)
# 1 11
# 35 11

    # Not sure if better then pure random after 10 moves
    # def change_direction(self):
    #     weights = [0.5,0.5,0.5,0.5]
    #     id = self.directions.index(self.current_direction)
    #     next_mov_id = (id+1)%4
    #     weights[id] = 20 - self.moves_in_same_direction / 4
    #     weights[next_mov_id] = self.moves_in_same_direction / 4
    #     print(weights)
    #     new_direction = random.choices(self.directions, weights=weights)[0]
    #     if self.current_direction != new_direction:
    #         self.current_direction = new_direction
    #         self.moves_in_same_direction = 0
     