import pygame
from constants import MYDIR, PLAYER_SIZE, SCALE, SET_COLOR

class PlayerSprite:
    def __init__(self):
        self.sprites = pygame.image.load(MYDIR + "/Sprites/Link.png")
        self.walk_frames = []
        self.attack_frames = []

        self.f = 0
        self.tick = 0

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


    def update(self, display, location, direction, current_event):
        #print(direction)
        self.tick += 1
        if self.tick >= 6:
            self.f += 1
            self.tick = 0
        # Down
        if current_event == "idleWalk" or current_event == "attackWalk" or current_event == "damagedWalk" or current_event == "walkIdle" or current_event == "attackIdle" or current_event == "damagedIdle":
            #por condiçao para se tiver dentro dos 10 frames invulneravel, nao mudar para sprites normais. Se passar os 10 frames ja muda
            if direction == (0,1):    
                display.blit(self.walk_frames[0], (location[0], location[1], PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))
            # Right
            elif direction == (1,0):
                display.blit(self.walk_frames[2], (location[0], location[1], PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))
            # Up
            elif direction == (0,-1):
                display.blit(self.walk_frames[4], (location[0], location[1], PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))
            # Left
            elif direction == (-1,0):
                display.blit(self.walk_frames[6], (location[0], location[1], PLAYER_SIZE*SCALE,PLAYER_SIZE*SCALE))
        #elif current_event == "idleAttack" or current_event == "walkAttack" or current_event == "damagedAttack":
            #dar refactor do player attacking sprite para aqui


        #elif current_event == "idleDamaged" or current_event == "walkDamaged" or current_event == "damagedAttack":
            #dar replace da cor verde da roupa do link por outra cor e ficar invulneravel por 10 segundos.