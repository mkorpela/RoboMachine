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

import re


class EquivalenceRule(object):

    def __init__(self, condition1, condition2):
        self._condition1 = condition1
        self._condition2 = condition2

    def __str__(self):
        return '{:s}  <==>  {:s}'.format(str(self._condition1), str(self._condition2))

    def is_valid(self, value_mapping):
        return self._condition1.is_valid(value_mapping) == self._condition2.is_valid(value_mapping)


class ImplicationRule(object):

    def __init__(self, condition1, condition2):
        self._condition1 = condition1
        self._condition2 = condition2

    def __str__(self):
        return '{:s}  ==>  {:s}'.format(str(self._condition1), str(self._condition2))

    def is_valid(self, value_mapping):
        return not self._condition1.is_valid(value_mapping) or self._condition2.is_valid(value_mapping)


class AndRule(object):

    def __init__(self, conditions):
        self._conditions = conditions

    def __str__(self):
        return '  and  '.join(str(c) for c in self._conditions)

    def is_valid(self, value_mapping):
        return not(any(not(c.is_valid(value_mapping)) for c in self._conditions))


class OrRule(object):

    def __init__(self, conditions):
        self._conditions = conditions

    def __str__(self):
        return '  or  '.join(str(c) for c in self._conditions)

    def is_valid(self, value_mapping):
        return any(c.is_valid(value_mapping) for c in self._conditions)


class NotRule(object):

    def __init__(self, condition):
        self._condition = condition

    def __str__(self):
        return 'not ({:s})'.format(str(self._condition))

    def is_valid(self, value_mapping):
        return not self._condition.is_valid(value_mapping)


class Condition(object):

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()

    def __str__(self):
        return '{:s} == {:s}'.format(self._name, self._value)

    def is_valid(self, value_mapping):
        return value_mapping[self._name].strip() == self._value.strip()


def UnequalCondition(variable_name, value):
    return NotRule(Condition(variable_name, value))


class GreaterThanCondition(object):

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()

    def __str__(self):
        return '{:s} > {:s}'.format(self._name, self._value)

    def is_valid(self, value_mapping):
        return value_mapping[self._name].strip() > self._value.strip()


class GreaterThanOrEqualCondition(object):

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()

    def __str__(self):
        return '{:s} >= {:s}'.format(self._name, self._value)

    def is_valid(self, value_mapping):
        return value_mapping[self._name].strip() >= self._value.strip()


class LessThanCondition(object):

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()

    def __str__(self):
        return '{:s} < {:s}'.format(self._name, self._value)

    def is_valid(self, value_mapping):
        return value_mapping[self._name].strip() < self._value.strip()


class LessThanOrEqualCondition(object):

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()

    def __str__(self):
        return '{:s} <= {:s}'.format(self._name, self._value)

    def is_valid(self, value_mapping):
        return value_mapping[self._name].strip() <= self._value.strip()


class RegexCondition(object):

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()

    def __str__(self):
        return '{:s} ~ {:s}'.format(self._name, self._value)

    def is_valid(self, value_mapping):
        return re.search(self._value.strip(), value_mapping[self._name].strip()) is not None


class RegexNegatedCondition(object):

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()

    def __str__(self):
        return '{:s} !~ {:s}'.format(self._name, self._value)

    def is_valid(self, value_mapping):
        return re.search(self._value.strip(), value_mapping[self._name].strip()) is None
