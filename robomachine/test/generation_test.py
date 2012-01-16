from StringIO import StringIO
import unittest
from robomachine.model import RoboMachine, State, Action
import robomachine


class GenerationTestCase(unittest.TestCase):

    def test_generation_with_no_tests(self):
        mock_machine = RoboMachine(states=[], variables=[], rules=[])
        output = StringIO()
        robomachine.generate(machine=mock_machine, output=output, strategy=_MockStrategyWithNoTests)
        self.assertEqual('*** Test Cases ***', output.getvalue())

    def test_generation_with_no_tests(self):
        mock_machine = RoboMachine(states=[State('bar', [], [])], variables=[], rules=[])
        output = StringIO()
        robomachine.generate(machine=mock_machine, max_tests=10, output=output, strategy=_MockStrategyWithHundredTests)
        self.assertEqual(10, sum(1 for line in output.getvalue().splitlines() if line.startswith('Test ')))

    def test_generation_with_same_generated_tests(self):
        mock_machine = RoboMachine(states=[State('bar', [], [])], variables=[], rules=[])
        output = StringIO()
        robomachine.generate(machine=mock_machine, max_tests=1000, output=output, strategy=_MockStrategyWithSameTests)
        self.assertEqual(1, sum(1 for line in output.getvalue().splitlines() if line.startswith('Test ')))


class _MockStrategy(object):

    def __init__(self, machine, *others):
        self._machine = machine

    def _action(self):
        a = Action('foo', 'bar')
        a.set_machine(self._machine)
        return a


class _MockStrategyWithNoTests(_MockStrategy):

    def tests(self):
        return []


class _MockStrategyWithHundredTests(_MockStrategy):

    def tests(self):
        return [([self._action()], []) for i in range(100)]


class _MockStrategyWithSameTests(_MockStrategy):

    def tests(self):
        test = ([self._action()], [])
        while True:
            yield test


if __name__ == '__main__':
    unittest.main()
