"""Custom expected conditions to wait for.

When using the ``wait_until`` or ``wait_until_not`` methods, if a certain
condition can not be checked for with the standard set of expected conditions
from Selenium, custom conditions and how to check for them should be defined
here.
"""

from selenium.webdriver.support import expected_conditions as EC

visible = EC.visibility_of_element_located
present = EC.presence_of_element_located
clickable = EC.element_to_be_clickable


class animating(object):
    """An expectation for checking that velicity animation is in progress."""

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        """Check that jQuery is present and not active."""
        el = driver.find_element(*self.locator)
        classes = el.get_attribute("class").split(" ")
        return "velocity-animating" in classes
