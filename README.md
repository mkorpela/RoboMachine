# RoboMachine

A test data generator for [Robot Framework](http://www.robotframework.org).

## What is this tool for?

You know those ugly bugs that users report that somehow were missed by all your ATDD-, TDD- and exploratory testing? Those bugs that lurk in the corners of complexity of the system that you are building. Those bugs that will make users of your application hate you..

This tool is here to help you seek and destroy those bugs before users will find them.

It gives you the ability to generate a huge number of tests that can go through a very vast number of similar (or not so similar) test scenarios.

## What is it?

If you know Regular Expressions:
A regular expression is a pattern that represents all the possible strings that match that pattern. RoboMachine works in a similar way. A machine represents a set of tests in a compact way. This machine can be used to generate all (or part of) the tests that it represents.

If you know Model-Based Testing or automata theory:
With RoboMachine you define an extended finite state machine (in a Robot Framework -like syntax) that represents a set of tests. RoboMachine also contains algorithms that can be used to generate real executable Robot Framework tests from a RoboMachine model.

If you know Combinatorial Testing or like data driven testing:
With RoboMachine you can define sets of data and rules about that data, that can be used to generate data driven tests (and also keyword driven tests). This allows you to keep your data in compact sets and let the system generate the real test data vectors from there.

## What does it look like?

Here is an example machine (using combinatorial techniques) that can generate tests for [SeleniumLibrary demo](http://code.google.com/p/robotframework-seleniumlibrary/wiki/Demo).

```robotframework
*** Settings ***
Suite Setup     Open Browser  ${LOGIN_PAGE_URL}   googlechrome
Suite Teardown  Close Browser
Test Setup      Go to  ${LOGIN_PAGE_URL}
Library         SeleniumLibrary

*** Variables ***
${USERNAME_FIELD}  username_field
${PASSWORD_FIELD}  password_field
${LOGIN_BUTTON}    LOGIN
${VALID_USERNAME}  demo
${VALID_PASSWORD}  mode
${LOGIN_PAGE_URL}  http://localhost:7272/html/

*** Machine ***
${USERNAME}  any of  ${VALID_USERNAME}  ${VALID_PASSWORD}  invalid123  ${EMPTY}
${PASSWORD}  any of  ${VALID_PASSWORD}  ${VALID_USERNAME}  password123  ${EMPTY}

# Add an equivalence rule to reduce the number of generated tests
${USERNAME} == ${VALID_PASSWORD}  <==>  ${PASSWORD} == ${VALID_USERNAME}

Login Page
  Title Should Be  Login Page
  [Actions]
    Submit Credentials  ==>  Welcome Page  when  ${USERNAME} == ${VALID_USERNAME}  and  ${PASSWORD} == ${VALID_PASSWORD}
    Submit Credentials  ==>  Error Page    otherwise

Welcome Page
  Title Should Be  Welcome Page

Error Page
  Title Should Be  Error Page

*** Keywords ***
Submit Credentials
  Input Text      ${USERNAME_FIELD}  ${USERNAME}
  Input Password  ${PASSWORD_FIELD}  ${PASSWORD}
  Click Button    ${LOGIN_BUTTON}
```

Here is another example machine (using model-based testing with finite state machine):

```robotframework
*** Settings ***
Suite Setup     Open Browser  ${LOGIN_PAGE_URL}   googlechrome
Suite Teardown  Close Browser
Test Setup      Go to  ${LOGIN_PAGE_URL}
Library         SeleniumLibrary

*** Variables ***
${USERNAME_FIELD}  username_field
${PASSWORD_FIELD}  password_field
${LOGIN_BUTTON}    LOGIN
${VALID_USERNAME}  demo
${VALID_PASSWORD}  mode
${LOGIN_PAGE_URL}  http://localhost:7272/html/

*** Machine ***
Login Page
  Title Should Be  Login Page
  [Actions]
    Submit Valid Credentials  ==>  Welcome Page
    Submit Invalid Credentials  ==>  Error Page

Welcome Page
  Title Should Be  Welcome Page
  [Actions]
    Go to  ${LOGIN_PAGE_URL}  ==>  Login Page

Error Page
  Title Should Be  Error Page
  [Actions]
    Go to  ${LOGIN_PAGE_URL}  ==>  Login Page

*** Keywords ***
Submit Valid Credentials
  Submit Credentials  ${VALID_USERNAME}  ${VALID_PASSWORD}

Submit Invalid Credentials
  Submit Credentials  invalid_username   invalid_password

Submit Credentials
  [Arguments]     ${username}        ${password}
  Input Text      ${USERNAME_FIELD}  ${USERNAME}
  Input Password  ${PASSWORD_FIELD}  ${PASSWORD}
  Click Button    ${LOGIN_BUTTON}
```

NOTE! This machine can generate infinite number of test sequences thus you need to constraint the generation.
For example:

    robomachine --tests-max 10 --actions-max 20 --to-state 'Welcome Page' --generation-algorithm random [MACHINE_FILE_NAME]

will generate 10 random tests with at most 20 actions each and all tests ending to state 'Welcome Page'.

## Installation

From [Python Package Index](http://pypi.python.org/pypi)

    pip install RoboMachine


From source:

    git clone git://github.com/mkorpela/RoboMachine.git
    cd RoboMachine
    python setup.py install

After this you should have a commandline tool called `robomachine` available.
See `robomachine --help` for commandline tool usage.

## Syntax

* Only supported Robot Framework format is space separated format.
* You should use `.robomachine` suffix for your Machine files.
* You can have a Robot Framework *Settings* table at the beginning of the machine file.
* You can have a Robot Framework *Variables* table after the optional Settings table.
* *Machine* table is a must.
* You can have a Robot Framework *Keywords* table after the Machine table.

## Machine table syntax

Used machine variables must be introduced at the beginning of the machine table. Valid machine variable is a valid Robot Framework variable that contains only uppercase characters A-Z, numbers (not at the start) 0-9 and
underscores (`_`). For example: `${VALID_123}` is a valid machine variable.

An example of a valid machine variable definition line::

    ${VALID_VARIABLE_1}  any of  Value 1  Value 2  Value 3

Rules about the machine variables should be next. Rule building blocks:
* Variable conditions:
  * `${VARIABLE} == value`
  * `${VARIABLE} != value`
  * `${VARIABLE} <  value`
  * `${VARIABLE} <= value`
  * `${VARIABLE} >  value`
  * `${VARIABLE} >= value`
  * `${VARIABLE} in (a, b)`  # short for ${VARIABLE} == a  or  ${VARIABLE} == b
  * `${VARIABLE} ~ REGEX`  # python regexp: re.search(REGEX, ${VARIABLE}) != None
  * `${VARIABLE} !~ REGEX`  # negated regexp match
* And rule:             [some condition]  and  [some other condition]
* Or rule:              [some condition]  or  [some other condition]
* Not rule:             not ([some condition])
* Implication rule:     [some condition]  ==>  [some condition]
* Equivalence rule:     [some condition]  <==>  [some condition]
* [some condition]:     Variable condition OR (rule)

Rules can be used to remove variable combinations that should not be used in
test generation.

An example of a valid rule line:

    ${VARIABLE_1} == Value 1  ==>  (${FOO} == bar  or  ${FOO} == zoo)

Which means: When `${VARIABLE_1}` value is "Value 1" then `${FOO}` should either be "bar" or "zoo".

State blocks should be next. First state block is the starting state.

State block starts with a line containing the states name. Valid state name contains only upper and lowercase characters a-zA-Z, numbers (not at the start) 0-9 and spaces (not at the start or end and only one
between words).

This is followed by the Robot Framework steps that should be executed when in that
state.

This can be followed by an actions block definition.

An actions block starts with `[Actions]` tag and is followed by one or more action lines.

An action line has four parts:
* A Robot Framework step that is executed when the action happens (action label) (you can also leave this out - use a tau transition)
* `  ==>  ` right arrow with two spaces before and after
* Name of the state that the machine ends up when the action is taken (end state)
* Optional rule (when the action is available) this either starts with
  `  when  ` and the rule or  `  otherwise  ` - meaning this action should be taken when
  all of the other actions with same action label are not available

An example of a valid state definition::

```robotframework
State Name
  Robot Framework  Step  with  ${arguments}
  Log  something  WARN
  [Actions]
    Log  other thing  ==>  Other State  when  ${FOO} == bar
    Log  other thing  ==>  Another State  when  (${FOO} == zoo  and  ${BAR} == goo)
    Log  other thing  ==>  End State  otherwise
    Log  nothing      ==>  End State
    ==>  Some state # This here is a tau transition that does not write a step to the test
```
