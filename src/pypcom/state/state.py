from pypcom import PC


class State(object):
    """The expected state of the object being checked.

    Instances of this class can be created with multiple expected attributes to
    be checked against the test subject object all at once when compared through
    ``__eq__``. For each expected attribute that is passed, each will be
    utilized even if others had problems. When all are used, the ``State``
    object will check their results and return ``True`` if all passed, or
    ``False`` if any had a problem.

    Each expected attribute is responsible for handling the logic for how to
    compare against the test subject. If they find a problem, they are
    responsible for storing that problem in their ``self._problems`` list
    through their ``self.add_problem`` method, which the ``State`` object will
    check through their ``self.get_problems`` method once it has used all of its
    expected attributes. The expected attributes can also just raise an
    ``AssertionError`` in their ``compare`` method, and the ``State`` object
    will catch it and include it in the reported problems.

    When the ``State`` has all the reported problems, it will bundle them up
    into a readable string accessed through ``self.get_report()``, so they can
    all be reported as one failure. This is meant for pytest to access during
    its ``pytest_assertrepr_compare`` hook, so that a readable representation of
    the failure can be provided.

    Here's an example of how it can be used::

        def test_my_component(self, page):
            assert page.component.my_form.my_input == State(
                IsPresent(),
                IsDisplayed(),
                IsEnabled(),
                TagName("input"),
                Type("text"),
            )
    """

    def __init__(self, *expected_attributes):
        self._expected_attributes = expected_attributes
        self._problems = []
        self._other_class_name = None

    def __eq__(self, other):
        self._other_class_name = other.__class__.__name__
        for attr in self._expected_attributes:
            attr.safe_compare(other)
            self.add_problems_of_attr(attr)
        if self._problems:
            return False

    def add_problems_of_attr(self, attr):
        """Grab and store the reported problems of the ``ExpectedAttribute``.

        These will be used later to generate a proper failure message for
        ``pytest`` to show in its output. This structure helps make iteration
        and truthy evaluation easier.

        Args:
            attr (obj): The ``ExpectedAttribute`` to pull the problems from.
        """
        problems = attr.get_problems()
        if problems:
            self._problems.append(attr)

    def get_pytest_failure_report_repr(self):
        """Get the failure report repr for ``pytest`` to display in its output.

        Run through all the stored problems and their associated
        ``ExpectedAttribute``s, and buld the failure message that ``pytest``
        will show in its output. For each problem of each associated
        ``ExpectedAttribute``, there will be a line showing the
        ``ExpectedAttribute``'s name and the problem's message. For example::

            Comparing AboutLink State:
                Text: "Contact Us" != "About Us"
                Href: "https://mysite.com/contact" != "https://mysite.com/about"

        This is designed to allow flexibility in what shows up in the failure
        message.
        """
        report = [
            "Comparing {} State:".format(self._other_class_name),
        ]
        report_messages = self.get_pytest_failure_report_messages()
        report.extend(report_messages)
        return report

    def get_pytest_failure_report_messages(self):
        """Get a list of all the report messages from all the problems.

        This is designed to be flexible, so that custom problems, or custom ways
        for ``ExpectedAttribute`` to report their problems can easily be made.

        For ``ExpectedAttribute`` objects, this will look for a
        ``get_report_messages`` method, and will add whatever it returns to the
        list of report messages for this ``State``. It expects a
        ``list``/``tuple`` of strings, but can handle a single string. If it
        doesn't have such a method, this will just look at each problem
        associated with it.
        """
        report_messages = []
        for attr in self._problems:
            if hasattr(attr, "get_report_messages"):
                messages = attr.get_report_messages()
                if isinstance(messages, str):
                    messages = [messages]
                report_messages.extend(messages)
                continue
        return report_messages
