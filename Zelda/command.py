from state import *

class Command:
    def execute():
        raise NotImplemented
    def undo():
        raise NotImplemented
    
class Up(Command):
    def execute(self, actor, current_event):
        return actor.player_move(0, -1), newEvent(current_event, 2)
class Down(Command):
    def execute(self, actor, current_event):
        return actor.player_move(0, 1), newEvent(current_event, 2)
class Left(Command):
    def execute(self, actor, current_event):
        return actor.player_move(-1, 0), newEvent(current_event, 2)
class Right(Command):
    def execute(self, actor, current_event):
        return actor.player_move(1, 0), newEvent(current_event, 2)
class Attack(Command):
    def execute(self, actor, current_event):
        return actor.attack(), newEvent(current_event, 3)
class NoCommand(Command):
    def execute(self, actor, current_event):
        return (0,0), newEvent(current_event, 1)
    
# Get new event
def newEvent(current_event, var):
    if current_event < 20:    #if it's any transition to idle
        if var == 1:
            current_event = State.IDLEIDLE
        elif var == 2:
            current_event = State.IDLEWALK
        elif var == 3:
            current_event = State.IDLEATTACK

    elif current_event in range(21, 31): #if it's any transition to walk
        if var == 1:
            current_event = State.WALKIDLE
        elif var == 2:
            current_event = State.WALKWALK
        elif var == 3:
            current_event = State.WALKATTACK

    elif current_event in range(31, 41): #if it's any transition to attack
        if var == 1:
            current_event = State.ATTACKIDLE
        elif var == 2:
            current_event = State.ATTACKWALK
        elif var == 3:
            current_event = State.ATTACKATTACK

    elif current_event > 40:    #if it's any transition to damaged
        if var == 1:
            current_event = State.DAMAGEDIDLE
        elif var == 2:
            current_event = State.DAMAGEDWALK
        elif var == 3:
            current_event = State.DAMAGEDATTACK
    return current_event