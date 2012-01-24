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
import re


class RoboMachine(object):

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
        for variable in self.variables:
            variable.set_machine(self)

    @property
    def start_state(self):
        return self.states[0]

    @property
    def variable_value_mapping(self):
        return dict((v.name, v.current_value) for v in self.variables)

    def find_state_by_name(self, name):
        for state in self.states:
            if state.name == name:
                return state
        return None

    def find_variable_by_name(self, name):
        for variable in self.variables:
            if variable.name == name:
                return variable
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
        if not self._keywords_table:
            output.write('\n*** Keywords ***\n')
        if self.variables:
            self.write_variable_setter(output)
        for state in self.states:
            if state.steps:
                output.write(state.name+'\n')
                state.write_steps_to(output)

    def write_variable_setter(self, output):
        output.write('Set Machine Variables\n')
        output.write('  [Arguments]  %s\n' % '  '.join(variable.name for variable in self.variables))
        for variable in self.variables:
            output.write('  Set Test Variable  \\%s\n' % variable.name)

    def write_variable_setting_step(self, values, output):
        output.write('  Set Machine Variables  %s\n' % '  '.join(values))

    def rules_are_ok(self, values):
        value_mapping = dict((v.name, value) for v, value in zip(self.variables, values))
        for rule in self.rules:
            if not rule.is_valid(value_mapping=value_mapping):
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

    def write_to(self, output):
        if self.steps:
            output.write('  %s\n' % self.name)


class Action(object):

    def __init__(self, name, next_state, condition=None):
        self.name = name
        self._next_state_name = next_state
        self.condition = condition

    def set_machine(self, machine):
        self._machine = machine
        if not self.next_state:
            raise AssertionError('Invalid end state "%s" in '\
                                 'action "%s"!' %
                                 (self._next_state_name, self.name))

    @property
    def next_state(self):
        return self._machine.find_state_by_name(self._next_state_name)

    def is_available(self):
        if not self.condition:
            return True
        if self.condition == 'otherwise':
            return True
        return self.condition.is_valid(value_mapping=self._machine.variable_value_mapping)

    def write_to(self, output):
        if self.name:
            output.write('  %s\n' % self.name)
        self.next_state.write_to(output)

class Variable(object):
    REGEX = r'\$\{[_A-Z][_A-Z0-9]*\}'
    PATTERN = re.compile(REGEX)
    _NO_VALUE = object()

    def __init__(self, name, values):
        self.name = name
        self.values = values
        self._current_value = Variable._NO_VALUE

    def set_machine(self, machine):
        self._machine = machine

    def set_current_value(self, value):
        self._current_value = value

    @property
    def current_value(self):
        if self._current_value is Variable._NO_VALUE:
            raise AssertionError('No current value set')
        return self._resolve_value(self._current_value)

    def _resolve_value(self, value):
        return self.PATTERN.sub(self._resolve_variable, value)

    def _resolve_variable(self, var_match):
        var = self._machine.find_variable_by_name(var_match.group(0))
        if not var:
            return var_match.group(0)
        return var.current_value
