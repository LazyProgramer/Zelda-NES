class Command:
    def execute():
        raise NotImplemented
    def undo():
        raise NotImplemented
    
class Up(Command):
    def execute(self,actor):
        return actor.player_move(0, -1)
class Down(Command):
    def execute(self,actor):
        return actor.player_move(0, 1)
class Left(Command):
    def execute(self,actor):
        return actor.player_move(-1, 0)
class Right(Command):
    def execute(self,actor):
        return actor.player_move(1, 0)
class Attack(Command):
    def execute(self,actor):
        return (0, 0)
class NoCommand(Command):
    def execute(self,actor):
        return (0, 0)