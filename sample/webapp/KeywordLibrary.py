from robot.api import logger
from random import random


# Error-inducing decorators
def fail_every_nth_time(count):
    def decorator(fn):
        def inner(*args, **kwargs):
            inner._count += 1
            if inner._count % count == 0:
                logger.warn('`%s` failed on call count' % fn.__name__)
                inner._count = 0
            else:
                fn(*args, **kwargs)
            return inner
        inner._count = 0
        inner.__name__= fn.__name__
        return inner
    return decorator


def failure_probability(prob):
    def decorator(fn):
        def inner(*args, **kwargs):
            if random() <= prob:
                logger.warn('`%s` random failure' % fn.__name__)
            else:
                fn(*args, **kwargs)
            return inner
        inner.__name__= fn.__name__
        return inner
    return decorator


# The actual keyword library
class KeywordLibrary(object):
    """
    This is the implementation of the keywords used in the robomachine test.

    The keywords mimic the behavior of a real application and is intended to
    be used for educational purposes. Insert errors and re-run the tests
    to see what happens!
    """
    def __init__(self):
        self._browser = None
        self._state = None
        self._name = None
        self._password = None
        self.change_state('Login Page')

    #
    # ASSERTS
    #
    def assert_state_is(self, state):
        """Asserts the page title"""
        if state != self._state:
            raise Exception('Wrong state! The state is `%s`, expected `%s`.' % \
                (self._state, state))
        else:
            logger.info('State: `%s`' % self._state)

    def assert_page_title_is(self, title):
        """Asserts the page title"""
        if title != self._page_title:
            raise Exception('Wrong page! The title at page `%s` was `%s`, expected `%s`.' % \
                (self._state, self._page_title, title))
        else:
            logger.info('Page title: `%s`' % self._page_title)

    #
    # USER ACTIONS
    #
    def click_login_button(self):
        """Execute the login"""
        if self._name == 'My Name' and self._password == 'mypassword':
            self.change_state('Welcome Page')
        else:
            self.change_state('Error Page')

    def click_log_out_button(self):
        """Log out and go to the login page"""
        self.change_state('Login Page')

    def enter_password(self, password):
        """Enter the password"""
        self._password = password
        logger.info('Password = `%s`' % password)

    def enter_username(self, name):
        """Enter the username"""
        self._name = name
        logger.info('User name = `%s`' % name)

    def start_browser(self, browser):
        self._browser = browser

    #
    # APPLICATION FLOW ACTIONS
    #
    def change_state(self, new_state):
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

    def exit_page(self):
        """Exit current page and change state"""
        if self._state == 'Error Page':
            self.change_state('Login Page')

        elif self._state == 'Profile Page':
            self.change_state('Welcome Page')

    def go_to(self, state):
        """Change state"""
        self.change_state(state)
