#  Copyright 2011-2012 Mikko Korpela
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

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

    def write_variable_setting_step(self, values, output):
        output.write('  Set Machina Variables  %s\n' % '  '.join(values))

    def variable_value_sets(self):
        if not self.variables:
            return ((),)
        tail_values = [v.values for v in self.variables[1:]]
        head_values = [[value] for value in self.variables[0].values]
        while tail_values:
            next_values = tail_values[0]
            tail_values = tail_values[1:]
            head_values = [h+[n] for h in head_values for n in next_values]
        return head_values

    def apply_variable_values(self, values):
        for variable, value in zip(self.variables, values):
            variable.set_current_value(value)


class State(object):

    def __init__(self, name, steps, actions):
        self.name = name
        self.steps = steps or []
        self._actions = actions or []

    @property
    def actions(self):
        result = []
        names = set()
        for action in self._actions:
            if action.is_available() and action.name not in names:
                result.append(action)
                names.add(action.name)
        return result

    def set_machine(self, machine):
        for action in self._actions:
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

    def is_available(self):
        if not self.condition:
            return True
        if self.condition == 'otherwise':
            return True
        cond = self.condition
        for variable in self._machine.variables:
            cond = cond.replace(variable.name, variable.current_value)
        cond = cond.split(' and ')
        for first, second in [c.split(' == ') for c in cond]:
            if first != second:
                return False
        return True

    def write_to(self, output):
        output.write('  %s\n' % self.name)
        self.next_state.write_steps_to(output)

class Variable(object):
    _NO_VALUE = object()

    def __init__(self, name, values):
        self.name = name
        self.values = values
        self._current_value = Variable._NO_VALUE

    def set_current_value(self, value):
        self._current_value = value

    @property
    def current_value(self):
        if self._current_value is Variable._NO_VALUE:
            raise AssertionError('No current value set')
        return self._current_value
