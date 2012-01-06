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
from robomachine.strategies import DepthFirstSearch


class DepthFirstSearchStrategyTestCase(unittest.TestCase):

    def test_can_generate_test_from_simple_machine(self):
        action12 = Action('to state2', 'state2', None)
        action21 = Action('to state1', 'state1', None)
        states = [State('state1', [], [action12]),
                  State('state2', [], [action21])]
        tests = list(DepthFirstSearch(RoboMachina(states, [], []), 2).tests())
        self.assertEqual(1, len(tests))
        self.assertEqual(([action12, action21], ()), tests[0])

if __name__ == '__main__':
    unittest.main()
