.. _expected_attribute:

ExpectedAttribute
=================

The :py:class:`~pypcom.state.expected_attribute.ExpectedAttribute` objects
serve as a means of compartmentalizing the logic for both how to check for
something specific against a :py:class:`~pypcom.component.PageComponent`, and
how to summarize any problems found. You can pass any number of
:py:class:`~pypcom.state.expected_attribute.ExpectedAttribute` objects to a
:py:class:`~pypcom.state.state.State` object when you create it.

PyPCOM offers plenty of
:py:class:`~pypcom.state.expected_attribute.ExpectedAttribute` classes out of
the box, which can be found below. But the system is designed to be customizable
so you can inherit from the
:py:class:`~pypcom.state.expected_attribute.ExpectedAttribute` class and define
your own checks along with how to report them.

Defining Your Own
-----------------

In order to define your own
:py:class:`~pypcom.state.expected_attribute.ExpectedAttribute`, all you need to
do is make a class that inherits from
:py:class:`~pypcom.state.expected_attribute.ExpectedAttribute`, and then give it
an ``__init__`` and ``compare`` method.

The ``__init__`` method can be used to accept any expected values you want the
object to check for.

The ``compare`` method will be passed a reference to the
:py:class:`~pypcom.component.PageComponent` when it gets called by the
:py:class:`~pypcom.state.state.State` object during the actual comparison. In
that method, there's three ways you can track problems you find, all of which
are equally recommended (so use whichever you find most appealing):

#. You can manually add problems you find using
   :py:func:`~pypcom.state.expected_attribute.ExpectedAttribute.add_problem`

#. Use a standard ``assert`` statement, with an failure message attached (e.g.
   ``assert True is False, "True is not False"``)

#. Raise an ``AssertionError`` manually with a provided failure message (e.g.
   ``raise AssertionError("some failure message")``)

If you choose the first option, it's recommended that you stick with
``AssertionError``s, or at least provide an object with a ``.message`` attribute
so that :py:class:`~pypcom.state.expected_attribute.ExpectedAttribute` can find
the problem's message in the way it normally does.

Here's a quick example of a custom
:py:class:`~pypcom.state.expected_attribute.ExpectedAttribute`, which is
provided already in PyPCOM (with the docstrings removed, however)::

    class IsDisplayed(ExpectedAttribute):
        _msg = {
            True: "Element is not displayed when it should be",
            False: "Element is displayed when it shouldn't be",
        }
        def __init__(self, expected=True):
            self._expected = bool(expected)
        def compare(self, other):
            assert other.is_displayed() is self._expected, self._msg[self._expected]

.. _provided_expected_attributes:

Provided ExpectedAttribute Classes
----------------------------------

.. automodule:: pypcom.state.expected_attribute
    :members:
