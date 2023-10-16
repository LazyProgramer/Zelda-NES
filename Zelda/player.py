import pygame

class Player:
    def __init__(self):
        self.sprites = pygame.image.load("Link.png")
        self.location = (256*1.5,256*1.5)
        self.hitbox = (15,15)

    def player_move(self, x, y, display):
        if self.check_next_position(x, y, display):
            self.location = (self.location[0] + x, self.location[1] + y)

    """
    TODO
    Add bytonic sort for all posible ground colors
    Add way to still be able to enter dungeons (probably just use black)
    Add check if reach edge to change map 
    Simplify code (I know)
    """
    def check_next_position(self, x, y, display):
        if y == -6:
            print("UP")
            for i in range(int(self.location[0]), int(self.location[0]+45)):
                if display.get_at((i,int(self.location[1])+y))[:3] != (252, 216, 168):
                    return False
        elif y == 6:
            print("DOWN")
            for i in range(int(self.location[0]), int(self.location[0]+45)):
                if display.get_at((i,int(self.location[1]+45+y)))[:3] != (252, 216, 168):
                    return False
        elif x == -6:
            print("LEFT")
            for i in range(int(self.location[1]), int(self.location[1]+45)):
                if display.get_at((int(self.location[0])+x,i))[:3] != (252, 216, 168):
                    return False
        elif x == 6:
            print("RIGHT")
            for i in range(int(self.location[1]), int(self.location[1]+45)):
                if display.get_at((int(self.location[0]+45+x),i))[:3] != (252, 216, 168):
                    return False
        return True

    def load_player(self, display):
        player_sprite = pygame.Surface((15,15)).convert_alpha()
        player_sprite.blit(self.sprites, (0,0), (69,11,15,15))
        player_sprite = pygame.transform.scale(player_sprite, (15*3,15*3))
        player_sprite.set_colorkey((116,116,116))
        display.blit(player_sprite, (self.location[0], self.location[1], 15*3,15*3))  
        