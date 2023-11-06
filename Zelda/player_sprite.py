import pygame

class PlayerSprite:
    def __init__(self):
        self.sprites = pygame.image.load("Zelda/Sprites/Link.png")
        self.walkUpArray = {}
        self.walkLeftArray = {}
        self.walkRightArray = {}
        self.walkDownArray = {}

    def load_sprites(self):
        #display.blit(player_sprite, (self.location[0], self.location[1], 15*3,15*3))
        downLeftLegSprite = pygame.Surface((15,15)).convert_alpha()
        downLeftLegSprite.blit(self.sprites, (0,0), (69,11,15,15)) #ponto 69,11
        downLeftLegSprite = pygame.transform.scale(downLeftLegSprite, (15*3,15*3))
        downLeftLegSprite.set_colorkey((116,116,116))
        
        downRightLegSprite = pygame.Surface((15,15)).convert_alpha()
        downRightLegSprite.blit(self.sprites, (0,0), (85,11,15,15)) #ponto 85,11
        downRightLegSprite = pygame.transform.scale(downRightLegSprite, (15*3,15*3))
        downRightLegSprite.set_colorkey((116,116,116))

        self.walkDownArray = [downLeftLegSprite, downRightLegSprite]

        rightLeftLegSprite = pygame.Surface((15,15)).convert_alpha()
        rightLeftLegSprite.blit(self.sprites, (0,0), (101,11,15,15)) #ponto 101,11
        rightLeftLegSprite = pygame.transform.scale(rightLeftLegSprite, (15*3,15*3))
        rightLeftLegSprite.set_colorkey((116,116,116))

        rightRightLegSprite = pygame.Surface((15,15)).convert_alpha()
        rightRightLegSprite.blit(self.sprites, (0,0), (117,11,15,15)) #ponto 117,11
        rightRightLegSprite = pygame.transform.scale(rightRightLegSprite, (15*3,15*3))
        rightRightLegSprite.set_colorkey((116,116,116))

        self.walkRightArray = [rightLeftLegSprite, rightRightLegSprite]

        leftLeftLegSprite = pygame.transform.flip(rightLeftLegSprite, True, False)
        leftRightLegSprite = pygame.transform.flip(rightRightLegSprite, True, False)

        self.walkLeftArray = [leftLeftLegSprite, leftRightLegSprite]

        upLeftLegSprite = pygame.Surface((15,15)).convert_alpha()
        upLeftLegSprite.blit(self.sprites, (0,0), (133,11,15,15)) #ponto 133,11
        upLeftLegSprite = pygame.transform.scale(upLeftLegSprite, (15*3,15*3))
        upLeftLegSprite.set_colorkey((116,116,116))

        upRightLegSprite = pygame.Surface((15,15)).convert_alpha()
        upRightLegSprite.blit(self.sprites, (0,0), (149,11,15,15)) #ponto 149,11
        upRightLegSprite = pygame.transform.scale(upRightLegSprite, (15*3,15*3))
        upRightLegSprite.set_colorkey((116,116,116))

        self.walkUpArray = [upLeftLegSprite, upRightLegSprite]
