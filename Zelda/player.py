from tkinter import SEL
import pygame
from player_sprite import *
from state_machine import *


from constants import WIDTH, HEIGHT, HUD_HEIGHT,SCALE, PLAYER_SPEED, PLAYER_SIZE, PLAYER_SPRITE_SIZE, PLAYER_HITBOX, MYDIR, SWORD_SIZE, SET_COLOR, HEATH_SIZE, INVULNERABILITY_FRAMES

class Player:
    def __init__(self, display, observer):
        self.sprites = pygame.image.load(MYDIR+"/Sprites/Link.png")
        self.hub_sprites = pygame.image.load(MYDIR+"/Sprites/HUD.png").convert()

        self.location = (WIDTH*SCALE/2+3,HEIGHT*SCALE/2+3)

        self.max_health = 16
        self.health = 16

        self.display = display
        self.observer = observer
        
        self._direction = (0,1)
        self.playerSprite = PlayerSprite()

        self.status = 0
        
        self.idle = Idle()
        self.walk = Walk()
        self.fight = Fight()
        self.damaged = Damaged()

        self.states = [self.walk, self.idle, self.fight, self.damaged]
        self.transitions = {    
            "idleWalk": Transition(self.idle, self.walk),
            "idleAttack": Transition(self.idle, self.fight),    
            "idleDamaged": Transition(self.idle, self.damaged),
            "walkIdle": Transition(self.walk, self.idle),
            "walkAttack": Transition(self.walk, self.fight),
            "walkDamaged": Transition(self.walk, self.damaged),
            "attackIdle": Transition(self.fight, self.idle),
            "attackWalk": Transition(self.fight, self.walk),
            "attackDamaged": Transition(self.fight, self.damaged),
            "damagedIdle": Transition(self.damaged, self.idle),
            "damagedWalk": Transition(self.damaged, self.walk),
            "damagedAttack": Transition(self.damaged, self.fight)
        }

        self.fsm = FSM(self.states, self.transitions)

        self.left = LeftLeg()
        self.right = RightLeg()

        self.spriteStates = [self.left, self.right]

        self.spriteTransitions = {
            "leftRight": Transition(self.left, self.right),
            "rightLeft": Transition(self.right, self.left)
        }

        self.spriteFSM = FSM(self.spriteStates, self.spriteTransitions)

        self.invulnerability_frames = 0
        self.took_damaged = 0

    def get_direction(self):
        return self._direction

    def set_direction(self, direction):
        self._direction = direction

        self.player_hitbox = None
        self.sword_hitbox = None

        self.status = 0

    # Verify is next position is possible then move
    def player_move(self, x, y):
        self._direction = (x, y)
        # Map update, updates map if player leaves playble area
        # PLAYER_SPEED is here or we can cause seizure
        # Load map to the left
        if (self.location[0] + x <= 0):
            self.location = ((WIDTH-PLAYER_SIZE)*SCALE-PLAYER_SPEED, self.location[1])
            return (-1,0)
        # Load map to the right
        elif (self.location[0] + x >= (WIDTH-PLAYER_SIZE)*SCALE):
            self.location = (PLAYER_SPEED + 3, self.location[1])
            return (1,0)
        # Load map above
        elif (self.location[1] + y <= HUD_HEIGHT*SCALE):
            self.location = (self.location[0], (HEIGHT-PLAYER_SIZE)*SCALE-PLAYER_SPEED)
            return (0,-1)
        # Load map below 
        elif (self.location[1] + y >= (HEIGHT-PLAYER_SIZE)*SCALE):
            self.location = (self.location[0], HUD_HEIGHT*SCALE+PLAYER_SPEED-3)
            return (0,1)
        
        # Check player collision with map
        if self.check_next_position(x, y):
            # Move to next position
            self.location = (self.location[0] + x*PLAYER_SPEED, self.location[1] + y*PLAYER_SPEED)
            
            self.set_direction((x,y))

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
        for i in range(int(self.location[n]), int(self.location[n]+PLAYER_SIZE*SCALE)):
            if self.display.get_at(((int((self.location[m]+x)*n + i*m + PLAYER_HITBOX*l*n)),
                               (int((self.location[m]+y)*m + i*n + PLAYER_HITBOX*l*m))))[:3] != (252, 216, 168):
                return False
            
        return True

    def load_sprites(self):
        self.playerSprite.load_sprites()

    def load_player(self):
        if self.status == 0:

            # # Get player sprite
            # player_sprite.blit(self.sprites, (0,0), (35 - 34 * self._direction[1],11,PLAYER_SIZE,PLAYER_SIZE))
            # player_sprite = pygame.transform.scale(player_sprite, (PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))

            # if self._direction[0] < 0:
            #     player_sprite = pygame.transform.flip(player_sprite, True, False)

            self.sword_hitbox = (0,0,0,0)

        # Attack
        else:
            # Sprite 
            # Size:
            # (16,27) -> Up Down
            # (16,16), (27, 16), (23, 16), (19, 16) -> Left Right
            # Coords:
            # (94,47) -> Down (0,1)  || (16,27)::(111,47)
            # (94,77) -> Left Right  || (27,16)::(111,77)
            # (94,97) -> Up   (0,-1) || (16,28)::(111,97)

            self.status = 0
            # n = 0
            # m = 0
            # if self._direction[1] == -1:
            #     n = 1

            # # Get sprite size: (16,27) -> Up Down || (27, 16) -> Left Right
            # sprite_size = (PLAYER_SPRITE_SIZE + 11 * abs(self._direction[0]), PLAYER_SPRITE_SIZE + 11 * abs(self._direction[1]) + n)

            # # Load player attack sprite
            # player_sprite = pygame.Surface(sprite_size).convert_alpha()
            # player_sprite.blit(self.sprites, (0,0), (111, 72 - 25 * self._direction[1] + 5 * abs(self._direction[0]),sprite_size[0],sprite_size[1]))
            # player_sprite = pygame.transform.scale(player_sprite, (sprite_size[0]*SCALE,sprite_size[1]*SCALE))

            # # Rotate if player looking left
            # if self._direction[0] == -1:
            #     player_sprite = pygame.transform.flip(player_sprite, True, False)
            #     m = 1

            # # Change all background colors (only green here) to the same color
            # pixels = pygame.PixelArray(player_sprite)
            # pixels.replace((0,128,0),(SET_COLOR))
            # pixels.close()

            # # Set background color as transparent
            # player_sprite.set_colorkey(SET_COLOR)

            # # Load player attack sprite
            # self.display.blit(player_sprite, (self.location[0] - 12 * m * SCALE, self.location[1] - 12 * n * SCALE, sprite_size[0]*SCALE,sprite_size[1]*SCALE))  

            # Update sword hitbox
            match self._direction:
                case(-1,0):
                    self.sword_hitbox = (self.location[0]-PLAYER_HITBOX+9, self.location[1]+7*3,
                                         self.location[0]-PLAYER_HITBOX+9+13*3, self.location[1]+7*3+12)
            
                case(1,0):
                    self.sword_hitbox = (self.location[0]+PLAYER_HITBOX-15+9, self.location[1]+7*3,
                                         self.location[0]+PLAYER_HITBOX-15+16*3, self.location[1]+7*3+12)
            
                case(0,-1):
                    self.sword_hitbox = (self.location[0]+4*3, self.location[1]-13*3,
                                         self.location[0]+4*3+4*3, self.location[1]-13*3+13*3)
            
                case(0,1):
                    self.sword_hitbox = (self.location[0]+5*3, self.location[1]+PLAYER_HITBOX-12+6,
                                         self.location[0]+5*3+5*3, self.location[1]+PLAYER_HITBOX-12+15*3)

        # Update player hitbox
        self.player_hitbox = (self.location[0], self.location[1],
                              self.location[0]+PLAYER_HITBOX, self.location[1]+PLAYER_HITBOX)
        
        # # Check hitboxes
        # pygame.draw.rect(self.display, "black", (self.player_hitbox[0], self.player_hitbox[1], 3,3))
        # pygame.draw.rect(self.display, "black", (self.player_hitbox[2], self.player_hitbox[3], 3,3))

        # pygame.draw.rect(self.display, "black", (self.sword_hitbox[0], self.sword_hitbox[1], 3,3))
        # pygame.draw.rect(self.display, "black", (self.sword_hitbox[2], self.sword_hitbox[3], 3,3))

        # Give observer current hitboxes
        self.observer.update_player(self.player_hitbox, self.sword_hitbox)

    def load_hub(self):
        load_sword = pygame.Surface((SWORD_SIZE[0],SWORD_SIZE[1])).convert_alpha()
        load_sword.blit(self.hub_sprites, (0,0), (564,137,SWORD_SIZE[0],SWORD_SIZE[1]))
        load_sword = pygame.transform.scale(load_sword, (SWORD_SIZE[0]*SCALE,SWORD_SIZE[1]*SCALE))
        self.display.blit(load_sword, (128*SCALE,24*SCALE, SWORD_SIZE[0]*SCALE,SWORD_SIZE[1]*SCALE))
        
        for x in range(self.max_health):
            load_heath = pygame.Surface((HEATH_SIZE,HEATH_SIZE)).convert_alpha()
            
            if self.health > x:
                load_heath.blit(self.hub_sprites, (0,0), (645,117,HEATH_SIZE,HEATH_SIZE))
            if self.health - x == 0.5:
                load_heath.blit(self.hub_sprites, (0,0), (636,117,HEATH_SIZE,HEATH_SIZE))
            if self.health <= x:
                load_heath.blit(self.hub_sprites, (0,0), (627,117,HEATH_SIZE,HEATH_SIZE))

            load_heath = pygame.transform.scale(load_heath, (HEATH_SIZE*SCALE,HEATH_SIZE*SCALE))
            self.display.blit(load_heath, ((176+8*(x%8))*SCALE,(32+8*(x//8))*SCALE, HEATH_SIZE*SCALE,HEATH_SIZE*SCALE))

    # Needs invulnerability frames
    def tookDamaged(self):
        if self.took_damaged == 0:
            self.took_damaged = 1
            self.health -= 0.5
            self.invulnerability_frames = INVULNERABILITY_FRAMES

    def update(self, display, current_event = "idleWalk"):
        if self.took_damaged == 1 and self.invulnerability_frames <= 0:
            self.took_damaged = 0
        else:
            self.invulnerability_frames -= 1

        # display.blit(player_sprite, (self.location[0], self.location[1], 15*3,15*3))
        return self.playerSprite.update(self.display, self.location, self.get_direction(), current_event)
        
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
    
    def stateMachine(self, current_event):
        return self.fsm.update(self.display, current_event, self)