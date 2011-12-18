import pyparsing
from robomachina.model import RoboMachina

def join_all(parts):
    return ''.join(parts)

state_name = pyparsing.Word(pyparsing.alphanums+' ').setResultsName('state_name')
robo_step = pyparsing.Word(pyparsing.alphanums+' ').setResultsName('robo_step')
step = pyparsing.White(min=2)+robo_step
step.setParseAction(lambda t: t.robo_step)
action_header = pyparsing.White(min=2)+pyparsing.Literal('[Actions]')
action = pyparsing.White(min=4)+robo_step+pyparsing.Literal('==>')+state_name
action.setParseAction(lambda t: [[t.robo_step, t.state_name]])
actions = action_header + pyparsing.OneOrMore(action).setResultsName('actions')
actions = pyparsing.Optional(actions)
actions.setParseAction(lambda t: t.actions)
steps = pyparsing.ZeroOrMore(step).setResultsName('steps')
steps.setParseAction(lambda t: [t.steps])
state = state_name + steps +actions

def create_state(parts):
    state_name = parts[0]
    steps = parts[1]
    actions = parts[2]
    print 'state "%s" steps "%s" actions "%s"' % (state_name.strip(), steps, actions)
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

