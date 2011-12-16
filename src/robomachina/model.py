class RoboMachina(object):

    def __init__(self):
        self._states = []

    def add_state(self, name):
        state = State(name)
        self._states += [state]
        return state

    @property
    def states(self):
        return self._states


class State(object):

    def __init__(self, name):
        self.name = name
        self.actions = []
        self.steps = []

    def add_action(self, name):
        self.actions += [Action(name)]

    def add_step(self, step):
        self.steps += [step]


class Action(object):

    def __init__(self, name):
        self.name = name
