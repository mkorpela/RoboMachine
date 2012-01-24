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
import random


class _Strategy(object):

    def __init__(self, machine, max_actions, to_state=None):
        self._machine = machine
        self._max_actions = max_actions
        self._to_state = to_state
        assert not to_state or self._machine.find_state_by_name(to_state)

    def _matching_to_state(self, test):
        return not self._to_state or self._to_state == test[-1].next_state.name


class DepthFirstSearchStrategy(_Strategy):

    def tests(self):
        for values in self._variable_value_sets(self._machine.variables):
            self._machine.apply_variable_values(values)
            for test in self._generate_all_from(self._machine.start_state, self._max_actions):
                yield test, [v.current_value for v in self._machine.variables]

    def _variable_value_sets(self, variables):
            if not variables:
                return ([],)
            return (vs for vs in self._var_set(variables) if self._machine.rules_are_ok(vs))

    def _var_set(self, vars):
        if not vars:
            return [[]]
        return ([val]+sub_set for val in vars[0].values for sub_set in self._var_set(vars[1:]))

    def _generate_all_from(self, state, max_actions):
        if not state.actions or max_actions == 0:
            if self._to_state and self._to_state != state.name:
                return
            yield []
        else:
            at_least_one_generated = False
            for action in state.actions:
                for test in self._generate_all_from(action.next_state, max_actions-1):
                    at_least_one_generated = True
                    yield [action]+test
            if not at_least_one_generated and self._to_state == state.name:
                yield []


class RandomStrategy(_Strategy):

    def tests(self):
        while True:
            test = []
            values = self._generate_variable_values()
            self._machine.apply_variable_values(values)
            current_state = self._machine.start_state
            while self._max_actions > len(test) and current_state.actions:
                action = random.choice(current_state.actions)
                current_state = action.next_state
                test.append(action)
            while test and not self._matching_to_state(test):
                test.pop()
            if not test and self._to_state and self._to_state != self._machine.start_state.name:
                continue
            yield test, [v.current_value for v in self._machine.variables]

    def _generate_variable_values(self):
        while True:
            candidate = [random.choice(v.values) for v in self._machine.variables]
            if self._machine.rules_are_ok(candidate):
                return candidate
