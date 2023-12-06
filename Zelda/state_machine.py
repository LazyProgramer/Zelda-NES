import pygame

class State:
    def __init__(self, name) -> None:
        self.name = name

    def update(self, object, event):
        return object.update(event)

class Transition:
    def __init__(self, _from, _to) -> None:
        self._from = _from
        self._to = _to

class Idle(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object, event):
        return super().update(object, event)
    
class Walk(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object, event):
        # print("Moving")
        return super().update(object, event)
    
class Fight(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object, event):
        # print("Attacking")
        return super().update(object, event)
    
class Damaged(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self, object, event):
        # print("Taking damage")
        return super().update(object, event)
    

class FSM:
    def __init__(self, states: list[State], transitions: dict[Transition]) -> None:
        self._states = states
        self._transitions = transitions
        self.current_state: State = self._states[0]

    def update(self, event, object):
        if event:
            trans = self._transitions.get(event)
            if trans and trans._from == self.current_state:
                self.current_state = trans._to
        return self.current_state.update(object, event)