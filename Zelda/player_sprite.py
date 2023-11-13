import pygame
from constants import MYDIR, PLAYER_SIZE, SCALE, SET_COLOR

class PlayerSprite:
    def __init__(self):
        self.sprites = pygame.image.load(MYDIR + "/Sprites/Link.png")
        self.walk_frames = []

        self.f = 0
        self.tick = 0

        # self.walkUpArray = None
        # self.walkLeftArray = None
        # self.walkRightArray = None
        # self.walkDownArray = None

    def load_sprites(self):
        # Save all frames in 1 array
        # Frames are organized in the following order : Down > Right > Up > Left;
        # with each direction having both its frames one after the other
        for x in range(8):
            if x < 6:
                walk_frame = pygame.Surface((PLAYER_SIZE,PLAYER_SIZE)).convert_alpha()

                walk_frame.blit(self.sprites, (0,0), (1 + 17 * x,11,PLAYER_SIZE,PLAYER_SIZE))

                walk_frame = pygame.transform.scale(walk_frame, (PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))
            else:
                walk_frame = self.walk_frames[x - 4]
                
                walk_frame = pygame.transform.flip(walk_frame, True, False)


            walk_frame.set_colorkey(SET_COLOR)
            self.walk_frames.append(walk_frame)


        # #display.blit(player_sprite, (self.location[0], self.location[1], PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))
        # downLeftLegSprite = pygame.Surface((15,15)).convert_alpha()
        # downLeftLegSprite.blit(self.sprites, (0,0), (69,11,15,15)) #ponto 69,11
        # downLeftLegSprite = pygame.transform.scale(downLeftLegSprite, (PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))
        # downLeftLegSprite.set_colorkey((116,116,116))
        
        # downRightLegSprite = pygame.Surface((15,15)).convert_alpha()
        # downRightLegSprite.blit(self.sprites, (0,0), (85,11,15,15)) #ponto 85,11
        # downRightLegSprite = pygame.transform.scale(downRightLegSprite, (PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))
        # downRightLegSprite.set_colorkey((116,116,116))

        # self.walkDownArray = [downLeftLegSprite, downRightLegSprite]

        # rightLeftLegSprite = pygame.Surface((15,15)).convert_alpha()
        # rightLeftLegSprite.blit(self.sprites, (0,0), (101,11,15,15)) #ponto 101,11
        # rightLeftLegSprite = pygame.transform.scale(rightLeftLegSprite, (PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))
        # rightLeftLegSprite.set_colorkey((116,116,116))

        # rightRightLegSprite = pygame.Surface((15,15)).convert_alpha()
        # rightRightLegSprite.blit(self.sprites, (0,0), (117,11,15,15)) #ponto 117,11
        # rightRightLegSprite = pygame.transform.scale(rightRightLegSprite, (PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))
        # rightRightLegSprite.set_colorkey((116,116,116))

        # self.walkRightArray = [rightLeftLegSprite, rightRightLegSprite]

        # leftLeftLegSprite = pygame.transform.flip(rightLeftLegSprite, True, False)
        # leftRightLegSprite = pygame.transform.flip(rightRightLegSprite, True, False)

        # self.walkLeftArray = [leftLeftLegSprite, leftRightLegSprite]

        # upLeftLegSprite = pygame.Surface((15,15)).convert_alpha()
        # upLeftLegSprite.blit(self.sprites, (0,0), (133,11,15,15)) #ponto 133,11
        # upLeftLegSprite = pygame.transform.scale(upLeftLegSprite, (PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))
        # upLeftLegSprite.set_colorkey((116,116,116))

        # upRightLegSprite = pygame.Surface((15,15)).convert_alpha()
        # upRightLegSprite.blit(self.sprites, (0,0), (149,11,15,15)) #ponto 149,11
        # upRightLegSprite = pygame.transform.scale(upRightLegSprite, (PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))
        # upRightLegSprite.set_colorkey((116,116,116))

        # self.walkUpArray = [upLeftLegSprite, upRightLegSprite]

    def update(self, display, location, direction):
        #print(direction)
        self.tick += 1
        if self.tick >= 6:
            self.f += 1
            self.tick = 0
        # Down
        if direction == (0,1): 
            display.blit(self.walk_frames[0 + self.f%2], (location[0], location[1], PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))
        # Right
        elif direction == (1,0):
            display.blit(self.walk_frames[2 + self.f%2], (location[0], location[1], PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))
        # Up
        elif direction == (0,-1):
            display.blit(self.walk_frames[4 + self.f%2], (location[0], location[1], PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))
        # Left
        elif direction == (-1,0):
            display.blit(self.walk_frames[6 + self.f%2], (location[0], location[1], PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))