import unittest
from robomachina import parsing


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

class VariableMachineParsingTestCases(unittest.TestCase):

    def test_machine_parsing(self):
        m = parsing.parse(_LOGIN_MACHINE)
        self.assertEqual('${USERNAME}', m.variables[0].name)
        self.assertEqual('${PASSWORD}', m.variables[1].name)
        self.assertEqual(2, len(m.variables))
        self.assertEqual('${USERNAME} == demo and ${PASSWORD} == mode', m.states[0].actions[0].condition)
        self.assertEqual('otherwise', m.states[0].actions[1].condition)

if __name__ == '__main__':
    unittest.main()
