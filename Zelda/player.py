from tkinter import SEL
import pygame
from player_sprite import *


from constants import WIDTH, HEIGHT, HUD_HEIGHT,SCALE, PLAYER_SPEED, PLAYER_SIZE, PLAYER_HITBOX, MYDIR, SWORD_HITBOX, SET_COLOR, HEATH_SIZE

class Player:
    def __init__(self, display, observer):
        self.sprites = pygame.image.load(MYDIR+"/Sprites/Link.png")
        self.hearths = pygame.image.load(MYDIR+"/Sprites/HUD.png").convert()

        self.location = (WIDTH*SCALE/2,HEIGHT*SCALE/2)

        self.max_health = 16
        self.health = 16

        self.display = display
        self.observer = observer
        self.direction = (0,1)
        self.playerSprite = PlayerSprite

        self.player_hitbox = None
        self.sword_hitbox = None

        self.status = 0

    # Verify is next position is possible then move
    def player_move(self, x, y):
        self.direction = (x, y)
        # Map update, updates map if player leaves playble area
        # PLAYER_SPEED is here or we can cause seizure
        # Load map to the left
        if (self.location[0] + x <= 0):
            self.location = ((WIDTH-PLAYER_SIZE)*SCALE-PLAYER_SPEED, self.location[1])
            return (-1,0)
        # Load map to the right
        elif (self.location[0] + x >= (WIDTH-PLAYER_SIZE)*SCALE):
            self.location = (PLAYER_SPEED, self.location[1])
            return (1,0)
        # Load map above
        elif (self.location[1] + y <= HUD_HEIGHT*SCALE):
            self.location = (self.location[0], (HEIGHT-PLAYER_SIZE)*SCALE-PLAYER_SPEED)
            return (0,-1)
        # Load map below 
        elif (self.location[1] + y >= (HEIGHT-PLAYER_SIZE)*SCALE):
            self.location = (self.location[0], HUD_HEIGHT*SCALE+PLAYER_SPEED)
            return (0,1)
        
        # Check player collision with map
        if self.check_next_position(x, y):
            # Move to next position
            self.location = (self.location[0] + x*PLAYER_SPEED, self.location[1] + y*PLAYER_SPEED)

        return (0,0)

    # Check if player is gonna collide with a wall/water
    def check_next_position(self, x, y):
        l = ((x + y)+1)/2
        m = 1
        n = 0

        if x != 0:
            m = 0
            n = 1

        # Funny calculation to have 1 if statement instead of 8
        for i in range(int(self.location[n]), int(self.location[n]+PLAYER_HITBOX)):
            if self.display.get_at(((int((self.location[m]+x)*n + i*m + PLAYER_HITBOX*l*n)),
                               (int((self.location[m]+y)*m + i*n + PLAYER_HITBOX*l*m))))[:3] != (252, 216, 168):
                return False
            
        return True

    def load_sprites(self):
        self.playerSprite.load_sprites()

        """player_sprite = pygame.Surface((15,15)).convert_alpha()
        player_sprite.blit(self.sprites, (0,0), (69,11,15,15))
        player_sprite = pygame.transform.scale(player_sprite, (15*3,15*3))
        player_sprite.set_colorkey((116,116,116))
        display.blit(player_sprite, (self.location[0], self.location[1], 15*3,15*3))"""

    def load_player(self):
        player_sprite = pygame.Surface((PLAYER_SIZE,PLAYER_SIZE)).convert_alpha()
        if self.status == 0:

            # Get player sprite
            player_sprite.blit(self.sprites, (0,0), (35 - 34 * self.direction[1],11,PLAYER_SIZE,PLAYER_SIZE))
            player_sprite = pygame.transform.scale(player_sprite, (PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))

            if self.direction[0] < 0:
                player_sprite = pygame.transform.flip(player_sprite, True, False)

            self.sword_hitbox = (0,0,0,0)

        # Attack
        else:
            self.status = 0

            # Get sword sprite size
            if self.direction[0] == 0:                
                sword_sprite_size = (7,15)
            elif self.direction[1] == 0:
                sword_sprite_size = (16,15)

            # Get sword sprite
            sword_sprite = pygame.Surface((sword_sprite_size[0],sword_sprite_size[1])).convert_alpha()
            sword_sprite.blit(self.sprites, (0,0), (45-9*abs(self.direction[1]),154,sword_sprite_size[0],sword_sprite_size[1]))
            sword_sprite = pygame.transform.scale(sword_sprite, (sword_sprite_size[0]*SCALE,sword_sprite_size[1]*SCALE))

            # Get player sprite
            player_sprite.blit(self.sprites, (0,0), (124 - 17 * self.direction[1],11,PLAYER_SIZE,PLAYER_SIZE))
            player_sprite = pygame.transform.scale(player_sprite, (PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))

            # Rotate sprite if needed
            if self.direction[0] < 0:
                sword_sprite = pygame.transform.flip(sword_sprite, True, False)
                player_sprite = pygame.transform.flip(player_sprite, True, False)
            if self.direction[1] > 0:
                sword_sprite = pygame.transform.flip(sword_sprite, False, True)

            # Set color key to remove background grey
            sword_sprite.set_colorkey(SET_COLOR)

            # Specific sword coords to load sprite and define hitbox
            match self.direction:
                case(-1,0):
                    self.display.blit(sword_sprite, (self.location[0]-PLAYER_HITBOX+12, self.location[1]+3, 
                                                     sword_sprite_size[0]*SCALE,sword_sprite_size[1]*SCALE))
                    
                    self.sword_hitbox = (self.location[0]-PLAYER_HITBOX+9, self.location[1]+7*3,
                                         self.location[0]-PLAYER_HITBOX+9+13*3, self.location[1]+7*3+12)
            
                case(1,0):
                    self.display.blit(sword_sprite, (self.location[0]+PLAYER_HITBOX-15, self.location[1]+3, 
                                                     sword_sprite_size[0]*SCALE,sword_sprite_size[1]*SCALE))

                    self.sword_hitbox = (self.location[0]+PLAYER_HITBOX-15+9, self.location[1]+7*3,
                                         self.location[0]+PLAYER_HITBOX-15+16*3, self.location[1]+7*3+12)
            
                case(0,-1):
                    self.display.blit(sword_sprite, (self.location[0]+3*3, self.location[1]-12*3, 
                                                     sword_sprite_size[0]*SCALE,sword_sprite_size[1]*SCALE))  

                    self.sword_hitbox = (self.location[0]+4*3, self.location[1]-13*3,
                                         self.location[0]+4*3+4*3, self.location[1]-13*3+13*3)
            
                case(0,1):
                    self.display.blit(sword_sprite, (self.location[0]+5*3, self.location[1]+PLAYER_HITBOX-12, 
                                                     sword_sprite_size[0]*SCALE,sword_sprite_size[1]*SCALE))

                    self.sword_hitbox = (self.location[0]+5*3, self.location[1]+PLAYER_HITBOX-12+6,
                                         self.location[0]+5*3+5*3, self.location[1]+PLAYER_HITBOX-12+15*3)

        # Load player after sword, so sword is placed behind player
        player_sprite.set_colorkey(SET_COLOR)
        self.display.blit(player_sprite, (self.location[0], self.location[1], PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))  

        self.player_hitbox = (self.location[0], self.location[1],
                              self.location[0]+PLAYER_HITBOX, self.location[1]+PLAYER_HITBOX)
        
        # # Check hitboxes
        # pygame.draw.rect(self.display, "black", (self.player_hitbox[0], self.player_hitbox[1], 3,3))
        # pygame.draw.rect(self.display, "black", (self.player_hitbox[2], self.player_hitbox[3], 3,3))

        # pygame.draw.rect(self.display, "black", (self.sword_hitbox[0], self.sword_hitbox[1], 3,3))
        # pygame.draw.rect(self.display, "black", (self.sword_hitbox[2], self.sword_hitbox[3], 3,3))

        # Give observer current hitboxes
        self.observer.update_player(self.player_hitbox, self.sword_hitbox)

    def load_hearths(self):
        # for x in range(int(self.health)):
        #     load_heath = pygame.Surface((HEATH_SIZE,HEATH_SIZE)).convert_alpha()
        #     load_heath.blit(self.hearths, (0,0), (645,117,HEATH_SIZE,HEATH_SIZE))
        #     load_heath = pygame.transform.scale(load_heath, (HEATH_SIZE*SCALE,HEATH_SIZE*SCALE))
        #     self.display.blit(load_heath, ((176+8*(x%8))*SCALE,(32+8*(x//8))*SCALE, HEATH_SIZE*SCALE,HEATH_SIZE*SCALE))

        # for x in range(int(self.health), self.max_health):
        #     load_heath = pygame.Surface((HEATH_SIZE,HEATH_SIZE)).convert_alpha()
        #     load_heath.blit(self.hearths, (0,0), (627,117,HEATH_SIZE,HEATH_SIZE))
        #     load_heath = pygame.transform.scale(load_heath, (HEATH_SIZE*SCALE,HEATH_SIZE*SCALE))
        #     self.display.blit(load_heath, ((176+8*(x%8))*SCALE,(32+8*(x//8))*SCALE, HEATH_SIZE*SCALE,HEATH_SIZE*SCALE))
        
        # if int(self.health) - self.health < 0:
        #     x = int(self.health)
        #     load_heath = pygame.Surface((HEATH_SIZE,HEATH_SIZE)).convert_alpha()
        #     load_heath.blit(self.hearths, (0,0), (636,117,HEATH_SIZE,HEATH_SIZE))
        #     load_heath = pygame.transform.scale(load_heath, (HEATH_SIZE*SCALE,HEATH_SIZE*SCALE))
        #     self.display.blit(load_heath, ((176+8*(x%8))*SCALE,(32+8*(x//8))*SCALE, HEATH_SIZE*SCALE,HEATH_SIZE*SCALE))

        for x in range(self.max_health):
            load_heath = pygame.Surface((HEATH_SIZE,HEATH_SIZE)).convert_alpha()
            
            if self.health > x:
                load_heath.blit(self.hearths, (0,0), (645,117,HEATH_SIZE,HEATH_SIZE))
            if self.health - x == 0.5:
                load_heath.blit(self.hearths, (0,0), (636,117,HEATH_SIZE,HEATH_SIZE))
            if self.health <= x:
                load_heath.blit(self.hearths, (0,0), (627,117,HEATH_SIZE,HEATH_SIZE))

            load_heath = pygame.transform.scale(load_heath, (HEATH_SIZE*SCALE,HEATH_SIZE*SCALE))
            self.display.blit(load_heath, ((176+8*(x%8))*SCALE,(32+8*(x//8))*SCALE, HEATH_SIZE*SCALE,HEATH_SIZE*SCALE))

    def update(self):
        pass
        # display.blit(player_sprite, (self.location[0], self.location[1], 15*3,15*3))
        
    def attack(self): 
        self.status = 1

        # sword_sprite = pygame.Surface((7,15)).convert_alpha()
        # sword_sprite.blit(self.sprites, (0,0), (36,154,7,15))
        # sword_sprite = pygame.transform.scale(sword_sprite, (7*3,15*3))
        # sword_sprite.set_colorkey((116,116,116))
        # self.display.blit(sword_sprite, (self.location[0]+3*3, self.location[1]-12*3, 7*3,15*3))  

        # player_sprite = pygame.Surface((15,15)).convert_alpha()
        # player_sprite.blit(self.sprites, (0,0), (141,11,15,15))
        # player_sprite = pygame.transform.scale(player_sprite, (15*3,15*3))
        # player_sprite.set_colorkey((116,116,116))
        # self.display.blit(player_sprite, (self.location[0], self.location[1], 15*3,15*3)) 
        return (0,0)