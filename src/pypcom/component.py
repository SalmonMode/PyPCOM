"""This module just contains the base class for components."""

from contextlib import contextmanager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.color import Color
from selenium.common.exceptions import NoSuchElementException

from pypcom import expected_conditions


class CssProperties():
    """CSS properties.

    Lookups can be defined manually for nuanced control over what is returned,
    but if not defined manually, the attribute being looked up will be passed
    as a string to the ``value_of_css_property`` method of the manager class's
    WebElement. If the property's name can't be treated as a Python variable
    name, the name can be passed as a string to the ``get()`` method.
    """

    def __get__(self, instance, owner):
        self._parent = instance
        return self

    def __getattr__(self, name):
        """Treat the attribute name as the name of the CSS value to lookup."""
        return self.get(name)

    def get(self, name):
        """Get the value of the given CSS property."""
        return self._parent.value_of_css_property(name)

    @property
    def color(self):
        """``Color`` object with multiple ways to view color value."""
        return Color.from_string(self._parent.value_of_css_property("color"))

    @property
    def background_color(self):
        """``Color`` object for ``backgorund-color`` CSS property of element."""
        return Color.from_string(
            self._parent.value_of_css_property("background-color"),
        )


class PageComponent(object):
    """The base class for all page components.

    This is the class that all page components should inherit from. Components
    are meant to represent a specific element on a page, and aren't a direct
    reference to the WebElement itself. Instead, an attempt to get the
    WebElement is only ever made if a reference is made to an attribute of the
    component that it doesn't have defined itself (see ``__getattr__`` for
    details).

    If a reference is made to an attribute of the component that the component
    doesn't have, then the component's ``_locator`` attribute is used to get
    the WebElement, and the attribute lookup is deferred to the WebElement. For
    example, if a reference is made to the ``text`` attribute of component
    ``x``, and component ``x`` doesn't have a ``text`` attribute defined for
    it, then ``x`` gets its WebElement and gets the ``text`` attribute of it.

    If the component has no ``_locator`` attribute, an exception is raised
    stating that the component cannot be referenced as an element without one.

    If the WebElement can't be found, an exception is raised stating so.

    If the WebElement is found, but it doesn't have the attribute initially
    referenced, then an exception is raised stating that the component (not the
    WebElement) doesn't have that attribute. All WebElements have a static set
    of attributes, so it's assumed that any referenced attributes that aren't
    part of that set are meant to be defined for that component, and if the
    lookup for it failed in this way, it was because it wasn't properly defined
    in the component's class.

    Components must be descriptors of their owner pages'/components' classes.
    They can be made to be subcomponents of other components to create a tree
    of ownership, accessed through dot-notation. If a component is a manager of
    another component, it can still have its own ``_locator``, which allows it
    to be treated as an element.

    For example, a 'username' component could belong to a 'login_form'
    component, and the 'login_form' component could belong to the page. In
    order to reference the 'username' component, you would say::

        page.login_form.username

    If you want to find the WebElement of the ``PageComponent`` by searching
    from its parent component's element, give the component the
    ``_find_from_parent`` attribute and set it to ``True``.

    Attributes:
        _locator (:obj:`tuple` of :obj:`str`): The locator method and value to
            find the WebElement.
        driver (WebDriver): WebDriver to be used for element lookups and page
            interactions.
        _parent (PageComponent): The instance of the manager class for this
            component.
        _find_from_parent (bool): Whether or not to used the parent
            component's element as the jumping off point to find the element
            from.
    """

    _locator = None
    _find_from_parent = False
    _iframe_ancestor = False
    _is_iframe = False

    css = CssProperties()

    @property
    def _reference_node(self):
        if self._find_from_parent and isinstance(self._parent, PageComponent):
            return self._parent
        return self.driver

    def __get__(self, instance, owner):
        """Grab the driver from the instance.

        Whenever the component is referenced, it should make sure it knows how
        to reference the instance of the manager class that it's being
        referenced through (i.e. it's parent), and it should get the WebDriver
        from that instance. This is how the WebDriver is passed down to
        subcomponents, and how the component ensures it has the tools it needs
        to attempt to find the WebElement it's responsible for, and also so
        that it's subcomponents will be able to access these tools as well.
        Once it has these tools, it just returns itself.

        Args:
            instance (obj): The instance of the manager class that this
                component is a descriptor for (i.e. the parent component).
            owner (obj): The manager class that this component is a descriptor
                for.
        """
        self._parent = instance
        self.driver = self._parent.driver
        return self

    def __set__(self, instance, value):
        """Grab the driver from the instance and send keys to the WebElement.

        Whenever the component is referenced, it should make sure it knows how
        to reference the instance of the manager class that it's being
        referenced through (i.e. it's parent), and it should get the WebDriver
        from that instance. This is how the WebDriver is passed down to
        subcomponents, and how the component ensures it has the tools it needs
        to attempt to find the WebElement it's responsible for, and also so
        that it's subcomponents will be able to access these tools as well. The
        component may not have been referenced in such a way that the
        ``__get__`` had a chance to run, so the ``__set__`` should also be sure
        to grab these tools.

        Once it has the tools, the component tries to send keys to the element
        through the ``send_keys`` method of the WebElement.

        Example::

            page.login_form.username = "my_username"

        Args:
            instance (obj): The instance of the manager class that this
                component is a descriptor for (i.e. the parent component).
            value (str): The keys that should be sent to the WebElement.
        """
        self._parent = instance
        self.driver = self._parent.driver
        if self._locator is None:
            raise AttributeError(
                "Component must have _locator to be treated as an element.",
            )

        with self.possible_iframe_context():
            self.send_keys(value)

    def __getattr__(self, name):
        """Defer the attribute lookup to the WebElement for this component.

        If a reference is made to an attribute of the component that the
        component doesn't have, then the component's ``_locator`` attribute is
        used to get the WebElement, and the attribute lookup is deferred to the
        WebElement. For example, if a reference is made to the ``text``
        attribute of component ``x``, and component ``x`` doesn't have a
        ``text`` attribute defined for it, then ``x`` gets its WebElement and
        gets the ``text`` attribute of it.

        If the component has no ``_locator`` attribute, an exception is raised
        stating that the component cannot be referenced as an element without
        one.

        If the WebElement can't be found, an exception is raised stating so.

        If the WebElement is found, but it doesn't have the attribute initially
        referenced, then an exception is raised stating that the component (not
        the WebElement) doesn't have that attribute. All WebElements have a
        static set of attributes, so it's assumed that any referenced
        attributes that aren't part of that set are meant to be defined for
        that component, and if the lookup for it failed in this way, it was
        because it wasn't properly defined in the component's class.

        Args:
            name (str): Name of the attribute to lookup.
        """
        __tracebackhide__ = True
        with self.possible_iframe_context():
            el = object.__getattribute__(self, "_el")
            try:
                attr = getattr(el, name)
                if callable(attr):
                    def attr_wrapper(*args, **kwargs):
                        # must be wrapped as the callable attribute would
                        # otherwise be evaluated and return, exiting the
                        # context, before actually getting called, which would
                        # make it stale.
                        with self.possible_iframe_context():
                            return attr(*args, **kwargs)
                    return attr_wrapper

                return attr
            except AttributeError:
                raise AttributeError(
                    "'{}' object has no attribute '{}'".format(
                        self.__class__.__name__,
                        name,
                    ),
                )

    @property
    def _el(self):
        """Use the ``_locator`` to get the WebElement."""
        if self._locator is None:
            raise AttributeError(
                "Component must have _locator to be treated as an element.",
            )
        return self._reference_node.find_element(*self._locator)

    def wait_until(self, condition, timeout=10):
        """Wait for up to the allotted time until the condition is met.

        Args:
            condition (str): The condition to be met.
            timout (int): The maximum number of seconds to wait before failing.
        """
        self._wait(True, condition, timeout)

    def wait_until_not(self, condition, timeout=10):
        """Wait for up to the allotted time until the condition is not met.

        Args:
            condition (str): The condition to not be met.
            timout (int): The maximum number of seconds to wait before failing.
        """
        self._wait(False, condition, timeout)

    def _wait(self, wait_bool, condition, timeout=10):
        """Logic for waiting.

        Lookups for expected conditions are either explicitely

        Args:
            wait_bool (bool): Whether the condition should be met or not met.
            condition (str): The condition to be met/not met.
            timout (int): The maximum number of seconds to wait before failing.
        """
        if isinstance(condition, str):
            condition_callable = getattr(
                expected_conditions,
                condition.lower(),
                None,
            )

            if condition_callable is None:
                raise KeyError(
                    "Condition '{}' is not supported".format(condition),
                )

        wait = WebDriverWait(
            driver=self._reference_node,
            timeout=timeout,
            poll_frequency=0.1,
        )
        until_method = wait.until if wait_bool else wait.until_not
        with self.possible_iframe_context():
            until_method(
                condition_callable(self._locator),
            )

    def is_present(self):
        """Query the element to find if it is present or not.

        Make a call to ``is_displayed`` to force a lookup of the element. If a
        ``NoSuchElementException`` is raised, then the element is not present,
        and ``False`` is returned. Otherwise, ``True`` is returned. Only a
        ``NoSuchElementException`` is checked for so that other exceptions can
        still be raised as they shoud be.

        A call to ``is_displayed`` is made, because some behavior of the
        ``PageComponent`` may have been overridden which might cause a
        reference to ``self._el`` to not actually make a reference to the
        ``WebElement`` itself. Making a call to ``is_displayed`` should trigger
        any new behavior for the ``WebElement`` lookup if this is the case, but
        will also work if the standard behavior hasn't been overridden.
        """
        try:
            self.is_displayed()
        except NoSuchElementException:
            return False
        return True

    def remove_from_dom(self):
        """Remove the element from the DOM."""
        self.driver.execute_script(
            "arguments[0].parentElement.removeChild(arguments[0])",
            self._el,
        )

    @property
    def iframe_ancestor(self):
        """First ancestor ``PageComponent`` that is of type ``Iframe``.

        Walk up through the ``PageComponent``'s ancestors, checking for one
        that is of type ``Iframe``. If one is found, return it. If none are
        found, return ``None``.

        This also caches the ancestor the first time it's searched for (as it
        shouldn't be changing), which will speed up further references to it.
        """
        if self._iframe_ancestor is False:
            self._iframe_ancestor = None
            ancestor = self._parent
            while issubclass(ancestor.__class__, PageComponent):
                if ancestor._is_iframe:
                    self._iframe_ancestor = ancestor
                    break
                if hasattr(ancestor, "_parent"):
                    ancestor = ancestor._parent
                else:
                    ancestor = None

        return self._iframe_ancestor

    @contextmanager
    def possible_iframe_context(self):
        """Context manager for interacting with elements possibly in an iframe.

        This is used to automatically handle switching the focus to an iframe
        before some actions are done, and then switching back to the default
        content frame (page) once those actions are completed.

        This was made specifically for performing the repetitive task of
        managing switching focus to an iframe and back. This was also made to
        make sure that, should an exception be raised, focus is switched back
        to the default content without interferring with how the exception is
        handled, and without having to put a bunch of try/except/finally blocks
        everywhere.
        """
        if self.iframe_ancestor:
            self.iframe_ancestor.switch_to()
        yield
        if self.iframe_ancestor:
            self.driver.switch_to.default_content()
