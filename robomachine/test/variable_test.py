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
from robomachine import parsing
import robomachine
import pyparsing

class VariableParsingTestCases(unittest.TestCase):

    def test_variable_parsing(self):
        self._parse_var('${VARIABLE}')
        self._parse_var('${VAR2}')
        self._parse_var('${_VAR_WITH_UNDERSCORE}')
        self._invalid_var('')
        self._invalid_var('${foo}')
        self._invalid_var('${1}')
        self._invalid_var('${2FOO}')
        self._invalid_var('${FOO BAR}')

    def _parse_var(self, var_name):
        self.assertEqual(var_name, parsing.variable.parseString(var_name)[0])

    def _invalid_var(self, var_name):
        try:
            parsing.variable.parseString(var_name)
            self.fail('Should not parse invalid variable name "%s"' % var_name)
        except pyparsing.ParseException, e:
            pass

    def test_variable_definition_parsing(self):
        v = parsing.variable_definition.parseString('${ABC123}  any of  one  two  123\n')[0]
        self.assertEqual('${ABC123}', v.name)
        self.assertEqual(['one', 'two', '123'], v.values)

    def test_variable_definition_parsing_when_more_than_two_spaces(self):
        v = parsing.variable_definition.parseString('${ABC123}          any of           one   two  123\n')[0]
        self.assertEqual('${ABC123}', v.name)
        self.assertEqual(['one', 'two', '123'], v.values)


class ConditionActionParsingTestCases(unittest.TestCase):

    def test_conditional_action_parsing(self):
        a = parsing.action.parseString('    My Action  ==>  End Step  when  ${FOO} == bar\n')[0]
        self.assertEqual('My Action', a.name)
        self.assertEqual('End Step', a._next_state_name)
        self.assertEqual('${FOO} == bar', str(a.condition))

    def test_multiconditional_action_parsing(self):
        a = parsing.action.parseString('    My Action  ==>  End Step  when  ${BAR} == a  and  ${FOO} == cee\n')[0]
        self.assertEqual('My Action', a.name)
        self.assertEqual('End Step', a._next_state_name)
        self.assertEqual('${BAR} == a  and  ${FOO} == cee', str(a.condition))

    def test_otherwise_conditional_action_parsing(self):
        a = parsing.action.parseString('    My Action  ==>  End Step  otherwise\n')[0]
        self.assertEqual('My Action', a.name)
        self.assertEqual('End Step', a._next_state_name)
        self.assertEqual('otherwise', a.condition)


class RuleParsingTestCases(unittest.TestCase):

    def test_equivalence_rule_parsing(self):
        rule = parsing.rule.parseString('${USERNAME} == ${VALID_PASSWORD}  <==>  ${PASSWORD} == ${VALID_USERNAME}\n')[0]
        self.assertEqual('${USERNAME} == ${VALID_PASSWORD}  <==>  ${PASSWORD} == ${VALID_USERNAME}', str(rule))
        value_mapping = {'${USERNAME}':'${VALID_PASSWORD}',
                         '${PASSWORD}':'${VALID_USERNAME}'}
        self.assertTrue(rule.is_valid(value_mapping=value_mapping))
        value_mapping['${USERNAME}']='something else'
        self.assertFalse(rule.is_valid(value_mapping=value_mapping))
        value_mapping['${USERNAME}']='${VALID_PASSWORD}'
        value_mapping['${PASSWORD}']='something'
        self.assertFalse(rule.is_valid(value_mapping=value_mapping))
        value_mapping['${USERNAME}']='not valid'
        value_mapping['${PASSWORD}']='nothis validus'
        self.assertTrue(rule.is_valid(value_mapping=value_mapping))

    def test_implication_rule_parsing(self):
        rule = parsing.rule.parseString('${VARIABLE} != value  ==>  ${OTHER} == other')[0]
        self.assertEqual('not (${VARIABLE} == value)  ==>  ${OTHER} == other', str(rule))

    def test_condition_parsing(self):
        rule = parsing.rule.parseString('${VARIABLE} == value')[0]
        self.assertEqual('${VARIABLE} == value', str(rule))

    def test_and_rule_parsing(self):
        rule = parsing.rule.parseString('${VARIABLE} == value  and  ${VAR2} == baluu')[0]
        self.assertEqual('${VARIABLE} == value  and  ${VAR2} == baluu', str(rule))

    def test_or_rule_parsing(self):
        rule = parsing.rule.parseString('${VARIABLE} == value  or  ${VAR2} == baluu')[0]
        self.assertEqual('${VARIABLE} == value  or  ${VAR2} == baluu', str(rule))

    def test_not_rule_parsing(self):
        rule = parsing.rule.parseString('not (${VAR2} == baluu)')[0]
        self.assertEqual('not (${VAR2} == baluu)', str(rule))

    def test_complex(self):
        rule = parsing.rule.parseString('${FOO} == bar  or  (not (${BAR} == foo  and  ${ZOO} == fii))')[0]
        self.assertEqual('${FOO} == bar  or  not (${BAR} == foo  and  ${ZOO} == fii)', str(rule))


