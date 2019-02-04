.. _writing_tests:

Using PyPCOM in Automated Tests
===============================

PyPCOM was built around writing end-to-end/UI tests for websites, and, as a
result, comes with several features to make that process easier. While it will
work within any Python testing framework, it was built with pytest_ in mind, so
examples and code snippets will be written assuming your test framework is
pytest_.

The Tests
---------

PyPCOM comes with two handy classes to assist with writing tests:
:py:class:`~pypcom.state.state.State` and
:py:class:`~pypcom.state.expected_attribute.ExpectedAttribute`. Using them, you
can check the state of a component against several things at once with only a
single assert statement. If you're using pytest_, it will also automatically
provide an organized message of all the problems it found in the failure
message.

A :py:class:`~pypcom.state.state.State` is used to compare against the
component, while multiple
:py:class:`~pypcom.state.expected_attribute.ExpectedAttribute` objects are
passed to the :py:class:`~pypcom.state.state.State` when it's instantiated. The
:py:class:`~pypcom.state.expected_attribute.ExpectedAttribute` objects are
responsible for knowing how to check the values off the component and reporting
any problems. The :py:class:`~pypcom.state.state.State` is just there to
manage the comparison of each
:py:class:`~pypcom.state.expected_attribute.ExpectedAttribute` against the
component and generate a failure message for pytest to show in the failure
output.

Quick Example
`````````````

Assuming you have all the page objects and fixtures defined, writing a test can
be as easy as this (assume this is a method inside a test class)::

    def test_some_component(self, page):
        assert page.some_component == State(
            IsDisplayed(),
            Text("My Text"),
            TagName("p"),
        )

If the element was found to be displayed, but had different text and wasn't a
`<p>` tag, you would see a failure that looks something like this:

.. code-block:: none

    Comparing SomeComponent State:
        Text: "Something else" != "My Text"
        TagName: "div" != "p"

The :py:class:`~pypcom.state.expected_attribute.IsDisplayed`,
:py:class:`~pypcom.state.expected_attribute.Text`, and
:py:class:`~pypcom.state.expected_attribute.TagName` classes you see all inherit
from :py:class:`~pypcom.state.expected_attribute.ExpectedAttribute`. PyPCOM
comes with several baked in (see :ref:`provided_expected_attributes` for a full
list), but the system is designed to easily extended so you can add your own.
For more detail on that, check out :ref:`state` or :ref:`expected_attribute`.

.. _pytest: https://docs.pytest.org/
