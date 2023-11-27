import pygame

class State:
    def __init__(self, name) -> None:
        self.name = name

    def enter(self):
        # print(f"Entering {self.name}")
        pass

    def update(self, display, object, event):
        return object.update(display, event)

    def exit(self):
        # print(f"Leaving {self.name}")
        pass


class Transition:
    def __init__(self, _from, _to) -> None:
        self._from = _from
        self._to = _to

class Idle(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, display, object, event):
        # print("waiting for your command...")
        return super().update(display, object, event)
    
class Walk(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, display, object, event):
        # print("Moving")
        return super().update(display, object, event)
    
class Fight(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, display, object, event):
        # print("Attacking")
        return super().update(display, object, event)
    
class Damaged(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, display, object, event):
        # print("Taking damage")
        return super().update(display, object, event)
    
class LeftLeg(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, display, object, event):
        # print("Left leg")
        return super().update(display, object, event)
    
class RightLeg(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, display, object, event):
        # print("Right leg")
        return super().update(display, object, event)

class FSM:
    def __init__(self, states: list[State], transitions: dict[Transition]) -> None:
        self._states = states
        self._transitions = transitions
        self.current_state: State = self._states[0]
        self.end: State = self._states[-1]

    def update(self, display, event, object):
        if event:
            trans = self._transitions.get(event)
            if trans and trans._from == self.current_state:
                #self.current_state.exit()
                self.current_state = trans._to
                #self.current_state.enter()
        return self.current_state.update(display, object, event)

        #if self.current_state == self.end:
        #    self.current_state.exit()
        #    return False
        #return True 