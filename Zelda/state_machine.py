import pygame

class State:
    def __init__(self, name) -> None:
        self.name = name

    def enter(self):
        print("Entering {self.name}")

    def update(self, object):
        object.update()

    def exit(self):
        print("Leaving {self.name}")


class Transition:
    def __init__(self, _from, _to) -> None:
        self._from = _from
        self._to = _to

class Idle(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object):
        print("waiting for your command...")
        return super().update(object)
    
class Walk(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object):
        print("Moving")
        return super().update(object)
    

class FSM:
    def __init__(self, states: list[State], transitions: dict[Transition]) -> None:
        self._states = states
        self._transitions = transitions

        self.current_state: State = self._states[0]
        self.end: State = self._states[-1]

    def update(self, event, object):
        if event:
            trans = self._transitions.get(event)
            if trans and trans._from == self.current_state:
                self.current_state.exit()
                self.current_state = trans._to
                self.current_state.enter()
        self.current_state.update(object)

        if self.current_state == self.end:
            self.current_state.exit()
            return False
        return True