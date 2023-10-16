class InputHandler:
    def __init__(self, command):
        self.command = command

    def handleInput(self, key):
        return self.command[key]
