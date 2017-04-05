"""
This is the keyword library for the webapp sample application,
a mock for a proper System Under Test.
"""
from robot.api import logger
from random import random

from robot.libraries.BuiltIn import BuiltIn


# ---------------------------------------------
#  Error-inducing decorators
#
#  Indended usage:
#  Decorate a function in the keyword library
#  with one of the supplied decorators and try
#  to find the failure(s) with your tests.
#  The idea is to learn what types of tests
#  that are required to find certain types
#  of failures.
# ---------------------------------------------
class SimulatedFailureException(Exception):
    """
    Raise this exception in the supplied
    decorators when a function is supposed
    to fail
    """


def fail_every_nth_time(count, hard=True):
    """
    This decorator will skip the decorated function every
    n-th time it is called. A hard failure (hard=True) will
    raise an exception. A soft failure (hard=False) will stop
    the decorated function from doing what it was supposed to.

    *Usage example:*

        @fail_every_nth_time(12)
        def my_func(*args):
            ...

    This example will cause my_func to return an unexpected
    value every 12:th time it is called
    """
    def decorator(func):
        def inner(*args, **kwargs):
            inner.count += 1
            if inner.count % count == 0:
                if hard is True:
                    raise SimulatedFailureException(
                        '\n  Fail in method `{:s}` (call count)'.format(
                            func.__name__))
                else:
                    logger.warn('Skipping method `{:s}` (call count)'.format(
                        func.__name__))
            else:
                func(*args, **kwargs)
            return inner
        inner.count = 0
        inner.__name__ = func.__name__
        return inner
    return decorator


def fail_with_probability(prob, hard=True):
    """
    This decorator will skip the decorated function based on the supplied
    probability of failure [0..1]. A hard failure (hard=True) will
    raise an exception. A soft failure (hard=False) will stop
    the decorated function from doing what it was supposed to.

    *Usage example:*

        @fail_with_probability(0.25)
        def my_func(*args):
            ...

    This example will cause my_func to return an unexpected
    value on average 25% of the times it is called
    """
    def decorator(func):
        def inner(*args, **kwargs):
            if random() <= prob:
                if hard is True:
                    raise SimulatedFailureException(
                        '\n  Fail in method `{:s}` (probability)'.format(
                            func.__name__))
                else:
                    logger.warn('Skipping method `{:s}` (probability)'.format(
                        func.__name__))
            else:
                func(*args, **kwargs)
            return inner
        inner.__name__ = func.__name__
        return inner
    return decorator


def fail_in_config(bad_configs, hard=True):
    """
    This decorator will skip the decorated function if the supplied
    dictionary is a subset of the available RobotFramework variables.
    A hard failure (hard=True) will raise an exception. A soft failure
    (hard=False) will stop the decorated function from doing what it
    was supposed to.

    *Usage example:*

        @fail_in_config({'${USER}': 'monkey'})
        @fail_in_config({'${CITY}': 'Boston'})
        def my_func(*args):
            ...

    This example will cause my_func to return an unexpected
    value if ${USER} is 'monkey' or if ${CITY} is 'Boston'
    """
    def decorator(func):
        def inner(*args, **kwargs):
            variables = BuiltIn().get_variables()
            if dict(variables, **bad_configs) == dict(variables):
                if hard is True:
                    raise SimulatedFailureException(
                        '\n  Fail in method `{:s}` '.format(func.__name__) +
                        '(configuration: {:s})'.format(str(bad_configs)))
                else:
                    logger.warn(
                        'Skipping method `{:s}` '.format(func.__name__) +
                        '(configuration: {:s})'.format(str(bad_configs)))
            else:
                func(*args, **kwargs)
            return inner
        inner.__name__ = func.__name__
        return inner
    return decorator


# ----------------------------
#  The actual keyword library
# ----------------------------
class KeywordLibrary(object):
    """
    This is the implementation of the keywords used in the robomachine test.

    This class mimics the observable behavior of a real application and
    is intended to be used for educational purposes. Insert errors, re-run
    your tests and try to find them!
    """
    def __init__(self):
        self._browser = None
        self._state = None
        self._name = None
        self._password = None
        self._page_title = ''
        self._change_state('Login Page')

    #
    # ASSERTS
    #
    def assert_state_is(self, state):
        """Asserts the page title"""
        if state != self._state:
            raise Exception(
                'Wrong state! The state is ' +
                '`{:s}`, expected `{:s}`.'.format(self._state, state))
        else:
            logger.info('State: `%s`' % self._state)

    def assert_page_title_is(self, title):
        """Asserts the page title"""
        if title != self._page_title:
            raise Exception(
                'Wrong page! The title at page `{:s}` '.format(self._state) +
                'was `{:s}`, expected `{:s}`.'.format(self._page_title, title))
        else:
            logger.info('Page title: `%s`' % self._page_title)

    #
    # USER ACTIONS
    #
    # In a live situation, we would call functions
    # that invokes functionality in the System Under
    # Test instead of our simple SUT mock
    # (the self._change_state() method)
    def click_login_button(self):
        """Execute the login"""
        if self._name == 'My Name' and self._password == 'mypassword':
            self._change_state('Welcome Page')
        else:
            self._change_state('Error Page')

    def click_log_out_button(self):
        """Log out and go to the login page"""
        self._change_state('Login Page')

    def enter_password(self, password):
        """Enter the password"""
        self._password = password
        logger.info('Password = `%s`' % password)

    def enter_username(self, name):
        """Enter the username"""
        self._name = name
        logger.info('User name = `%s`' % name)

    def start_browser(self, browser):
        """Emulate a browser start"""
        self._browser = browser

    #
    # APPLICATION FLOW ACTIONS
    #
    def exit_page(self):
        """Exit current page and change state"""
        if self._state == 'Error Page':
            self._change_state('Login Page')

        elif self._state == 'Profile Page':
            self._change_state('Welcome Page')

    def go_to(self, state):
        """Change state"""
        self._change_state(state)

    #
    #  PRIVATE MEMBERS
    #
    def _change_state(self, new_state):
        """Set page titles according to current page"""
        if new_state == 'Login Page':
            self._name = ''
            self._password = ''
            self._page_title = 'Please log in!'

        elif new_state == 'Welcome Page':
            self._page_title = 'This is the welcome page!'

        elif new_state == 'Profile Page':
            self._page_title = 'Hello, %s!' % self._name

        elif new_state == 'Error Page':
            self._page_title = 'Oops, something went wrong!'

        self._state = new_state
        logger.info('Changed state to `%s`' % new_state)
