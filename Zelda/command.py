class Command:
    def execute():
        raise NotImplemented
    def undo():
        raise NotImplemented
    
class Up(Command):
    def execute(self,actor):
        x, y = actor.get_current_direction()
        if y - 1 !=0:
            actor.set_current_direction(0, -1)
class Down(Command):
    def execute(self,actor):
        x, y = actor.get_current_direction()
        if y + 1 !=0:
            actor.set_current_direction(0, 1)
class Left(Command):
    def execute(self,actor):
        x, y = actor.get_current_direction()
        if x - 1 != 0:
            actor.set_current_direction(-1, 0)
class Right(Command):
    def execute(self,actor):
        x, y = actor.get_current_direction()
        if x + 1 != 0:
            actor.set_current_direction(1, 0)