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

    def __init__(self, states, variables, rules, settings_table=None,
                 variables_table=None, keywords_table=None):
        self.states = states or []
        self.variables = variables or []
        self.rules = rules or []
        self._settings_table = settings_table or []
        self._variables_table = variables_table or []
        self._keywords_table = keywords_table or []
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

    def write_settings_table(self, output):
        for content in self._settings_table:
            output.write(content)

    def write_variables_table(self, output):
        for content in self._variables_table:
            output.write(content)

    def write_keywords_table(self, output):
        for content in self._keywords_table:
            output.write('\n'+content)
        if self.variables:
            if not self._keywords_table:
                output.write('\n*** Keywords ***\n')
            self.write_variable_setter(output)

    def write_variable_setter(self, output):
        output.write('Set Machine Variables\n')
        output.write('  [Arguments]  %s\n' % '  '.join(variable.name for variable in self.variables))
        for variable in self.variables:
            output.write('  Set Test Variable  \\%s\n' % variable.name)

    def write_variable_setting_step(self, values, output):
        output.write('  Set Machine Variables  %s\n' % '  '.join(values))

    def rules_are_ok(self, values):
        for rule in self.rules:
            for variable, value in zip(self.variables, values):
                rule.set_variable(variable.name, value)
            if not rule.is_valid():
                return False
        return True

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
            cond.set_variable(variable.name, variable.current_value)
        return cond.is_valid()

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

class EquivalenceRule(object):

    def __init__(self, condition1, condition2):
        self._condition1 = condition1
        self._condition2 = condition2
        self._values = {}

    @property
    def text(self):
        return '%s  <==>  %s' % (self._condition1, self._condition2)

    def set_variable(self, name, value):
        self._values[name] = value

    def is_valid(self):
        return self._condition1.is_valid(self._values) == self._condition2.is_valid(self._values)


class AndRule(object):

    def __init__(self, conditions):
        self._conditions = conditions
        self._values = {}

    def __str__(self):
        return '  and  '.join(str(c) for c in self._conditions)

    def set_variable(self, name, value):
        self._values[name] = value

    def is_valid(self):
        return not(any(not(c.is_valid(self._values)) for c in self._conditions))


class Condition(object):

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()
        self._values = {}

    def __str__(self):
        return '%s == %s' % (self._name, self._value)

    def is_valid(self, value_mapping=None):
        value_mapping = value_mapping or self._values
        return value_mapping[self._name].strip() == self._value.strip()

    def set_variable(self, name, value):
        self._values[name] = value
