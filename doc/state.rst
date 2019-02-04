.. _state:

State
=====

:py:class:`~pypcom.state.state.State` is used to bundle up multiple
:py:class:`~pypcom.state.expected_attribute.ExpectedAttribute` objects so that
they can all be checked against a :py:class:`~pypcom.component.PageComponent`
with a single `assert` statement. The intent is to achieve the following:

* Maintain the best practice of only using a single `assert` statement per test
    test function/method, while still allowing the test to check multiple things
    at once.
* Speed up and simplify writing complex tests for a page's components.
* Make the code for tests more readable/writable and compact.
* Provide concise, readable output containing all problems should the test fail.

How to Use
----------

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

How It Works
------------

When you first make the :py:class:`~pypcom.state.state.State` object, you pass
it one or more :py:class:`~pypcom.state.expected_attribute.ExpectedAttribute`
objects, which it holds onto. The
:py:class:`~pypcom.state.expected_attribute.ExpectedAttribute` objects are
responsible for knowing how to check the
:py:class:`~pypcom.component.PageComponent` for any problems, and storing them
for later reference. The :py:class:`~pypcom.state.state.State` object runs
through all the :py:class:`~pypcom.state.expected_attribute.ExpectedAttribute`
objects in it's :py:func:`~pypcom.state.State.__eq__` method, and once all the
:py:class:`~pypcom.state.expected_attribute.ExpectedAttribute` objects are
checked against the :py:class:`~pypcom.component.PageComponent` object, the
:py:class:`~pypcom.state.state.State` object checks their results. If it sees
that any problems were found, the comparison will just evaluate to ``False``.

For most testing frameworks, that's as far as it will go. But if you're using
pytest_, then when it comes time for it to print out the failure report, the
:py:class:`~pypcom.state.state.State` object will be used to generate a more
readable failure report message by having it compile the list of problems
reported by each :py:class:`~pypcom.state.expected_attribute.ExpectedAttribute`
object. It's able to do this after the tests have long since been evaluated,
because each of the
:py:class:`~pypcom.state.expected_attribute.ExpectedAttribute` objects hold onto
their findings, and the :py:class:`~pypcom.state.state.State` object keeps a
reference to each of them.
