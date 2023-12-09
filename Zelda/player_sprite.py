import pygame
from state import *
from constants import MYDIR, SCALE, SET_COLOR, PLAYER_SPRITE_SIZE

class PlayerSprite:
    def __init__(self):
        self.sprites = pygame.image.load(MYDIR + "/Sprites/Link.png")
        self.walk_frames = []
        self.attack_frames_hor = []
        self.attack_frames_ver = []

        self.retract = 0
        self.sword = 0

        self.f = 0
        self.tick = 0

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

    # This will automatically switch colors if player was damaged
    def set_colors(self, display, current_event, frame, destination):
        # Replace colors with damaged colors
        if current_event % 10 == 4 or current_event > 40:    #"damaged" in current_event.lower():
            pixels = pygame.PixelArray(frame)
            pixels.replace((200,  76, 12),(255, 255, 255))
            pixels.replace((252, 152, 56),(252, 152,  56))
            pixels.replace((128, 208, 16),(216,  40,   0))
            pixels.close()
        
        # Replace colors back to original colors
        else:
            pixels = pygame.PixelArray(frame)
            pixels.replace((255, 255, 255),(200,  76, 12))
            pixels.replace((252, 152,  56),(252, 152, 56))
            pixels.replace((216,  40,   0),(128, 208, 16))
            pixels.close()

        # Load sprite
        display.blit(frame, destination)

    def update(self, display, location, direction, current_event):
        # Count tick to help with walk animation, each tick switch frame
        self.tick += 1
        if self.tick >= 3:
            self.f += 1
            self.tick = 0

        # Load idle sprite
        if current_event < 20:  #if it's any transition to idle
            # Down
            if direction == (0,1):
                self.set_colors(display, current_event,self.walk_frames[0], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Right
            elif direction == (1,0):
                self.set_colors(display, current_event,self.walk_frames[2], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Up
            elif direction == (0,-1):
                self.set_colors(display, current_event,self.walk_frames[4], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Left
            elif direction == (-1,0):
                self.set_colors(display, current_event,self.walk_frames[6], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
        
        # Load last 2 frames of attack animation
        elif current_event == 13 or current_event == 23:  #if transition is attack - idle or attack - walk, respectively
            # Down
            if direction == (0,1):
                self.set_colors(display, current_event,self.attack_frames_ver[2 + self.retract], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,(PLAYER_SPRITE_SIZE + 11)*SCALE))
            # Right
            elif direction == (1,0):
                self.set_colors(display, current_event,self.attack_frames_hor[2 + self.retract], (location[0], location[1], (PLAYER_SPRITE_SIZE + 15)*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Up
            elif direction == (0,-1):
                self.set_colors(display, current_event,self.attack_frames_ver[6 + self.retract], (location[0], location[1] - 12 * SCALE, PLAYER_SPRITE_SIZE*SCALE,(PLAYER_SPRITE_SIZE + 11)*SCALE))
            # Left
            elif direction == (-1,0):
                self.set_colors(display, current_event,self.attack_frames_hor[6 + self.retract], (location[0] - (8 - 4 * self.retract) * SCALE, location[1], (PLAYER_SPRITE_SIZE + 15)*SCALE,PLAYER_SPRITE_SIZE*SCALE))

            if self.retract == 1:
                self.retract = 0
            self.retract += 1
            self.sword = 0
            
        # Load walk animation
        elif current_event in range(21, 31):  #if it's any transition to walk
            # Down
            if direction == (0,1):
                self.set_colors(display, current_event,self.walk_frames[0 + self.f % 2], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Right
            elif direction == (1,0):
                self.set_colors(display, current_event,self.walk_frames[2 + self.f % 2], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Up
            elif direction == (0,-1):
                self.set_colors(display, current_event,self.walk_frames[4 + self.f % 2], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Left
            elif direction == (-1,0):
                self.set_colors(display, current_event,self.walk_frames[6 + self.f % 2], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            
        # Load first 2 frames of attack animation
        elif current_event in range(31, 41):  #if it's any transition to attack
            # Down
            if direction == (0,1):    
                self.set_colors(display, current_event,self.attack_frames_ver[0 + self.sword], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,(PLAYER_SPRITE_SIZE + 11)*SCALE))
            # Right
            elif direction == (1,0):
                self.set_colors(display, current_event,self.attack_frames_hor[0 + self.sword], (location[0], location[1], (PLAYER_SPRITE_SIZE + 15)*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Up
            elif direction == (0,-1):
                self.set_colors(display, current_event,self.attack_frames_ver[4 + self.sword], (location[0], location[1] - 12 * SCALE, PLAYER_SPRITE_SIZE*SCALE,(PLAYER_SPRITE_SIZE + 11)*SCALE))
            # Left
            elif direction == (-1,0):
                self.set_colors(display, current_event,self.attack_frames_hor[4 + self.sword], (location[0] - (11 * self.sword) * SCALE, location[1], (PLAYER_SPRITE_SIZE + 15)*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            
            self.sword = 1

        # Load damaged frame
        elif current_event > 40:  #if it's any transition to damaged
            if direction == (0,1):
                self.set_colors(display, current_event,self.walk_frames[0], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Right
            elif direction == (1,0):
                self.set_colors(display, current_event,self.walk_frames[2], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Up
            elif direction == (0,-1):
                self.set_colors(display, current_event,self.walk_frames[4], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
            # Left
            elif direction == (-1,0):
                self.set_colors(display, current_event,self.walk_frames[6], (location[0], location[1], PLAYER_SPRITE_SIZE*SCALE,PLAYER_SPRITE_SIZE*SCALE))
