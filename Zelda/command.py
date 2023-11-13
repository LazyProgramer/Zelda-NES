class Command:
    def execute():
        raise NotImplemented
    def undo():
        raise NotImplemented
    
class Up(Command):
    def execute(self, actor, current_event):
        array = {}
        array[0] = actor.player_move(0, -1)
        array[1] = newEvent(current_event, "walk")
        return array
class Down(Command):
    def execute(self, actor, current_event):
        array1 = {}
        array1[0] = actor.player_move(0, 1)
        array1[1] = newEvent(current_event, "walk")
        return array1
class Left(Command):
    def execute(self, actor, current_event):
        array2 = {}
        array2[0] = actor.player_move(-1, 0)
        array2[1] = newEvent(current_event, "walk")
        return array2
class Right(Command):
    def execute(self, actor, current_event):
        array3 = {}
        array3[0] = actor.player_move(1, 0)
        array3[1] = newEvent(current_event, "walk")
        return array3
class Attack(Command):
    def execute(self, actor, current_event):
        array4 = {}
        array4[0] = actor.attack()
        array4[1] = newEvent(current_event, "attack")
        return array4
class NoCommand(Command):
    def execute(self, actor, current_event):
        array5 = {}
        array5[0] = (0,0)
        array5[1] = newEvent(current_event, "idle")
        return array5
    
def newEvent(current_event, var):
    if current_event == "walkIdle" or current_event == "attackIdle" or current_event == "damagedIdle":
        if var == "walk":
            current_event = "idleWalk"
        elif var == "attack":
            current_event = "idleAttack"
        elif var == "damaged":
            current_event = "idleDamaged"

    elif current_event == "idleWalk" or current_event == "attackWalk" or current_event == "damagedWalk":
        if var == "idle":
            current_event = "walkIdle"
        elif var == "attack":
            current_event = "walkAttack"
        elif var == "damaged":
            current_event = "walkDamaged"

    elif current_event == "idleAttack" or current_event == "walkAttack" or current_event == "damagedAttack":
        if var == "idle":
            current_event = "attackIdle"
        elif var == "walk":
            current_event = "attackWalk"
        elif var == "damaged":
            current_event = "attackDamaged"

    elif current_event == "idleDamaged" or current_event == "walkDamaged" or current_event == "attackDamaged":
        if var == "idle":
            current_event = "damagedIdle"
        elif var == "walk":
            current_event = "damagedWalk"
        elif var == "attack":
            current_event = "damagedAttack"
    return current_event