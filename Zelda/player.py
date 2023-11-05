from tkinter import SEL
import pygame

from constants import WIDTH, HEIGHT, HUD_HEIGHT,SCALE, PLAYER_SPEED, PLAYER_SIZE, PLAYER_HITBOX, MYDIR

class Player:
    def __init__(self, display):
        self.sprites = pygame.image.load(MYDIR+"/Sprites/Link.png")
        self.location = (WIDTH*SCALE/2,HEIGHT*SCALE/2)

        self.display = display
        self.hitbox = (15,15)

    # Verify is next position is possible then move
    def player_move(self, x, y):

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

    # Load player sprite
    def load_player(self, display):
        player_sprite = pygame.Surface((15,15)).convert_alpha()
        player_sprite.blit(self.sprites, (0,0), (69,11,15,15))
        player_sprite = pygame.transform.scale(player_sprite, (15*3,15*3))
        player_sprite.set_colorkey((116,116,116))
        display.blit(player_sprite, (self.location[0], self.location[1], 15*3,15*3))  
        
    def update(self):
        pass