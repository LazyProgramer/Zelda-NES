from command import NoCommand

class InputHandler:
    def __init__(self, command):
        self.command = command

    def handleInput(self, key):
        if self.command.get(key) == None:
            return NoCommand
        return self.command.get(key)
