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
from StringIO import StringIO

from parsing import parse
from robomachine.strategies import DepthFirstSearchStrategy


def _write_test(name, machine, output, test, values):
    output.write('\n%s\n' % name)
    if values:
        machine.write_variable_setting_step(values, output)
    machine.start_state.write_to(output)
    for action in test:
        action.write_to(output)

def _write_tests(machine, max_tests, max_actions, to_state, output, strategy_class):
    i = 1
    skipped = 0
    generated_tests = set()
    for test, values in strategy_class(machine, max_actions, to_state).tests():
        if i + skipped > max_tests:
            print '--tests-max generation try limit (%d) reached with (%d) tests generated' % (max_tests, i - 1)
            return
        if (tuple(test), tuple(values)) in generated_tests:
            skipped += 1
            continue
        else:
            generated_tests.add((tuple(test), tuple(values)))
        _write_test('Test %d' % i, machine, output, test, values)
        i += 1

def generate(machine, max_tests=1000, max_actions=None, to_state=None, output=None, strategy=DepthFirstSearchStrategy):
    max_actions = -1 if max_actions is None else max_actions
    machine.write_settings_table(output)
    machine.write_variables_table(output)
    output.write('*** Test Cases ***')
    _write_tests(machine, max_tests, max_actions, to_state, output, strategy)
    machine.write_keywords_table(output)

def transform(text):
    output = StringIO()
    generate(parse(text), output=output)
    return output.getvalue()
