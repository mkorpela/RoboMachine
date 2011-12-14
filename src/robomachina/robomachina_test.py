import unittest
import robomachina


_MACHINA = """
*** Machine ***
Start State
  Log  In Start State
  [Actions]
    No Operation  ==>  End State

End State
  Log  In End State
"""

_TESTS = """
*** Test Cases ***
Test 1
  Log  In Start State
  No Operation
  Log  In End State
"""

class TestRoboMachina(unittest.TestCase):

    def test_transform_to_robot_test_cases(self):
        tests = robomachina.transform(_MACHINA)
        self.assertEqual(_TESTS, tests)

    def test_parse_machina_state_names(self):
        machina = robomachina.parse(_MACHINA)
        self.assertEqual(['Start State', 'End State'], [s.name for s in machina.states])

    def test_parse_machina_state_actions(self):
        machina = robomachina.parse(_MACHINA)
        self.assertEqual(['No Operation'], [a.name for a in machina.states[0].actions])
        self.assertEqual([], [a.name for a in machina.states[1].actions])

    def test_parse_machina_state_stepst(self):
        machina = robomachina.parse(_MACHINA)
        self.assertEqual(['  Log  In Start State'], machina.states[0].steps)
        self.assertEqual(['  Log  In End State'], machina.states[1].steps)


if __name__ == '__main__':
    unittest.main()
