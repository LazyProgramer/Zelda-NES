import pygame
import re

from constants import *
from player_sprite import *
from state_machine import *
from projectiles import *
from state import *

class Actor:
    def __init__(self, location, display, observer, health, size):
        self.location = location
        self.display = display
        self.observer = observer

        self.health = health
        self.size = size
        self.border = (size + 1) * SCALE

        self._direction = (0,1)

    def check_next_position(self, x, y):
        l = ((x + y)+1)/2
        m = 1
        n = 0

        if x != 0:
            m = 0
            n = 1
        # Funny calculation to have 1 if statement instead of 8
        for i in range(int(self.location[n]), int(self.location[n]+self.size*SCALE)):
            if self.display.get_at(((int((self.location[m]+x)*n + i*m + self.border*l*n)),
                               (int((self.location[m]+y)*m + i*n + self.border*l*m))))[:3] != (252, 216, 168):
                return False
            
        return True


class Player(Actor):
    def __init__(self, display, observer, location = (WIDTH*SCALE/2+3,HEIGHT*SCALE/2+3), health = 16, size = PLAYER_SIZE):
        super().__init__(location, display, observer, health, size)
        self.hub_sprites = pygame.image.load(MYDIR+"/Sprites/HUD.png").convert()
        self.max_health = health

        self.invulnerability_frames = 0
        self.took_damaged = 0
        self.sword_hitbox = (0,0,0,0)

        self.playerSprite = PlayerSprite()
        
        self.idle = Idle()
        self.walk = Walk()
        self.fight = Fight()
        self.damaged = Damaged()

        self.states = [self.walk, self.idle, self.fight, self.damaged]

        self.transitions = {    
            State.IDLEWALK: Transition(self.idle, self.walk),
            State.IDLEATTACK: Transition(self.idle, self.fight),    
            State.IDLEDAMAGED: Transition(self.idle, self.damaged),
            State.WALKIDLE: Transition(self.walk, self.idle),
            State.WALKATTACK: Transition(self.walk, self.fight),
            State.WALKDAMAGED: Transition(self.walk, self.damaged),
            State.ATTACKIDLE: Transition(self.fight, self.idle),
            State.ATTACKWALK: Transition(self.fight, self.walk),
            State.ATTACKDAMAGED: Transition(self.fight, self.damaged),
            State.DAMAGEDIDLE: Transition(self.damaged, self.idle),
            State.DAMAGEDWALK: Transition(self.damaged, self.walk),
            State.DAMAGEDATTACK: Transition(self.damaged, self.fight)
        }

        self.fsm = FSM(self.states, self.transitions)

        self.playerSprite.load_sprites()

    def get_direction(self):
        return self._direction

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
            
            self._direction = (x,y)

        return (0,0)

    # Loads sword and hearths on the hud
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

    def update(self, current_event = State.IDLEWALK):
        # Make sure sword has a hitbox
        if (current_event < 30 or current_event > 39): #if "Attack" is not in current_event
            self.sword_hitbox = (0,0,0,0)

        # Update player hitbox
        self.player_hitbox = (self.location[0], self.location[1],
                              self.location[0]+PLAYER_HITBOX, self.location[1]+PLAYER_HITBOX)
        
        # Give observer current hitboxes
        self.observer.update_player(self.player_hitbox, self.sword_hitbox)

        # Update sprite
        self.playerSprite.update(self.display, self.location, self.get_direction(), current_event)

        # If player took damage, count invulnerability frames
        if self.took_damaged == 1:
            self.invulnerability_frames -= 1

            # If invulnerability frames are over, player can take damage
            if self.invulnerability_frames < 0:
                self.took_damaged = 0

            # Update state
            if current_event < 40: #if "Damaged" is not in current_event
                current_event = 40 + current_event // 10  #current_event = re.findall('[A-Z][^A-Z]*', current_event)[-1].lower() + "Damaged"

        return current_event
        
    # Define sword hitbox
    def attack(self): 
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
        return (0,0)
    
    def stateMachine(self, current_event):
        return self.fsm.update(current_event, self)