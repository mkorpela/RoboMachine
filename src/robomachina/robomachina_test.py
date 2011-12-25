from StringIO import StringIO
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


_MACHINA2 = """
*** Machine ***
A
  Foo  bar
  Bar  foo
  [Actions]
    first  ==>  B
    second  ==>  C

B
  [Actions]
    something else  ==>  A
    other thing     ==>  C

C
  No Operation
"""

_TESTS2_GENERATE_ALL_DFS_MAX_ACTIONS_2 = """\
*** Test Cases ***
Test 1
  Foo  bar
  Bar  foo
  first
  something else
  Foo  bar
  Bar  foo

Test 2
  Foo  bar
  Bar  foo
  first
  other thing
  No Operation

Test 3
  Foo  bar
  Bar  foo
  second
  No Operation
"""

class TestParsing(unittest.TestCase):

    def test_parsing(self):
        m = robomachina.parse(_MACHINA2)
        self.assertEqual(m.states[0].name, 'A')
        self.assertEqual(m.states[0].steps, ['  Foo  bar', '  Bar  foo'])
        self.assertEqual([a.name for a in m.states[0].actions], ['first', 'second'])
        self.assertEqual([a.next_state.name for a in m.states[0].actions], ['B', 'C'])
        self.assertEqual(m.states[1].name, 'B')
        self.assertEqual(m.states[1].steps, [])
        self.assertEqual([a.name for a in m.states[1].actions], ['something else', 'other thing'])
        self.assertEqual([a.next_state.name for a in m.states[1].actions], ['A', 'C'])
        self.assertEqual(m.states[2].name, 'C')
        self.assertEqual(m.states[2].steps, ['  No Operation'])
        self.assertEqual(m.states[2].actions, [])

class TestTestGeneration(unittest.TestCase):

    def test_generate_all_dfs_max_actions_2(self):
        m = robomachina.parse(_MACHINA2)
        out = StringIO()
        robomachina.generate_all_dfs(m, max_actions=2, output=out)
        self.assertEqual(out.getvalue(), _TESTS2_GENERATE_ALL_DFS_MAX_ACTIONS_2)


if __name__ == '__main__':
    unittest.main()
