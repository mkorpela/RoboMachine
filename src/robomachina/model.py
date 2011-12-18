class RoboMachina(object):

    def __init__(self, states):
        self.states = states or []


class State(object):

    def __init__(self, name, steps, actions):
        self.name = name
        self.steps = steps or []
        self.actions = actions or []


class Action(object):

    def __init__(self, name, next_state):
        self.name = name
        self.next_state = next_state
