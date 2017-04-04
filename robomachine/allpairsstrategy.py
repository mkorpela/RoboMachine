#  Copyright 2012 Mikko Korpela
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

from allpairspy import AllPairs
from robomachine.strategies import RandomStrategy


class AllPairsRandomStrategy(RandomStrategy):

    def __init__(self, machine, max_actions, to_state=None):
        if machine.rules:
            raise AssertionError('ERROR! AllPairs does not work correctly with rules')
        RandomStrategy.__init__(self, machine, max_actions, to_state)

    def tests(self):
        for values in self._generate_all_pairs_variable_values():
            test = self._generate_test(values)
            if not test and self._to_state and self._to_state != self._machine.start_state.name:
                continue
            yield test, [v.current_value for v in self._machine.variables]

    def _generate_all_pairs_variable_values(self):
        if len(list(self._machine.variables)) < 2:
            for var in self._machine.variables:
                return [v for v in var.values]
            return [[]]
        return AllPairs([v.values for v in self._machine.variables])
