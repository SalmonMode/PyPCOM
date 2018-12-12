"""This module just contains the base class for pages."""


class Page(object):
    """The base class for all pages.

    This is the class that all pages should inherit from. Components of a page
    should be descriptors of the page's class. Components that belong to other
    components should not be included as descriptors for the page's class. For
    example, a 'username' component should be a descriptor for a 'login_form'
    component, and the 'login_form' component should be a descriptor of the
    page, so the 'username' component shouldn't be a descriptor of the page as
    well.

    Attributes:
        driver (WebDriver): WebDriver to be used for element lookups and page
            interactions.
    """

    def __init__(self, driver):
        """Create an instance of the page.

        The webdriver should be provided to the page instance at instantiation
        so that it can be passed down to its components and subcomponents as
        they're referenced.

        Args:
            driver (WebDriver): WebDriver to be used for element lookups and
                page interactions.
        """
        self.driver = driver
