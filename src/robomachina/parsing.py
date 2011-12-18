import pyparsing
from robomachina.model import RoboMachina, State, Action


def join_all(parts):
    return ''.join(parts)

state_name = pyparsing.Word(pyparsing.alphanums+' ').setResultsName('state_name')
robo_step = pyparsing.Word(pyparsing.alphanums+' ').setResultsName('robo_step')

step = pyparsing.White(min=2)+robo_step
step.setParseAction(lambda t: ['  '+t.robo_step])

action_header = pyparsing.White(min=2)+pyparsing.Literal('[Actions]')
action = pyparsing.White(min=4)+robo_step+pyparsing.Literal('==>')+state_name
action.setParseAction(lambda t: [Action(t.robo_step.rstrip(), t.state_name)])

actions = action_header + pyparsing.OneOrMore(action).setResultsName('actions')
actions = pyparsing.Optional(actions)
actions.setResultsName('actions')

steps = pyparsing.ZeroOrMore(step).setResultsName('steps')

state = state_name + steps +actions
state.setParseAction(lambda p: State(p.state_name, list(p.steps), list(p.actions)))

machina_header = pyparsing.Literal('*** Machine ***')
states = pyparsing.OneOrMore(state).setResultsName('states')
machina = machina_header+states
machina.setParseAction(lambda p: RoboMachina(list(p.states)))

def parse(text):
    return machina.parseString(text)[0]
