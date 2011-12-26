from pyparsing import *
from robomachina.model import RoboMachina, State, Action, Variable

state_name = Word(alphanums+' ').setResultsName('state_name')
robo_step = Word(alphanums+' ').setResultsName('robo_step')

variable = Literal('${')+Word(alphanums)+'}'
variable.setParseAction(lambda  t: '${%s}' % t[1])

variable_value = Word(alphanums)+ZeroOrMore(' '+Word(alphanums))

variable_definition = variable.setResultsName('variable_name') + 'any of' + OneOrMore(variable_value).setResultsName('variable_values')
variable_definition.setParseAction(lambda t: [Variable(t.variable_name, list(t.variable_values))])

step = White(min=2)+robo_step
step.setParseAction(lambda t: ['  '+t.robo_step])

action_header = White(min=2)+'[Actions]'
action = White(min=4)+robo_step+'==>'+state_name
action.setParseAction(lambda t: [Action(t.robo_step.rstrip(), t.state_name)])

actions = action_header + OneOrMore(action).setResultsName('actions')
actions = Optional(actions)
actions.setResultsName('actions')

steps = ZeroOrMore(step).setResultsName('steps')

state = state_name + steps +actions
state.setParseAction(lambda p: State(p.state_name, list(p.steps), list(p.actions)))

machina_header = Literal('*** Machine ***')
states = OneOrMore(state).setResultsName('states')
machina = machina_header+states
machina.setParseAction(lambda p: RoboMachina(list(p.states)))

def parse(text):
    return machina.parseString(text, parseAll=True)[0]
