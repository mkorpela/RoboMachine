from parsing import parse

def transform(text):
    machine = parse(text)
    tests = ['*** Test Cases ***', 'Test 1']
    tests += machine.states[0].steps
    tests += ['  '+machine.states[0].actions[0].name]
    tests += machine.states[1].steps
    return '\n'.join(tests)
