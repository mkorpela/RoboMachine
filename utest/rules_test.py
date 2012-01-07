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
from robomachine.rules import Condition, AndRule, EquivalenceRule, OrRule, NotRule


class RulesTestCases(unittest.TestCase):

    def test_condition(self):
        condition = Condition('${VARIABLE}', 'value')
        self.assertTrue(condition.is_valid(value_mapping={'${VARIABLE}':'value'}))
        self.assertFalse(condition.is_valid(value_mapping={'${VARIABLE}':'wrong value'}))

    def test_and_rule(self):
        and_rule = AndRule([Condition('${VARIABLE%d}' % i, str(i)) for i in range(10)])
        value_mapping = {}
        for i in range(10):
            value_mapping['${VARIABLE%d}' % i] = str(i)
        self.assertTrue(and_rule.is_valid(value_mapping=value_mapping))
        for i in range(10):
            value_mapping['${VARIABLE%d}' % i] = 'wrong'
            self.assertFalse(and_rule.is_valid(value_mapping=value_mapping))
            value_mapping['${VARIABLE%d}' % i] = str(i)

    def test_equivalence_rule(self):
        equivalence_rule = EquivalenceRule(Condition('${V1}', 'foo'), Condition('${V2}', 'bar'))
        self.assertTrue(equivalence_rule.is_valid({'${V1}':'foo', '${V2}':'bar'}))

    def test_or_rule(self):
        or_rule = OrRule([Condition('${VARIABLE%d}' % i, str(i)) for i in range(10)])
        value_mapping = {}
        for i in range(10):
            value_mapping['${VARIABLE%d}' % i] = 'wrong'
        self.assertFalse(or_rule.is_valid(value_mapping=value_mapping))
        for i in range(10):
            value_mapping['${VARIABLE%d}' % i] = str(i)
            self.assertTrue(or_rule.is_valid(value_mapping=value_mapping))
            value_mapping['${VARIABLE%d}' % i] = 'wrong'

    def test_not_rule(self):
        not_rule = NotRule(Condition('${VARIABLE}', 'value'))
        self.assertFalse(not_rule.is_valid({'${VARIABLE}':'value'}))
        self.assertTrue(not_rule.is_valid({'${VARIABLE}':'wrong value'}))

if __name__ == '__main__':
    unittest.main()
