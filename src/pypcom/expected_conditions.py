"""Custom expected conditions to wait for.

When using the ``wait_until`` or ``wait_until_not`` methods, if a certain
condition can not be checked for with the standard set of expected conditions
from Selenium, custom conditions and how to check for them should be defined
here.
"""

from selenium.webdriver.support import expected_conditions as EC


def visible(component, **kwargs):
    return EC.visibility_of_element_located(component._locator)


def present(component, **kwargs):
    return EC.presence_of_element_located(component._locator)


def clickable(component, **kwargs):
    return EC.element_to_be_clickable(component._locator)
