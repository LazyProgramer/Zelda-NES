import pygame, command

COMMAND_WASD = {
    pygame.K_UP: command.Up ,
    pygame.K_DOWN : command.Down ,
    pygame.K_LEFT : command.Left ,
    pygame.K_RIGHT: command.Right ,
    pygame.K_SPACE: command.Attack
}
COMMAND_ARROWS = {
    pygame.K_UP: command.Up ,
    pygame.K_DOWN : command.Down ,
    pygame.K_LEFT : command.Left ,
    pygame.K_RIGHT: command.Right ,
    pygame.K_SPACE: command.Attack
}