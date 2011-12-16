import pyparsing
from robomachina.model import RoboMachina

def transform(text):
    machine = parse(text)
    tests = ['*** Test Cases ***', 'Test 1']
    tests += machine.states[0].steps
    tests += ['  '+machine.states[0].actions[0].name]
    tests += machine.states[1].steps
    return '\n'.join(tests)

def printther(s):
    def printaa(u):
        print s, u
        return u
    return printaa

machina_header = pyparsing.Literal('*** Machine ***')
machina_header.setParseAction(printther('machina header'))
state_name = pyparsing.Word(pyparsing.alphanums+' ')
state_name.setParseAction(printther('state name'))
robo_step = pyparsing.Word(pyparsing.alphanums+' ')
step = pyparsing.White(min=2)+robo_step
step.setParseAction(printther('step'))
action_header = pyparsing.White(min=2)+pyparsing.Literal('[Actions]')
action_header.setParseAction(printther('action header'))
action = pyparsing.White(min=4)+robo_step+pyparsing.Literal('==>')+state_name
action.setParseAction(printther('action'))
actions = action_header + pyparsing.OneOrMore(action)
state = state_name + pyparsing.ZeroOrMore(step)+actions
state.setParseAction(printther('state'))

machina = machina_header+pyparsing.OneOrMore(state)

def parse(text):
    print machina.parseString(text)
    machine = RoboMachina()
    current_state = None
    for line in text.splitlines():
        if line == '*** Machine ***':
            continue
        if len(line) and line[0] != ' ':
            current_state = machine.add_state(line.strip())
            continue
        if line.startswith('    ') and line.strip():
            current_state.add_action(line.split('==>')[0].strip())
            continue
        if line == '  [Actions]':
            continue
        if line.startswith('  ') and line.strip():
            current_state.add_step(line)
    return machine
