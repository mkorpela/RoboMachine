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
from robomachine.model import RoboMachine, Variable


class MachinaModelTestCase(unittest.TestCase):

    def test_empty_machina_model(self):
        empty_machina = RoboMachine(None, None, None)
        self.assertEqual([], empty_machina.states)
        self.assertEqual([], empty_machina.variables)
        self.assertEqual(None, empty_machina.find_state_by_name('some name'))

    def test_variable_model(self):
        var_model = Variable('name', ['1', '2'])
        self.assertEqual('name', var_model.name)
        self.assertEqual(['1', '2'], var_model.values)

    def test_variable_current_value(self):
        var_model = Variable('foo', ['bar', 'zoo'])
        try:
            var_model.current_value
            self.fail('should throw assertion error as no current value has been set')
        except AssertionError:
            pass
        var_model.set_current_value('bar')
        self.assertEqual('bar', var_model.current_value)

if __name__ == '__main__':
    unittest.main()
