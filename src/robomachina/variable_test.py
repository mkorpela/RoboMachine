import unittest
from robomachina import parsing


class VariableParsingTestCases(unittest.TestCase):

    def test_variable_parsing(self):
        v = parsing.variable.parseString('${variable}')
        self.assertEqual('${variable}', v[0])

    def test_variable_definition_parsing(self):
        v = parsing.variable_definition.parseString('${abc123}  any of  one  two  123')[0]
        self.assertEqual('${abc123}', v.name)
        self.assertEqual(['one', 'two', '123'], v.values)

if __name__ == '__main__':
    unittest.main()
