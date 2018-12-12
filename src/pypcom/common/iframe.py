"""Template component class for iframes."""

from pypcom import PageComponent as PC


class Iframe(PC):
    """Iframe base class.

    Sometimes pages have iframes that you need to access, but Selenium has
    difficulty accessing them, because it needs to switch its focus to that
    frame in order to look inside (depending on the browser). This class is
    designed to automate switching the focus to the iframe and back to the
    "default content" (the normal context for the page) so that it doesn't have
    to be handled manually. This gets tricky, because you can't just switch the
    focus back to the default content once you have the reference to the
    ``WebElement`` inside the iframe, as the reference becomes moot, so you
    won't be able to do anything with the ``WebElement``.

    ``PageComponent``s that are descendants of an ``Iframe`` should be able to
    automatically handle switching focus as long they are referenced as a
    descriptor, and you don't access their ``_el`` property directly. They do
    this by:

    1. checking for an ancestor that is an ``Iframe`` whenever you need to
    interact with their associated ``WebElement`` (e.g. sending keys, getting
    an attribute/property, clicking, waiting)
    2. if they find one, they try to make sure it has focus before looking the
    ``WebElement`` up, and
    3. only return the focus to the "default content" once the interaction is
    completed.

    You should have the focus switched to the iframe only as long as you need
    to get what you want, and then reset it back to the default immediately
    once you're done. This system attempts to automate that process. But
    sometimes, the structure of your Page object might not allow for this to
    happen automatically. This is rare, and should be avoided whenever
    possible. But if it can't be avoided, this class offers two methods for you
    to have your code manually switch focus:

    1. ``switch_to()``
    2. ``switch_to_default_content()``

    If you have to invoke these yourself, it should be incorporated into your
    Page object model structure so that they aren't seen in your code, and to
    ensure that the focus is managed in a consistent manner.

    Example:

    .. code-block::

        MyIframe(Iframe):

            _locator = (
                By.CSS_SELECTOR,
                "#my-iframe",
            )
    Example:

    .. code-block::

        page.my_iframe.switch_to()
        page.my_iframe.switch_to_default_content()
        assert page.my_iframe.my_component.is_displayed()
        my_component = page.my_iframe.my_component
        my_component.sub_component.wait_until("visible")
        assert my_component.sub_component.is_present()
    """

    _is_iframe = True

    def switch_to_default_content(self):
        """Switch the focus of Selenium to the default content (the page)."""
        self.driver.switch_to.default_content()

    def switch_to(self):
        """Switch the focus of Selenium to this iframe.

        If an iframe is nested within another iframe, then the driver must
        switch to the parent iframe before it can switch to the child iframe.
        Because of this limitation, every iframe must be declared appropriately
        in the Page object model hierarchy as ``Iframe``s. This will be
        utilized in order to make sure the hierarchy is stepped through in the
        right order.

        To do this, the ``switch_to`` method will first have the driver switch
        focus to the default content to make sure the starting point is
        consistent. After that's done, it makes sure any ancestor ``Iframe``s
        have a chance to switch focus to themselves so the hierarchy of iframes
        is stepped through appropriately. Once that's taken care of, it will
        finally switch focus to itself before returning.
        """
        self.switch_to_default_content()
        if self.iframe_ancestor is not None:
            self.iframe_ancestor.switch_to()
        self.driver.switch_to.frame(self._el)
