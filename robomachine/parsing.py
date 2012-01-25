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

from pyparsing import *
from robomachine.model import RoboMachine, State, Action, Variable
from robomachine.rules import AndRule, Condition, EquivalenceRule, OrRule, NotRule, ImplicationRule, UnequalCondition


end_of_line = Regex(r' *\n') ^ LineEnd()

settings_table = Literal('*** Settings ***')+Regex(r'[^\*]+(?=\*)')
settings_table.setParseAction(lambda t: '\n'.join(t))
variables_table = Literal('*** Variables ***')+Regex(r'[^\*]+(?=\*)')
variables_table.setParseAction(lambda t: '\n'.join(t))
keywords_table = Literal('*** Keywords ***')+CharsNotIn('')+StringEnd()
keywords_table.setParseAction(lambda t: '\n'.join(t))

state_name = Regex(r'\w+( \w+)*')
state_name.leaveWhitespace()
state_name = state_name.setResultsName('state_name')

robo_step = Regex('([\w\$\{\}][ \w\$\{\}]*[\w\}]|\w)')
robo_step.leaveWhitespace()
robo_step = robo_step.setResultsName('robo_step')

variable = Regex(Variable.REGEX)

variable_value = Regex(r'[\w\$\{\}!?\-\_\.\/]+( [\w\$\{\}!?\-\_\.\/]+)*')

splitter = Literal(' ')+OneOrMore(' ')
splitter.setParseAction(lambda t: '  ')

variable_values = (variable_value+ZeroOrMore(splitter+variable_value)).setResultsName('variable_values')
variable_values.setParseAction(lambda t: [[t[2*i] for i in range((len(t)+1)/2)]])

variable_definition = variable.setResultsName('variable_name') + splitter+'any of'+splitter+ variable_values + end_of_line
variable_definition.leaveWhitespace()
variable_definition.setParseAction(lambda t: [Variable(t.variable_name, list(t.variable_values))])

rule = Forward()

condition_rule = variable+' == '+variable_value
condition_rule.setParseAction(lambda t: [Condition(t[0], t[2])])
condition_rule.leaveWhitespace()

unequal_condition_rule = variable+' != '+variable_value
unequal_condition_rule.setParseAction(lambda t: [UnequalCondition(t[0], t[2])])
unequal_condition_rule.leaveWhitespace()

closed_rule = condition_rule ^ unequal_condition_rule ^ ('('+rule+')')
closed_rule.setParseAction(lambda t: [t[1]] if len(t) == 3 else t)

not_rule = Literal('not ')+closed_rule
not_rule.leaveWhitespace()
not_rule.setParseAction(lambda t: [NotRule(t[1])])

equivalence_rule = closed_rule +'  <==>  '+closed_rule
equivalence_rule.leaveWhitespace()
equivalence_rule.setParseAction(lambda t: [EquivalenceRule(t[0], t[2])])

implication_rule = closed_rule +'  ==>  '+closed_rule
implication_rule.leaveWhitespace()
implication_rule.setParseAction(lambda t: [ImplicationRule(t[0], t[2])])

and_rule = closed_rule+ZeroOrMore('  and  '+closed_rule)
and_rule.setParseAction(lambda t: [AndRule([t[i] for i in range(len(t)) if i % 2 == 0])])
and_rule.leaveWhitespace()

or_rule = closed_rule+ZeroOrMore('  or  '+closed_rule)
or_rule.setParseAction(lambda t: [OrRule([t[i] for i in range(len(t)) if i % 2 == 0])])
or_rule.leaveWhitespace()

rule << (not_rule ^ equivalence_rule ^ implication_rule ^ and_rule ^ or_rule ^ closed_rule)

step = Regex(r'  [^\n\[][^\n]*(?=\n)')+LineEnd()
step.leaveWhitespace()
step.setParseAction(lambda t: [t[0]])

action_header = White(min=2)+'[Actions]'

condition = Literal('  when  ')+rule
condition = condition ^ Regex(r'  +otherwise')
def parse_condition(cond):
    if cond[0] == '  when  ':
        return [cond[1]]
    return ['otherwise']

condition.leaveWhitespace()
condition.setParseAction(parse_condition)
condition = Optional(condition).setResultsName('condition')
action = White(min=4)+Optional(robo_step + White(min=2)) + '==>'+White(min=2) + state_name + condition + end_of_line
action.leaveWhitespace()
action.setParseAction(lambda t: [Action(t.robo_step.rstrip(), t.state_name, t.condition)])

actions = action_header + end_of_line + OneOrMore(action).setResultsName('actions')
actions = Optional(actions)
actions.leaveWhitespace()
actions.setResultsName('actions')

comment = Regex(r'(^\s*\#[^\n]*\n)|(\s\s+\#[^\n]*(?=\n))')
comment.leaveWhitespace()

steps = ZeroOrMore(step).setResultsName('steps')

state = state_name + end_of_line + steps + actions
state.leaveWhitespace()
state.setParseAction(lambda p: State(p.state_name, list(p.steps), list(p.actions)))

machine_header = Literal('*** Machine ***')+end_of_line
states = state+ZeroOrMore(OneOrMore(LineEnd())+state)
states.setParseAction(lambda t: [[t[2*i] for i in range((len(t)+1)/2)]])
states = states.setResultsName('states')
variables = ZeroOrMore(variable_definition).setResultsName('variables')
rules = ZeroOrMore(rule+end_of_line).setResultsName('rules')
rules.setParseAction(lambda t: [t[i] for i in range(len(t)) if i % 2 == 0])
machine = Optional(settings_table).setResultsName('settings_table')+\
          Optional(variables_table).setResultsName('variables_table')+\
          machine_header+ZeroOrMore(end_of_line)+variables+\
          ZeroOrMore(end_of_line)+rules+\
          ZeroOrMore(end_of_line)+states+\
          Optional(keywords_table).setResultsName('keywords_table')

def create_robomachine(p):
    return RoboMachine(list(p.states),
                       list(p.variables),
                       list(p.rules),
                       settings_table=p.settings_table,
                       variables_table=p.variables_table,
                       keywords_table=p.keywords_table)

machine.setParseAction(create_robomachine)
machine.ignore(comment)
machine.setWhitespaceChars(' ')

class RoboMachineParsingException(Exception):
    pass

def parse(text):
    try:
        return machine.parseString(text, parseAll=True)[0]
    except ParseBaseException, pe:
        print 'Exception at line %d' % pe.lineno
        print pe.msg
        print 'line: "%s"' % pe.line
        raise RoboMachineParsingException(pe.msg)
    except AssertionError, ae:
        print ae
        raise RoboMachineParsingException(ae)
