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

from parsing import parse

def generate_all_dfs(machine, max_actions=None, output=None):
    max_actions = -1 if max_actions is None else max_actions
    output.write('*** Test Cases ***')
    i = 1
    for values in machine.variable_value_sets():
        machine.apply_variable_values(values)
        for test in generate_all_from(machine.start_state, max_actions):
            output.write('\nTest %d\n' % i)
            if values:
                machine.write_variable_setting_step(values, output)
            machine.start_state.write_steps_to(output)
            for action in test:
                action.write_to(output)
            i += 1
    if machine.variables:
        output.write('\n*** Keywords ***\n')
        machine.write_variable_setter(output)

def generate_all_from(state, max_actions):
    if max_actions == 0:
        return []
    if not state.actions:
        return [[]]
    tests = []
    for action in state.actions:
        sub_tests = generate_all_from(action.next_state, max_actions-1)
        if sub_tests:
            tests += [[action]+t for t in sub_tests]
        else:
            tests += [[action]]
    return tests

def transform(text):
    machine = parse(text)
    tests = ['*** Test Cases ***', 'Test 1']
    tests += machine.states[0].steps
    tests += ['  '+machine.states[0].actions[0].name]
    tests += machine.states[1].steps
    return '\n'.join(tests)
