import pyparsing
from robomachina.model import RoboMachina

def join_all(parts):
    return ''.join(parts)

state_name = pyparsing.Word(pyparsing.alphanums+' ')

robo_step = pyparsing.Word(pyparsing.alphanums+' ')

step = pyparsing.White(min=2)+robo_step
step.setParseAction(join_all)

action_header = pyparsing.White(min=2)+pyparsing.Literal('[Actions]')
action_header.setParseAction(join_all)

action = pyparsing.White(min=4)+robo_step+pyparsing.Literal('==>')+state_name

def create_action(parts):
    return [parts[1:]]

action.setParseAction(create_action)

actions = action_header + pyparsing.OneOrMore(action)

def create_actions(parts):
    return [action for action in parts[1:]]

actions.setParseAction(create_actions)

steps = pyparsing.ZeroOrMore(step)

def create_steps(parts):
    return parts or []

steps.setParseAction(create_steps)

state = state_name + steps +actions

def create_state(parts):
    state_name = parts[0]
    steps = parts[1]
    actions = parts[2]
    print state_name.strip(), steps.strip(), actions
    return parts

state.setParseAction(create_state)

machina_header = pyparsing.Literal('*** Machine ***')
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

