import pygame
from constants import MYDIR, SCALE, SET_COLOR, PLAYER_SPRITE_SIZE

class PlayerSprite:
    def __init__(self):
        self.sprites = pygame.image.load(MYDIR + "/Sprites/Link.png")
        self.walk_frames = []
        self.attack_frames_hor = []
        self.attack_frames_ver = []

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
                walk_frame = pygame.Surface((PLAYER_SPRITE_SIZE,PLAYER_SPRITE_SIZE)).convert_alpha()

                walk_frame.blit(self.sprites, (0,0), (1 + 17 * x,11,PLAYER_SPRITE_SIZE,PLAYER_SPRITE_SIZE))

                walk_frame = pygame.transform.scale(walk_frame, (PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            else:
                walk_frame = self.walk_frames[x - 4]
                
                walk_frame = pygame.transform.flip(walk_frame, True, False)


            walk_frame.set_colorkey(SET_COLOR)
            self.walk_frames.append(walk_frame)

        # Save all vertical attack frames
        for x in range(8):
            l = 0
            if x >= 4:
                l = 1
                x -= 4
            attack_frame = pygame.Surface((PLAYER_SPRITE_SIZE,PLAYER_SPRITE_SIZE + 11)).convert_alpha()

            attack_frame.blit(self.sprites, (0,0), (94 + 17 * x,47 + 50 * l,PLAYER_SPRITE_SIZE,PLAYER_SPRITE_SIZE + 11))

            attack_frame = pygame.transform.scale(attack_frame, (PLAYER_SPRITE_SIZE*SCALE,(PLAYER_SPRITE_SIZE + 11)*SCALE))

            # Change all background colors (only green here) to the same color
            pixels = pygame.PixelArray(attack_frame)
            pixels.replace((0,128,0),(SET_COLOR))
            pixels.close()

            attack_frame.set_colorkey(SET_COLOR)
            self.attack_frames_ver.append(attack_frame)

        # Save all horizontal attack frames
        for x in range(8):
            if x < 4:
                frame_coords = [94, 111, 139, 163]
                extra_pixels = [0,  11,  7,  3]

                attack_frame = pygame.Surface((PLAYER_SPRITE_SIZE + extra_pixels[x],PLAYER_SPRITE_SIZE)).convert_alpha()

                attack_frame.blit(self.sprites, (0,0), (frame_coords[x],77,PLAYER_SPRITE_SIZE + extra_pixels[x],PLAYER_SPRITE_SIZE))

                attack_frame = pygame.transform.scale(attack_frame, ((PLAYER_SPRITE_SIZE + extra_pixels[x])*SCALE,PLAYER_SPRITE_SIZE*SCALE))

                # Change all background colors (only green here) to the same color
                pixels = pygame.PixelArray(attack_frame)
                pixels.replace((0,128,0),(SET_COLOR))
                pixels.close()
            
            else:
                attack_frame = self.attack_frames_hor[x - 4]
                
                attack_frame = pygame.transform.flip(attack_frame, True, False)

            attack_frame.set_colorkey(SET_COLOR)
            self.attack_frames_hor.append(attack_frame)

    def clear(): #serve para criar uma surface da cor do mapa para sobrepor a do player sprite. É chamada no update antes de dar blit da proxima sprite 
        pass

    def update(self, display, location, direction, current_event):
        self.tick += 1
        if self.tick >= 6:
            self.f += 1
            self.tick = 0

        #e preciso separar o idle do walk
        if current_event == "walkIdle" or current_event == "damagedIdle" or current_event == "attackIdle":
            # Down
            if direction == (0,1):
                display.blit(self.walk_frames[0], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Right
            elif direction == (1,0):
                display.blit(self.walk_frames[2], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Up
            elif direction == (0,-1):
                display.blit(self.walk_frames[4], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Left
            elif direction == (-1,0):
                display.blit(self.walk_frames[6], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            
            return current_event
        
        # elif current_event == "attackIdle":
        #     # Down
        #     if direction == (0,1):    
        #         display.blit(self.attack_frames_ver[2 + self.f % 2], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,(PLAYER_SPRITE_SIZE + 11)*SCALE))
        #     # Right
        #     elif direction == (1,0):
        #         display.blit(self.attack_frames_hor[2 + self.f % 2], (location[0], location[1], (PLAYER_SPRITE_SIZE + 15)*SCALE,PLAYER_SPRITE_SIZE*SCALE))
        #     # Up
        #     elif direction == (0,-1):
        #         display.blit(self.attack_frames_ver[6 + self.f % 2], (location[0], location[1] - 12 * SCALE, PLAYER_SPRITE_SIZE*SCALE,(PLAYER_SPRITE_SIZE + 11)*SCALE))
        #     # Left
        #     elif direction == (-1,0):
        #         display.blit(self.attack_frames_hor[6 + self.f % 2], (location[0] - 12 * SCALE, location[1], (PLAYER_SPRITE_SIZE + 15)*SCALE,PLAYER_SPRITE_SIZE*SCALE))

        #     return current_event
            
        elif current_event == "idleWalk" or current_event == "attackWalk" or current_event == "damagedWalk":
            # Down
            if direction == (0,1):
                display.blit(self.walk_frames[0 + self.f % 2], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Right
            elif direction == (1,0):
                display.blit(self.walk_frames[2 + self.f % 2], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Up
            elif direction == (0,-1):
                display.blit(self.walk_frames[4 + self.f % 2], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Left
            elif direction == (-1,0):
                display.blit(self.walk_frames[6 + self.f % 2], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            
            return "walkIdle"

        elif current_event == "idleAttack" or current_event == "walkAttack" or current_event == "damagedAttack":
            # Down
            if direction == (0,1):    
                display.blit(self.attack_frames_ver[1], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,(PLAYER_SPRITE_SIZE + 11)*SCALE))
            # Right
            elif direction == (1,0):
                display.blit(self.attack_frames_hor[1], (location[0], location[1], (PLAYER_SPRITE_SIZE + 15)*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Up
            elif direction == (0,-1):
                display.blit(self.attack_frames_ver[5], (location[0], location[1] - 12 * SCALE, PLAYER_SPRITE_SIZE*SCALE,(PLAYER_SPRITE_SIZE + 11)*SCALE))
            # Left
            elif direction == (-1,0):
                display.blit(self.attack_frames_hor[5], (location[0] - 12 * SCALE, location[1], (PLAYER_SPRITE_SIZE + 15)*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            
            return "attackIdle"
        
        #elif current_event == "idleDamaged" or current_event == "walkDamaged" or current_event == "damagedAttack":

            #return "damagedIdle"