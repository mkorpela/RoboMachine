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
import random

import unittest
from robomachine.rules import Condition, AndRule, EquivalenceRule, OrRule, NotRule, ImplicationRule, UnequalCondition


class RulesTestCases(unittest.TestCase):

    _TRUE = lambda:0
    _TRUE.is_valid = lambda value_mapping: True
    _FALSE = lambda:0
    _FALSE.is_valid = lambda value_mapping: False

    def test_condition(self):
        condition = Condition('${VARIABLE}', 'value')
        self.assertTrue(condition.is_valid(value_mapping={'${VARIABLE}':'value'}))
        self.assertFalse(condition.is_valid(value_mapping={'${VARIABLE}':'wrong value'}))

    def test_unequal_condition(self):
        condition = UnequalCondition('${VARIABLE}', 'value')
        self.assertFalse(condition.is_valid(value_mapping={'${VARIABLE}':'value'}))
        self.assertTrue(condition.is_valid(value_mapping={'${VARIABLE}':'wrong value'}))

    def test_and_rule(self):
        self.assertTrue(AndRule([self._TRUE for _ in range(10)]).is_valid({}))
        self.assertFalse(AndRule([self._FALSE]+[self._TRUE for _ in range(10)]).is_valid({}))

    def test_equivalence_rule(self):
        self.assertTrue(EquivalenceRule(self._TRUE, self._TRUE).is_valid({}))
        self.assertFalse(EquivalenceRule(self._FALSE, self._TRUE).is_valid({}))
        self.assertFalse(EquivalenceRule(self._TRUE, self._FALSE).is_valid({}))
        self.assertTrue(EquivalenceRule(self._FALSE, self._FALSE).is_valid({}))

    def test_or_rule(self):
        self.assertFalse(OrRule([self._FALSE for _ in range(10)]).is_valid({}))
        self.assertTrue(OrRule([self._TRUE]+[self._FALSE for _ in range(10)]).is_valid({}))

    def test_not_rule(self):
        self.assertFalse(NotRule(self._TRUE).is_valid({}))
        self.assertTrue(NotRule(self._FALSE).is_valid({}))

    def test_implication_rule(self):
        self.assertTrue(ImplicationRule(self._TRUE, self._TRUE).is_valid({}))
        self.assertTrue(ImplicationRule(self._FALSE, self._TRUE).is_valid({}))
        self.assertFalse(ImplicationRule(self._TRUE, self._FALSE).is_valid({}))
        self.assertTrue(ImplicationRule(self._FALSE, self._FALSE).is_valid({}))

if __name__ == '__main__':
    unittest.main()
