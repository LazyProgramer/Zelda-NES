from state import *

class Command:
    def execute():
        raise NotImplemented
    def undo():
        raise NotImplemented
    
class Up(Command):
    def execute(self, actor, current_event):
        return actor.player_move(0, -1), newEvent(current_event, State.WALKWALK)
class Down(Command):
    def execute(self, actor, current_event):
        return actor.player_move(0, 1), newEvent(current_event, State.WALKWALK)
class Left(Command):
    def execute(self, actor, current_event):
        return actor.player_move(-1, 0), newEvent(current_event, State.WALKWALK)
class Right(Command):
    def execute(self, actor, current_event):
        return actor.player_move(1, 0), newEvent(current_event, State.WALKWALK)
class Attack(Command):
    def execute(self, actor, current_event):
        return actor.attack(), newEvent(current_event, State.ATTACKATTACK)
class NoCommand(Command):
    def execute(self, actor, current_event):
        return (0,0), newEvent(current_event, State.IDLEIDLE)
    
#Get new event
def newEvent(current_event, var):
    if current_event < 20:    #if it's any transition to idle
        if var == 11:
            current_event = State.IDLEIDLE
        elif var == 22:
            current_event = State.IDLEWALK
        elif var == 33:
            current_event = State.IDLEATTACK

    elif current_event in range(21, 31): #if it's any transition to walk
        if var == 11:
            current_event = State.WALKIDLE
        elif var == 22:
            current_event = State.WALKWALK
        elif var == 33:
            current_event = State.WALKATTACK

    elif current_event in range(31, 41): #if it's any transition to attack
        if var == 11:
            current_event = State.ATTACKIDLE
        elif var == 22:
            current_event = State.ATTACKWALK
        elif var == 33:
            current_event = State.ATTACKATTACK

    elif current_event > 40:    #if it's any transition to damaged
        if var == 11:
            current_event = State.DAMAGEDIDLE
        elif var == 22:
            current_event = State.DAMAGEDWALK
        elif var == 33:
            current_event = State.DAMAGEDATTACK
    return current_event