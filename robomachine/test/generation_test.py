#  Copyright (c) 2011-2012 Mikko Korpela
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
#  ------------------------------------------------------------------------
#  Copyright 2017 David Kaplan
#
#  Changes:
#  - Python 3 support

try:
    from StringIO import StringIO
except:
    from io import StringIO

import unittest
from robomachine.model import RoboMachine, State, Action
import robomachine


class GenerationTestCase(unittest.TestCase):

    def test_generation_with_no_tests(self):
        mock_machine = RoboMachine(states=[], variables=[], rules=[])
        output = StringIO()
        robomachine.generate(machine=mock_machine, output=output, strategy=_MockStrategyWithNoTests)
        self.assertTrue(output.getvalue().startswith('*** Test Cases ***\n*** Keywords ***'))

    def test_generation_with_a_test_limit(self):
        mock_machine = RoboMachine(states=[State('bar', [], [])], variables=[], rules=[])
        output = StringIO()
        robomachine.generate(machine=mock_machine, max_tests=10, output=output, strategy=_MockStrategyWithHundredTests)
        self.assertEqual(10, sum(1 for line in output.getvalue().splitlines() if line.startswith('Test ')))

    def test_generation_with_same_generated_tests(self):
        mock_machine = RoboMachine(states=[State('bar', [], [])], variables=[], rules=[])
        output = StringIO()
        robomachine.generate(machine=mock_machine, max_tests=1000, output=output, strategy=_MockStrategyWithSameTests)
        self.assertEqual(1, sum(1 for line in output.getvalue().splitlines() if line.startswith('Test ')))


class _MockStrategy(object):

    def __init__(self, machine, *others):
        self._machine = machine

    def _action(self):
        a = Action('foo', 'bar')
        a.set_machine(self._machine)
        return a

    def _visited_actions(self):
        pass

    def _visited_states(self):
        pass


class _MockStrategyWithNoTests(_MockStrategy):

    def tests(self):
        return []


class _MockStrategyWithHundredTests(_MockStrategy):

    def tests(self):
        return [([self._action()], []) for i in range(100)]


class _MockStrategyWithSameTests(_MockStrategy):

    def tests(self):
        test = ([self._action()], [])
        while True:
            yield test


if __name__ == '__main__':
    unittest.main()
