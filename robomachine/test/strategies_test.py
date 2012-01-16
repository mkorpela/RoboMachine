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

import unittest
from robomachine.model import RoboMachine, State, Action, Variable
from robomachine.rules import Condition
from robomachine.strategies import DepthFirstSearchStrategy, RandomStrategy


class StrategyTestCase(object):

    def test_can_generate_test_from_simple_machine(self):
        action12 = Action('to state2', 'state2')
        action21 = Action('to state1', 'state1')
        states = [State('state1', [], [action12]),
                  State('state2', [], [action21])]
        at_least_one_test_generated = False
        for test in self.strategy_class(RoboMachine(states, [], []), 2).tests():
            self.assertEqual(([action12, action21], []), test)
            at_least_one_test_generated = True
            break
        self.assertTrue(at_least_one_test_generated)

    def test_can_generate_test_from_variable_machine(self):
        variables = [Variable('var', ['a', 'b', 'c'])]
        at_least_one_test_generated = False
        for test in self.strategy_class(RoboMachine([State('state', [], [])], variables, []), 0).tests():
            self.assertEqual([], test[0])
            self.assertEqual(1, len(test[1]))
            self.assertTrue(test[1][0] in ['a', 'b', 'c'])
            at_least_one_test_generated = True
            break
        self.assertTrue(at_least_one_test_generated)

    def test_obeys_rules(self):
        variables = [Variable('${VAR}', ['a', 'b', 'c', 'd', 'e', 'f', 'g'])]
        rules = [Condition('${VAR}', 'e')]
        at_least_one_test_generated = False
        for test in self.strategy_class(RoboMachine([State('state', [], [])], variables, rules), 0).tests():
            self.assertEqual([], test[0])
            self.assertEqual(1, len(test[1]))
            self.assertEqual('e', test[1][0])
            at_least_one_test_generated = True
            break
        self.assertTrue(at_least_one_test_generated)

    def test_obeys_to_state(self):
        a12 = Action('s1->s2', 's2')
        a21 = Action('s2->s1', 's1')
        a23 = Action('s2->s3', 's3')
        a31 = Action('s3->s1', 's1')
        states = [State('s1', [], [a12]),
                  State('s2', [], [a21, a23]),
                  State('s3', [], [a31])]
        tests_to_generate = 5
        for test in self.strategy_class(RoboMachine(states, [], []), 17, 's3').tests():
            self.assertEqual(states[-1].name, test[0][-1].next_state.name)
            tests_to_generate -= 1
            if tests_to_generate == 0:
                break
        self.assertEqual(0, tests_to_generate)

    def test_obeys_to_state_circular(self):
        a12 = Action('a12', 's2')
        a23 = Action('a23', 's3')
        a31 = Action('a31', 's1')
        states = [State('s1', [], [a12]),
                  State('s2', [], [a23]),
                  State('s3', [], [a31])]
        at_least_one_test_generated = False
        for test in self.strategy_class(RoboMachine(states, [], []), 4, 's3').tests():
            self.assertEqual(states[-1].name, test[0][-1].next_state.name)
            at_least_one_test_generated = True
            break
        self.assertTrue(at_least_one_test_generated)

    def test_to_state_is_start_state(self):
        at_least_one_test_generated = False
        for test in self.strategy_class(RoboMachine([State('s1', [], [])], [], []), 4, 's1').tests():
            self.assertEqual(([], []), test)
            at_least_one_test_generated = True
            break
        self.assertTrue(at_least_one_test_generated)


class DepthFirstSearchStrategyTestCase(StrategyTestCase, unittest.TestCase):
    strategy_class = DepthFirstSearchStrategy

class RandomStrategyTestCase(StrategyTestCase, unittest.TestCase):
    strategy_class = RandomStrategy

if __name__ == '__main__':
    unittest.main()
