class Command:
    def execute():
        raise NotImplemented
    def undo():
        raise NotImplemented
    
class Up(Command):
    def execute(self, actor, current_event):
        return actor.player_move(0, -1), newEvent(current_event, "walk")
class Down(Command):
    def execute(self, actor, current_event):
        return actor.player_move(0, 1), newEvent(current_event, "walk")
class Left(Command):
    def execute(self, actor, current_event):
        return actor.player_move(-1, 0), newEvent(current_event, "walk")
class Right(Command):
    def execute(self, actor, current_event):
        return actor.player_move(1, 0), newEvent(current_event, "walk")
class Attack(Command):
    def execute(self, actor, current_event):
        return actor.attack(), newEvent(current_event, "attack")
class NoCommand(Command):
    def execute(self, actor, current_event):
        return (0,0), newEvent(current_event, "idle")
    
def newEvent(current_event, var):
    if current_event == "walkIdle" or current_event == "attackIdle" or current_event == "damagedIdle" or current_event == "idleIdle":
        if var == "idle":
            current_event = "idleIdle"
        elif var == "walk":
            current_event = "idleWalk"
        elif var == "attack":
            current_event = "idleAttack"

    elif current_event == "idleWalk" or current_event == "attackWalk" or current_event == "damagedWalk" or current_event == "walkWalk":
        if var == "idle":
            current_event = "walkIdle"
        elif var == "walk":
            current_event = "walkWalk"
        elif var == "attack":
            current_event = "walkAttack"

    elif current_event == "idleAttack" or current_event == "walkAttack" or current_event == "damagedAttack" or current_event == "attackAttack":
        if var == "idle":
            current_event = "attackIdle"
        elif var == "walk":
            current_event = "attackWalk"
        elif var == "attack":
            current_event = "attackAttack"

    elif current_event == "idleDamaged" or current_event == "walkDamaged" or current_event == "attackDamaged":
        if var == "idle":
            current_event = "damagedIdle"
        elif var == "walk":
            current_event = "damagedWalk"
        elif var == "attack":
            current_event = "damagedAttack"
    return current_event