_LOGIN_MACHINE = """\
*** Machine ***
${USERNAME}  any of  demo  mode  invalid  ${EMPTY}
${PASSWORD}  any of  mode  demo  invalid  ${EMPTY}

${USERNAME} == mode  <==>  ${PASSWORD} == demo

Login Page
  Title Should Be  Login Page
  [Actions]
    Submit Credentials  ==>  Welcome Page  when  ${USERNAME} == demo  and  ${PASSWORD} == mode
    Submit Credentials  ==>  Error Page  otherwise

Welcome Page
  Title Should Be  Welcome Page

Error Page
  Title Should Be  Error Page
"""

_LOGIN_TESTS_GENERATE_ALL_DFS = """\
*** Test Cases ***
Test 1
  Set Machine Variables  demo  mode
  Login Page
  Submit Credentials
  Welcome Page

Test 2
  Set Machine Variables  demo  invalid
  Login Page
  Submit Credentials
  Error Page

Test 3
  Set Machine Variables  demo  ${EMPTY}
  Login Page
  Submit Credentials
  Error Page

Test 4
  Set Machine Variables  mode  demo
  Login Page
  Submit Credentials
  Error Page

Test 5
  Set Machine Variables  invalid  mode
  Login Page
  Submit Credentials
  Error Page

Test 6
  Set Machine Variables  invalid  invalid
  Login Page
  Submit Credentials
  Error Page

Test 7
  Set Machine Variables  invalid  ${EMPTY}
  Login Page
  Submit Credentials
  Error Page

Test 8
  Set Machine Variables  ${EMPTY}  mode
  Login Page
  Submit Credentials
  Error Page

Test 9
  Set Machine Variables  ${EMPTY}  invalid
  Login Page
  Submit Credentials
  Error Page

Test 10
  Set Machine Variables  ${EMPTY}  ${EMPTY}
  Login Page
  Submit Credentials
  Error Page

*** Keywords ***
Set Machine Variables
  [Arguments]  ${USERNAME}  ${PASSWORD}
  Set Test Variable  \${USERNAME}
  Set Test Variable  \${PASSWORD}
Login Page
  Title Should Be  Login Page
Welcome Page
  Title Should Be  Welcome Page
Error Page
  Title Should Be  Error Page
"""


class VariableMachineParsingTestCases(unittest.TestCase):

    def test_machine_parsing(self):
        m = parsing.parse(_LOGIN_MACHINE)
        self.assertEqual('${USERNAME}', m.variables[0].name)
        self.assertEqual('${PASSWORD}', m.variables[1].name)
        self.assertEqual(2, len(m.variables))
        m.apply_variable_values(['demo', 'mode'])
        self.assertEqual('${USERNAME} == demo  and  ${PASSWORD} == mode', str(m.states[0].actions[0].condition))
        self.assertEqual('Welcome Page', m.states[0].actions[0].next_state.name)
        m.apply_variable_values(['invalid', 'invalid'])
        self.assertEqual('otherwise', m.states[0].actions[0].condition)
        self.assertEqual('Error Page', m.states[0].actions[0].next_state.name)


class TestGenerationTestCases(unittest.TestCase):

    def test_generate_all_dfs(self):
        m = parsing.parse(_LOGIN_MACHINE)
        out = StringIO()
        robomachine.generate(m, output=out)
        self.assertEqual(_LOGIN_TESTS_GENERATE_ALL_DFS, out.getvalue())

if __name__ == '__main__':
    unittest.main()
