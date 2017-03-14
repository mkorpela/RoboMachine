"""
The keyword library for the sample webapp.

It it built for educational purposes and it merely mimics responses from a real application.
"""
from robot.api import logger



class KeywordLibrary(object):
    """
    This is the implementation of the keywords used in the robomachine test
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




