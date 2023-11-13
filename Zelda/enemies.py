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

        # 0: moving | 1: attacked
        self.state = 0
        self.invulnerability_frames = 15*15

        self.hitbox = []

    def update(self):
        if self.state == 1 and self.invulnerability_frames <= 0:
            self.state = 0
            return
        else:
            self.invulnerability_frames -= 1

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
        if self.state == 0:
            self.state = 1
            self.health -= 1
            self.invulnerability_frames = 5

    def load_enemie(self):
        enemie_sprite = pygame.Surface((OCTOROC_SIZE,OCTOROC_SIZE)).convert_alpha()

        enemie_sprite.blit(Enemy().get_sprites(), (0,0), (1 + 34 * abs(self.current_direction[0]),11 + 17 * self.state,OCTOROC_SIZE,OCTOROC_SIZE))
        enemie_sprite = pygame.transform.scale(enemie_sprite, (OCTOROC_SIZE*SCALE,OCTOROC_SIZE*SCALE))

        if self.current_direction[0] > 0:
            enemie_sprite = pygame.transform.flip(enemie_sprite, True, False)
        elif self.current_direction[1] < 0:
            enemie_sprite = pygame.transform.flip(enemie_sprite, False, True)

        enemie_sprite.set_colorkey(SET_COLOR)

        self.display.blit(enemie_sprite, (self.location[0], self.location[1], OCTOROC_SIZE*SCALE,OCTOROC_SIZE*SCALE))
        
     