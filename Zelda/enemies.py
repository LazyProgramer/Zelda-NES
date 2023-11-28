import pygame
import random

import actors
from projectiles import Rock
from constants import *

class Enemy(actors.Actor):
    def __init__(self, location, display, observer, health, size):
        super().__init__(location, display, observer, health, size)
        self.sprites = pygame.image.load(MYDIR+"/Sprites/Enemies.png")
    
    def out_of_bounds(self, enemy):
        if (enemy.location[0] + enemy._direction[0]*enemy.speed <= 0):
            enemy._direction = (1,0)
            enemy.change_direction = -0.05
            return True, (1,0), -0.05
        elif (enemy.location[0] + enemy._direction[0]*enemy.speed >= (WIDTH-enemy.size)*SCALE):
            enemy._direction = (-1,0)
            enemy.change_direction = -0.05
            return True, (-1,0), -0.05
        elif (enemy.location[1] + enemy._direction[1]*enemy.speed <= HUD_HEIGHT*SCALE):
            enemy._direction = (0,1)
            enemy.change_direction = -0.05
            return True, (0,1), -0.05
        elif (enemy.location[1] + enemy._direction[1]*enemy.speed >= (HEIGHT-enemy.size)*SCALE):
            enemy._direction = (0,-1)
            enemy.change_direction = -0.05
            return True, (0,-1), -0.05

class Octoroc(Enemy):
    def __init__(self, location, display, observer, health = 3, size = OCTOROC_SIZE):
        super().__init__(location, display, observer, health, size)
        self.speed = OCTOROC_SPEED

        self.change_direction = 0
        self.directions = [(0, -1),(0, 1),(-1, 0),(1, 0)]

        # 0: moving | 1: attacked
        self.state = 0
        self.invulnerability_frames = 0

        self.rock = None

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
            self._direction = random.choice(self.directions)

        # Make sure enemy doesn't leave map
        if self.out_of_bounds(self):
            pass

        # Verify if next position is in bounds and incricese chance to change direction
        elif self.check_next_position(self._direction[0], self._direction[1]):
            # Move to next position
            self.location = (self.location[0] + self._direction[0]*OCTOROC_SPEED, self.location[1] + self._direction[1]*OCTOROC_SPEED)
            self.change_direction += 0.05
        
        else:
            self.change_direction = 1

        self.hitbox = (self.location[0], self.location[1],self.location[0]+OCTOROC_HITBOX, self.location[1]+OCTOROC_HITBOX)

        if self.rock:
            self.rock.update(self.display)
            self.observer.update_projectiles(self.rock)
            if self.rock.crashed():
                self.rock = None

        # Give observer current position
        self.observer.update_enemy(self._direction, self.hitbox)
        self.load_enemie()
    
    def damaged(self):
        if self.state == 0:
            self.state = 1
            self.health -= 1
            self.invulnerability_frames = INVULNERABILITY_FRAMES

    def shoot(self):
        if not self.rock:
            self.rock = Rock(self.location, self._direction)

    def load_enemie(self):
        enemie_sprite = pygame.Surface((OCTOROC_SPRITE_SIZE,OCTOROC_SPRITE_SIZE)).convert_alpha()

        enemie_sprite.blit(self.sprites, (0,0), (18 + 34 * abs(self._direction[0]),11 + 17 * self.state,OCTOROC_SPRITE_SIZE,OCTOROC_SPRITE_SIZE))
        enemie_sprite = pygame.transform.scale(enemie_sprite, (OCTOROC_SPRITE_SIZE*SCALE,OCTOROC_SPRITE_SIZE*SCALE))

        if self._direction[0] > 0:
            enemie_sprite = pygame.transform.flip(enemie_sprite, True, False)
        elif self._direction[1] < 0:
            enemie_sprite = pygame.transform.flip(enemie_sprite, False, True)

        enemie_sprite.set_colorkey(SET_COLOR)

        self.display.blit(enemie_sprite, (self.location[0], self.location[1], OCTOROC_SPRITE_SIZE*SCALE,OCTOROC_SPRITE_SIZE*SCALE))
        