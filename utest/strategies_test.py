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
from robomachine.model import RoboMachina, State, Action
from robomachine.strategies import DepthFirstSearchStrategy, RandomStrategy


class StrategyTestCase(object):

    def test_can_generate_test_from_simple_machine(self):
        action12 = Action('to state2', 'state2', None)
        action21 = Action('to state1', 'state1', None)
        states = [State('state1', [], [action12]),
                  State('state2', [], [action21])]
        at_least_one_test_generated = False
        for test in self.strategy_class(RoboMachina(states, [], []), 2).tests():
            self.assertEqual(([action12, action21], ()), test)
            at_least_one_test_generated = True
            break
        self.assertTrue(at_least_one_test_generated)


class DepthFirstSearchStrategyTestCase(StrategyTestCase, unittest.TestCase):
    strategy_class = DepthFirstSearchStrategy

class RandomStrategyTestCase(StrategyTestCase, unittest.TestCase):
    strategy_class = RandomStrategy

if __name__ == '__main__':
    unittest.main()
