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
from robomachine.parsing import comment, RoboMachineParsingException
from robomachine.strategies import RandomStrategy


_MACHINA = """\
*** Settings ***
Default Tags  foo

*** Variables ***
${BAR}  zoo

*** Machine ***
Start State
  Log  In Start State
  [Actions]
    Some keyword  ==>  End State

End State
  Log  In End State

*** Keywords ***
Some keyword
  No Operation
"""

_TESTS = """\
*** Settings ***
Default Tags  foo

*** Variables ***
${BAR}  zoo

*** Test Cases ***
Test 1
  Start State
  Some keyword
  End State

*** Keywords ***

Some keyword
  No Operation
Start State
  Log  In Start State
End State
  Log  In End State
"""

class TestRoboMachina(unittest.TestCase):

    def test_transform_to_robot_test_cases(self):
        tests = robomachine.transform(_MACHINA)
        self.assertEqual(_TESTS, tests)

    def test_parse_machina_state_names(self):
        m = robomachine.parse(_MACHINA)
        self.assertEqual(['Start State', 'End State'], [s.name for s in m.states])

    def test_parse_machina_state_actions(self):
        m = robomachine.parse(_MACHINA)
        self.assertEqual(['Some keyword'], [a.name for a in m.states[0].actions])
        self.assertEqual([], [a.name for a in m.states[1].actions])

    def test_parse_machina_state_steps(self):
        m = robomachine.parse(_MACHINA)
        self.assertEqual(['  Log  In Start State'], m.states[0].steps)
        self.assertEqual(['  Log  In End State'], m.states[1].steps)


_MACHINA2 = """\
*** Machine ***
A
  Foo  bar
  Bar  foo
  [Actions]
    first  ==>  B
    second  ==>  C
    ==>  D

B
  [Actions]
    something else  ==>  A  # This is also a comment
    other thing     ==>  C

C
  No Operation  #This is a comment

D
  Log  tau action can only get here
"""

_TESTS2_GENERATE_ALL_DFS_MAX_ACTIONS_2 = """\
*** Test Cases ***
Test 1
  A
  first
  something else
  A

Test 2
  A
  first
  other thing
  C

Test 3
  A
  second
  C

Test 4
  A
  D

*** Keywords ***
A
  Foo  bar
  Bar  foo
C
  No Operation  #This is a comment
D
  Log  tau action can only get here
"""

_INVALID_STATE_MACHINE = """\
*** Machine ***
State 1
  [Actions]
    ==>  Invalid
"""

class TestParsing(unittest.TestCase):

    def test_header_parsing(self):
        header = parsing.machine_header.parseString('*** Machine ***\n')
        self.assertEqual('*** Machine ***', header[0])

    def test_state_parsing(self):
        state = """\
A
  Foo  bar
  Bar  foo
  [Actions]
    first  ==>  B
    second  ==>  C
"""
        state = parsing.state.parseString(state)[0]
        self.assertEqual('A', state.name)
        self.assertEqual(['  Foo  bar', '  Bar  foo'], state.steps)
        self.assertEqual(['first', 'second'], [a.name for a in state.actions])
        self.assertEqual(['B', 'C'], [a._next_state_name for a in state.actions])

    def test_steps_parsing(self):
        steps = """\
  Foo  bar
  Bar  foo
"""
        steps = parsing.steps.parseString(steps)
        self.assertEqual(['  Foo  bar', '  Bar  foo'], list(steps.steps))

    def test_step_parsing(self):
        self._should_parse_step('  Foo  bar\n')
        self._should_parse_step('  Log  ${value}\n')
        self._should_parse_step('  ${value}=  Set Variable  something\n')
        self._should_parse_step('  Log  [something]\n')

    def test_action_parsing(self):
        action = parsing.action.parseString('    action name  ==>  state')[0]
        self.assertEqual('action name', action.name)
        self.assertEqual('state', action._next_state_name)

    def test_tau_action_parsing(self):
        action = parsing.action.parseString('    ==>  state')[0]
        self.assertEqual('', action.name)
        self.assertEqual('state', action._next_state_name)

    def _should_parse_step(self, step):
        self.assertEqual(step[:-1], parsing.step.parseString(step)[0])

    def test_parsing(self):
        m = robomachine.parse(_MACHINA2)
        self.assertEqual(m.states[0].name, 'A')
        self.assertEqual(m.states[0].steps, ['  Foo  bar', '  Bar  foo'])
        self.assertEqual([a.name for a in m.states[0].actions], ['first', 'second', ''])
        self.assertEqual([a.next_state.name for a in m.states[0].actions], ['B', 'C', 'D'])
        self.assertEqual(m.states[1].name, 'B')
        self.assertEqual(m.states[1].steps, [])
        self.assertEqual([a.name for a in m.states[1].actions], ['something else', 'other thing'])
        self.assertEqual([a.next_state.name for a in m.states[1].actions], ['A', 'C'])
        self.assertEqual(m.states[2].name, 'C')
        self.assertEqual(m.states[2].steps, ['  No Operation  #This is a comment'])
        self.assertEqual(m.states[2].actions, [])

    def test_invalid_state_parsing(self):
        try:
            m = robomachine.parse(_INVALID_STATE_MACHINE)
            self.fail('Should raise exception')
        except RoboMachineParsingException:
            pass


_VAR_PROBLEM_MACHINE = """\
*** Machine ***
${FOO}  any of  bar
${BAR}  any of  ${FOO}

State
  No Operation
  [Actions]
    ==>  End  when  ${BAR} == bar

End
  No Operation
"""

_TEST_VAR_PROBLEM_MACHINE = """\
*** Test Cases ***
Test 1
  Set Machine Variables  bar  bar
  State
  End

*** Keywords ***
Set Machine Variables
  [Arguments]  ${FOO}  ${BAR}
  Set Test Variable  \${FOO}
  Set Test Variable  \${BAR}
State
  No Operation
End
  No Operation
"""

class TestTestGeneration(unittest.TestCase):

    def test_generate_all_dfs_max_actions_2(self):
        m = robomachine.parse(_MACHINA2)
        out = StringIO()
        robomachine.generate(m, max_actions=2, output=out)
        self.assertEqual(_TESTS2_GENERATE_ALL_DFS_MAX_ACTIONS_2, out.getvalue())

    def test_generate_all_with_variable_resolving_problem(self):
        m = robomachine.parse(_VAR_PROBLEM_MACHINE)
        out = StringIO()
        robomachine.generate(m, max_actions=1, output=out)
        self.assertEqual(_TEST_VAR_PROBLEM_MACHINE, out.getvalue())

    def test_generate_random_with_variable_resolving_problem(self):
        m = robomachine.parse(_VAR_PROBLEM_MACHINE)
        out = StringIO()
        robomachine.generate(m, max_actions=1, output=out, strategy=RandomStrategy)
        self.assertEqual(_TEST_VAR_PROBLEM_MACHINE, out.getvalue())


class TestComment(unittest.TestCase):

    def test_whole_line_comment(self):
        self._verify_comment('#   comment\n')

    def test_comment_line_with_whitespace(self):
        self._verify_comment('          #   comment\n')

    def test_content_and_comment(self):
        self._verify_comment('  Some content  # commenting it\n',
                             '  # commenting it')

    def _verify_comment(self, line, expected=None):
        expected = expected or line
        self.assertEqual(expected, comment.searchString(line)[0][0])

if __name__ == '__main__':
    unittest.main()
