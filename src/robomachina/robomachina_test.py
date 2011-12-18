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
""".strip()

class TestRoboMachina(unittest.TestCase):

    def test_transform_to_robot_test_cases(self):
        tests = robomachina.transform(_MACHINA)
        self.assertEqual(_TESTS, tests)

    def test_parse_machina_state_names(self):
        m = robomachina.parse(_MACHINA)
        self.assertEqual(['Start State', 'End State'], [s.name for s in m.states])

    def test_parse_machina_state_actions(self):
        m = robomachina.parse(_MACHINA)
        self.assertEqual(['No Operation'], [a.name for a in m.states[0].actions])
        self.assertEqual([], [a.name for a in m.states[1].actions])

    def test_parse_machina_state_steps(self):
        m = robomachina.parse(_MACHINA)
        self.assertEqual(['  Log  In Start State'], m.states[0].steps)
        self.assertEqual(['  Log  In End State'], m.states[1].steps)


if __name__ == '__main__':
    unittest.main()
