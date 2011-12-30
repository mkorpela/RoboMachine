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

from StringIO import StringIO
import unittest
from robomachina import parsing
import robomachina


class VariableParsingTestCases(unittest.TestCase):

    def test_variable_parsing(self):
        v = parsing.variable.parseString('${variable}')
        self.assertEqual('${variable}', v[0])

    def test_variable_definition_parsing(self):
        v = parsing.variable_definition.parseString('${abc123}  any of  one  two  123\n')[0]
        self.assertEqual('${abc123}', v.name)
        self.assertEqual(['one', 'two', '123'], v.values)


class ConditionActionParsingTestCases(unittest.TestCase):

    def test_conditional_action_parsing(self):
        a = parsing.action.parseString('    My Action  ==>  End Step  when  ${FOO} == bar\n')[0]
        self.assertEqual('My Action', a.name)
        self.assertEqual('End Step', a._next_state_name)
        self.assertEqual('${FOO} == bar', a.condition)

    def test_multiconditional_action_parsing(self):
        a = parsing.action.parseString('    My Action  ==>  End Step  when  ${BAR} == a and ${FOO} == cee\n')[0]
        self.assertEqual('My Action', a.name)
        self.assertEqual('End Step', a._next_state_name)
        self.assertEqual('${BAR} == a and ${FOO} == cee', a.condition)

    def test_otherwise_conditional_action_parsing(self):
        a = parsing.action.parseString('    My Action  ==>  End Step  otherwise\n')[0]
        self.assertEqual('My Action', a.name)
        self.assertEqual('End Step', a._next_state_name)
        self.assertEqual('otherwise', a.condition)

_LOGIN_MACHINE = """\
*** Machine ***
${USERNAME}  any of  demo  mode  invalid  ${EMPTY}
${PASSWORD}  any of  mode  demo  invalid  ${EMPTY}
Login Page
  Title Should Be  Login Page
  [Actions]
    Submit Credentials  ==>  Welcome Page  when  ${USERNAME} == demo and ${PASSWORD} == mode
    Submit Credentials  ==>  Error Page  otherwise

Welcome Page
  Title Should Be  Welcome Page

Error Page
  Title Should Be  Error Page
"""

_LOGIN_TESTS_GENERATE_ALL_DFS = """\
*** Test Cases ***
Test 1
  Set Machina Variables  demo  mode
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Welcome Page

Test 2
  Set Machina Variables  demo  demo
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Error Page

Test 3
  Set Machina Variables  demo  invalid
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Error Page

Test 4
  Set Machina Variables  demo  ${EMPTY}
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Error Page

Test 5
  Set Machina Variables  mode  mode
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Error Page

Test 6
  Set Machina Variables  mode  demo
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Error Page

Test 7
  Set Machina Variables  mode  invalid
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Error Page

Test 8
  Set Machina Variables  mode  ${EMPTY}
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Error Page

Test 9
  Set Machina Variables  invalid  mode
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Error Page

Test 10
  Set Machina Variables  invalid  demo
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Error Page

Test 11
  Set Machina Variables  invalid  invalid
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Error Page

Test 12
  Set Machina Variables  invalid  ${EMPTY}
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Error Page

Test 13
  Set Machina Variables  ${EMPTY}  mode
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Error Page

Test 14
  Set Machina Variables  ${EMPTY}  demo
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Error Page

Test 15
  Set Machina Variables  ${EMPTY}  invalid
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Error Page

Test 16
  Set Machina Variables  ${EMPTY}  ${EMPTY}
  Title Should Be  Login Page
  Submit Credentials
  Title Should Be  Error Page

*** Keywords ***
Set Machina Variables
  [Arguments]  ${USERNAME}  ${PASSWORD}
  Set Test Variable  \${USERNAME}
  Set Test Variable  \${PASSWORD}
"""


class VariableMachineParsingTestCases(unittest.TestCase):

    def test_machine_parsing(self):
        m = parsing.parse(_LOGIN_MACHINE)
        self.assertEqual('${USERNAME}', m.variables[0].name)
        self.assertEqual('${PASSWORD}', m.variables[1].name)
        self.assertEqual(2, len(m.variables))
        m.apply_variable_values(['demo', 'mode'])
        self.assertEqual('${USERNAME} == demo and ${PASSWORD} == mode', m.states[0].actions[0].condition)
        self.assertEqual('Welcome Page', m.states[0].actions[0].next_state.name)
        m.apply_variable_values(['invalid', 'invalid'])
        self.assertEqual('otherwise', m.states[0].actions[0].condition)
        self.assertEqual('Error Page', m.states[0].actions[0].next_state.name)


class TestGenerationTestCases(unittest.TestCase):

    def test_generate_all_dfs(self):
        m = parsing.parse(_LOGIN_MACHINE)
        out = StringIO()
        robomachina.generate_all_dfs(m, output=out)
        self.assertEqual(out.getvalue(), _LOGIN_TESTS_GENERATE_ALL_DFS)

if __name__ == '__main__':
    unittest.main()
