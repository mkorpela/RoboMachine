
def transform(machina):
    pass

def parse(text):
    machine = RoboMachina()
    current_state = None
    for line in text.splitlines():
        if line == '*** Machine ***':
            continue
        if len(line) and line[0] != ' ':
            current_state = machine.add_state(line.strip())
            continue
        if line.startswith('    ') and line.strip():
            current_state.add_action(line.split('==>')[0].strip())
            continue
        if line == '  [Actions]':
            continue
        if line.startswith('  ') and line.strip():
            current_state.add_step(line)
    return machine


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
