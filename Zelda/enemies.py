import pygame
import random
from projectiles import Rock
from constants import WIDTH, HEIGHT, SCALE, HUD_HEIGHT, MYDIR, OCTOROC_SIZE, OCTOROC_SPRITE_SIZE, OCTOROC_SPEED, OCTOROC_HITBOX, SET_COLOR, INVULNERABILITY_FRAMES

class Enemy:
    def __init__(self):
        self.sprites = pygame.image.load(MYDIR+"/Sprites/Enemies.png")
        # self.location
        # self.speed
        # self.size
        # self.current_direction
        # self.change_direction

    def get_sprites(self):
        return self.sprites
    
    def chace_player(self):
        pass

    def out_of_bounds(self, enemy):
        if (enemy.location[0] + enemy.current_direction[0]*enemy.speed <= 0):
            enemy.current_direction = (1,0)
            enemy.change_direction = -0.05
            return True, (1,0), -0.05
        elif (enemy.location[0] + enemy.current_direction[0]*enemy.speed >= (WIDTH-enemy.size)*SCALE):
            enemy.current_direction = (-1,0)
            enemy.change_direction = -0.05
            return True, (-1,0), -0.05
        elif (enemy.location[1] + enemy.current_direction[1]*enemy.speed <= HUD_HEIGHT*SCALE):
            enemy.current_direction = (0,1)
            enemy.change_direction = -0.05
            return True, (0,1), -0.05
        elif (enemy.location[1] + enemy.current_direction[1]*enemy.speed >= (HEIGHT-enemy.size)*SCALE):
            enemy.current_direction = (0,-1)
            enemy.change_direction = -0.05
            return True, (0,-1), -0.05

# -----------------------------------------------------------

class Octoroc(Enemy):
    def __init__(self, display, observer, location = (WIDTH*SCALE/3,HEIGHT*SCALE/2)):
        self.location = location
        self.health = 3

        self.size = OCTOROC_SIZE
        self.speed = OCTOROC_SPEED

        self.change_direction = 0
        self.current_direction = (1, 0)
        self.directions = [(0, -1),(0, 1),(-1, 0),(1, 0)]
        
        self.display = display
        self.observer = observer

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
            self.current_direction = random.choice(self.directions)

        # Make sure enemy doesn't leave map
        if Enemy().out_of_bounds(self):
            pass

        # Verify if next position is in bounds and incricese chance to change direction
        elif self.check_next_position(self.current_direction[0], self.current_direction[1]):
            # Move to next position
            self.location = (self.location[0] + self.current_direction[0]*OCTOROC_SPEED, self.location[1] + self.current_direction[1]*OCTOROC_SPEED)
            self.change_direction += 0.05

        self.hitbox = (self.location[0], self.location[1],self.location[0]+OCTOROC_HITBOX, self.location[1]+OCTOROC_HITBOX)

        if self.rock:
            self.rock.update(self.display)
            self.observer.update_projectiles(self.rock)
            if self.rock.crashed():
                self.rock = None
        # else:
        #     self.observer.update_projectiles((0,0,0,0))

        # # Check hitbox
        # pygame.draw.rect(self.display, "black", (self.hitbox[0], self.hitbox[1], 3, 3))
        # pygame.draw.rect(self.display, "black", (self.hitbox[2], self.hitbox[3], 3, 3))

        # Give observer current position
        self.observer.update_enemy(self.current_direction, self.hitbox)
        # print(self.observer.overlap(self.hitbox))
        self.load_enemie()

    def check_next_position(self, x, y):
        l = ((x + y)+1)/2
        m = 1
        n = 0

        if x != 0:
            m = 0
            n = 1

        # Funny calculation to have 1 if statement instead of 8
        for i in range(int(self.location[n]), int(self.location[n]+OCTOROC_SIZE*SCALE)):
            if self.display.get_at(((int((self.location[m]+x)*n + i*m + OCTOROC_HITBOX*l*n)),
                               (int((self.location[m]+y)*m + i*n + OCTOROC_HITBOX*l*m))))[:3] != (252, 216, 168):
                self.change_direction = 1
                return False
            
        return True
    
    def damaged(self):
        if self.state == 0:
            self.state = 1
            self.health -= 1
            self.invulnerability_frames = INVULNERABILITY_FRAMES

    def shoot(self):
        if not self.rock:
            self.rock = Rock(self.location, self.current_direction)

    def load_enemie(self):
        enemie_sprite = pygame.Surface((OCTOROC_SPRITE_SIZE,OCTOROC_SPRITE_SIZE)).convert_alpha()

        enemie_sprite.blit(Enemy().sprites, (0,0), (18 + 34 * abs(self.current_direction[0]),11 + 17 * self.state,OCTOROC_SPRITE_SIZE,OCTOROC_SPRITE_SIZE))
        enemie_sprite = pygame.transform.scale(enemie_sprite, (OCTOROC_SPRITE_SIZE*SCALE,OCTOROC_SPRITE_SIZE*SCALE))

        if self.current_direction[0] > 0:
            enemie_sprite = pygame.transform.flip(enemie_sprite, True, False)
        elif self.current_direction[1] < 0:
            enemie_sprite = pygame.transform.flip(enemie_sprite, False, True)

        enemie_sprite.set_colorkey(SET_COLOR)

        self.display.blit(enemie_sprite, (self.location[0], self.location[1], OCTOROC_SPRITE_SIZE*SCALE,OCTOROC_SPRITE_SIZE*SCALE))
        