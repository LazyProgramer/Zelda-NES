from tkinter import SEL
import pygame

class Player:
    def __init__(self):
        self.sprites = pygame.image.load("Zelda/Sprites/Link.png")
        self.location = (256*1.5,256*1.5)
        self.hitbox = (15,15)

    def player_move(self, x, y, display):
        # Left
        if (self.location[0] + x <= 0):
            self.location = (256*3-48, self.location[1])
            return (-1,0)
        # Right
        elif (self.location[0] + x >= 256*3-48):
            self.location = (0, self.location[1])
            return (1,0)
        # Up
        elif (self.location[1] + y <= 56*3):
            self.location = (self.location[0], 256*3-48-72)
            return (0,-1)
        # Down 
        elif (self.location[1] + y >= 256*3-72-48):
            self.location = (self.location[0], 56*3)
            return (0,1)
        
        if self.check_next_position(x, y, display):
            self.location = (self.location[0] + x, self.location[1] + y)
         
        return (0,0)

    def check_next_position(self, x, y, display):
        l = (((x + y)/6)+1)/2
        m = 1
        n = 0

        if x != 0:
            m = 0
            n = 1

        # print(f'X:{x}|Y:{y}|N:{n}|M:{m}|L:{l}')
        # print(f'Coords{((int((self.location[m]+x)*n + 1*m + 45*l)),(int((self.location[m]+y)*m + 1*n + 45*l)))}')

        for i in range(int(self.location[n]), int(self.location[n]+45)):
            if display.get_at(((int((self.location[m]+x)*n + i*m + 45*l*n)),
                               (int((self.location[m]+y)*m + i*n + 45*l*m))))[:3] != (252, 216, 168):
                return False
            
        return True

    def load_player(self, display):
        player_sprite = pygame.Surface((15,15)).convert_alpha()
        player_sprite.blit(self.sprites, (0,0), (69,11,15,15))
        player_sprite = pygame.transform.scale(player_sprite, (15*3,15*3))
        player_sprite.set_colorkey((116,116,116))
        display.blit(player_sprite, (self.location[0], self.location[1], 15*3,15*3))  
        