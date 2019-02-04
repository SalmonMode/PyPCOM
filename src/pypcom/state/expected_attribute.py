class ExpectedAttribute(object):

    _problems = None
    name = None

    def get_name(self):
        """The name of the attribute to be used in the failure message."""
        return self.name or self.__class__.__name__

    def safe_compare(self, other):
        """Compares, but catches ``AssertionError`` to add to problems.

        Args:
            other (obj): The object to check for something expected.
        """
        try:
            self.compare(other)
        except AssertionError as e:
            self.add_problem(e)

    def compare(self, other):
        """Defines how to check the other object for something expected.

        This is responsible for either raising an ``AssertionError`` or adding
        a problem through ``add_problem``, should the expected not be found.

        Args:
            other (obj): The object to check for something expected.
        """
        raise NotImplementedError(
            "Must be overridden to define how to check the attribute.",
        )

    def add_problem(self, problem):
        """Add a problem to the list of problems for this attribute.

        Args:
            problem (obj): Some problem found with the state of the test
                subject.
        """
        if self._problems is None:
            self._problems = []
        self._problems.append(problem)

    def get_problems(self):
        """Get all problems for this attribute."""
        return self._problems or ()

    def get_report_messages(self):
        """Get all the strings that should be included in the failure report."""
        report_messages = []
        attr_name = self.get_name()
        for problem in self.get_problems():
            if hasattr(problem, "get_report_message"):
                report_messages.append(problem.get_report_message())
                continue
            msg = "    {}: {}".format(
                attr_name,
                self.get_problem_message(problem),
            )
            report_messages.append(msg)
        return report_messages

    def get_problem_message(self, problem):
        """Get details about the problem to show in the failure report.

        If the problem doesn't have a ``message` attribute or it does and it's
        just a blank string, then fall back to its ``args`` attribute and grab
        the first line from the first thing in there.

        Args:
            problem (obj): Some problem found with the state of the test
                subject.
        """
        if hasattr(problem, "message") and problem.message:
            return problem.message
        return problem.args[0].split("\n")[0]


class IsPresent(ExpectedAttribute):
    """Checks if the component is currently present on the page or not.

    Args:
        expected (bool): Whether or not the element should be present.
    """

    _msg = {
        True: "Element is not present when it should be",
        False: "Element is present when it shouldn't be",
    }

    def __init__(self, expected=True):
        self._expected = bool(expected)

    def compare(self, other):
        """Check if the element is present or not.

        The output will be one of the following::

            IsPresent: Element is not present when it should be
            IsPresent: Element is present when it shouldn't be
        """
        assert other.is_present() is self._expected, self._msg[self._expected]


class IsDisplayed(ExpectedAttribute):
    """Checks if the component is currently displayed on the page or not.

    Args:
        expected (bool): Whether or not the element should be displayed.
    """

    _msg = {
        True: "Element is not displayed when it should be",
        False: "Element is displayed when it shouldn't be",
    }

    def __init__(self, expected=True):
        self._expected = bool(expected)

    def compare(self, other):
        """Check if the element is displayed or not."""
        assert other.is_displayed() is self._expected, self._msg[self._expected]


class IsEnabled(ExpectedAttribute):
    """Checks if the component is currently enabled on the page or not.

    Args:
        expected (bool): Whether or not the element should be enabled.
    """

    _msg = {
        True: "Element is not enabled when it should be",
        False: "Element is enabled when it shouldn't be",
    }

    def __init__(self, expected=True):
        self._expected = bool(expected)

    def compare(self, other):
        """Check if the element is enabled or not."""
        assert other.is_enabled() is self._expected, self._msg[self._expected]


class TagName(ExpectedAttribute):
    """Checks if the component has a certain tag name or not.

    Args:
        expected (bool): What tag name the element should have.
    """

    def __init__(self, expected=True):
        self._expected = expected

    def compare(self, other):
        """Check the element's tag name."""
        other_tag_name = other.tag_name
        msg = "'{}' is not '{}'".format(
            other_tag_name,
            self._expected,
        )
        assert other_tag_name == self._expected, msg


class Href(ExpectedAttribute):
    """Checks if the component has a certain href value or not.

    Args:
        expected (bool): What href value the element should have.
    """

    def __init__(self, expected=True):
        self._expected = expected

    def compare(self, other):
        """Check the element's href."""
        other_href = other.get_attribute("href")
        msg = "'{}' is not '{}'".format(
            other_href,
            self._expected,
        )
        assert other_href == self._expected, msg


class Text(ExpectedAttribute):
    """Checks if the component has certain text or not.

    Args:
        expected (bool): What text the element should have.
    """

    def __init__(self, expected=True):
        self._expected = expected

    def compare(self, other):
        """Check the element's text."""
        other_text = other.text
        msg = "'{}' is not '{}'".format(
            other_text,
            self._expected,
        )
        assert other_text == self._expected, msg


class Placeholder(ExpectedAttribute):
    """Checks if the component has a certain placeholder value or not.

    Args:
        expected (bool): What placeholder the element should have.
    """

    def __init__(self, expected=True):
        self._expected = expected

    def compare(self, other):
        """Check the element's placeholder."""
        other_placeholder = other.get_attribute("placeholder")
        msg = "'{}' is not '{}'".format(
            other_placeholder,
            self._expected,
        )
        assert other_placeholder == self._expected, msg


class Type(ExpectedAttribute):
    """Checks if the component is of a certain type or not.

    Args:
        expected (bool): What type the element should be.
    """

    def __init__(self, expected=True):
        self._expected = expected

    def compare(self, other):
        """Check the element's type."""
        other_type = other.get_attribute("type")
        msg = "'{}' is not '{}'".format(
            other_type,
            self._expected,
        )
        assert other_type == self._expected, msg
