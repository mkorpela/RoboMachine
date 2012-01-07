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

class EquivalenceRule(object):

    def __init__(self, condition1, condition2):
        self._condition1 = condition1
        self._condition2 = condition2
        self._values = {}

    @property
    def text(self):
        return '%s  <==>  %s' % (self._condition1, self._condition2)

    def set_variable(self, name, value):
        self._values[name] = value

    def is_valid(self):
        return self._condition1.is_valid(self._values) == self._condition2.is_valid(self._values)


class AndRule(object):

    def __init__(self, conditions):
        self._conditions = conditions
        self._values = {}

    def __str__(self):
        return '  and  '.join(str(c) for c in self._conditions)

    def set_variable(self, name, value):
        self._values[name] = value

    def is_valid(self):
        return not(any(not(c.is_valid(self._values)) for c in self._conditions))


class Condition(object):

    def __init__(self, variable_name, value):
        self._name = variable_name.strip()
        self._value = value.strip()
        self._values = {}

    def __str__(self):
        return '%s == %s' % (self._name, self._value)

    def is_valid(self, value_mapping=None):
        value_mapping = value_mapping or self._values
        return value_mapping[self._name].strip() == self._value.strip()

    def set_variable(self, name, value):
        self._values[name] = value
