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