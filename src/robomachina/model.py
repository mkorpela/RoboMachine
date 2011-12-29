class RoboMachina(object):

    def __init__(self, states, variables):
        self.states = states or []
        self.variables = variables or []
        for state in self.states:
            state.set_machine(self)

    @property
    def start_state(self):
        return self.states[0]

    def find_state_by_name(self, name):
        for state in self.states:
            if state.name == name:
                return state
        return None

    def write_variable_setter(self, output):
        output.write('Set Machina Variables\n')
        output.write('  [Arguments]  %s\n' % '  '.join(variable.name for variable in self.variables))
        for variable in self.variables:
            output.write('  Set Test Variable  \\%s\n' % variable.name)


class State(object):

    def __init__(self, name, steps, actions):
        self.name = name
        self.steps = steps or []
        self.actions = actions or []

    def set_machine(self, machine):
        for action in self.actions:
            action.set_machine(machine)

    def write_steps_to(self, output):
        for step in self.steps:
            output.write(step+'\n')


class Action(object):

    def __init__(self, name, next_state, condition):
        self.name = name
        self._next_state_name = next_state
        self.condition = condition

    def set_machine(self, machine):
        self._machine = machine

    @property
    def next_state(self):
        return self._machine.find_state_by_name(self._next_state_name)

    def write_to(self, output):
        output.write('  %s\n' % self.name)
        self.next_state.write_steps_to(output)

class Variable(object):

    def __init__(self, name, values):
        self.name = name
        self.values = values
