.. _components:

Components
==========

These are the heart of soul of this framework.

At a very basic level, components are just classes that have a locator for a
specific element, and get used as descriptors in pages or other components.
When referenced, they can be treated as though you are referencing the
:py:class:`~selenium.webdriver.remote.webelement.WebElement` they're associated
with. That means you can reference their `.text` property or `.is_displayed()`
on them. You can even do this for a component that has sub-components of its
own.

But they offer much more convenience than that. You can read below on how they
work and how you can get the most out of them.

Defining
--------

Defining a component is ver straightforward. All you need to do is make a class
that inherits from :py:class:`PageComponent` (or :py:class:`PC` for something
shorter), and give it a locator that can be passed to `.find_element()`. It
would look something like this::

    class MyComponent(PC):
        _locator = (By.ID, "my-id")

Adding Sub-Components
`````````````````````

If you want to add sub-components to it, it's identical to adding a component
to the page class. You just need to add it like a decorator::

    class MySubComponent(PC):
        _locator = (By.ID, "my-other-id")

    class MyComponent(PC):
        _locator = (By.ID, "my-id")
        my_sub_component = MySubComponent()

To put `MyComponent` in a page class, you can then just add it in like you
normally would::

    class MyPage(Page):
        my_component = MyComponent()

You can then reference the normal
:py:class:`~selenium.webdriver.remote.webelement.WebElement` attributes/methods
and the sub-component like this::

    page.my_component.is_displayed()
    page.my_component.text
    page.my_component.my_sub_component.is_displayed()
    page.my_component.my_sub_component.text

Adding Custom Methods
`````````````````````

Adding in custom methods is just as easy::

    class MySubComponent(PC):
        _locator = (By.ID, "my-other-id")

        def do_more_things(self):
            # do more stuff
            pass

    class MyComponent(PC):
        _locator = (By.ID, "my-id")
        my_sub_component = MySubComponent()

        def do_something(self):
            # do stuff
            pass

They can now be used just like the normal attributes and methods provided by
:py:class:`~selenium.webdriver.remote.webelement.WebElement` and
:py:class:`PageComponent`. This also doesn't change how it works normally, so
long as you don't add any sub-components or custom methods that would interfere
with the normal :py:class:`~selenium.webdriver.remote.webelement.WebElement` or
:py:class:`PageComponent` methods/attributes.


Enterring Text
--------------

Enterring text is easy. For a given component, the locator just needs to point
to the actual `input` element, and then you can invoke
:py:func:`~selenium.webdriver.remote.webelement.WebElement.send_keys` through
the `=` operator like this::

    page.my_form.my_input = "something"

Advanced
````````

If you need to change how this behavior works, you can override the `__set__`
method in your component. Just make sure you look at how it works normally, so
you basically duplicate it, and only modify the part where it invokes
:py:func:`~selenium.webdriver.remote.webelement.WebElement.send_keys` to make
sure it continues working as it needs to.

This approach will likely change in the future to provide a more convenient
hook to override, but any additional hook will not break a custom `__set__`
implementation if it copies the current one.

Waiting
-------

Waiting is simple, too. You can either call
:py:func:`PageComponent.wait_until()` or
:py:func:`PageComponent.wait_until_not()` on the component you want to perform
the wait on, and pass it a string for the condition you want to wait for. The
three available conditions are `"present"`, `"visible"`, and `"clickable"`.

Here's a quick example of its usage::

    page.component.wait_until("visible", timeout=5)

It accepts strings that correspond to the normal expected conditions you've
seen. But you can also reference expected conditions you've defined yourself
and attached to the :py:class:`PageComponent` in its `_expected_condition`
attribute. Here's an example of how it can be set up::

    def custom_visible_condition(component):
        def callable(driver):
            return component.is_displayed()
        return callable

    class MyComponent(PC):
        _locator = (...)
        _expected_conditions = {
            "custom_visible": custom_visible_condition,
        }

and here's how you'd use it::

    page.my_component.wait_until("custom_visible")

You can also pass in the callable directly, like this::

    page.my_component.wait_until(custom_visible_condition)

If you need to, you can provide additional keyword arguments for more flexible
logic. Of course, you'll have to make sure you can handle it properly within
the callable. For example, if you have some more advanced component structures
and need to perform a query that goes beyond normal selenium logic, you could
implement a `query` method (with whatever name you want, of course) and provide
the necessary query details at the time the wait is executed. This might be
how your callable looks::

    def custom_query_condition(component, **query_details):
        def callable(driver):
            return component.query(**query_details)
        return callable

Then you could add it to the `_expected_conditions` dict attribute of that
component, maybe as "complex_component_present", and invoke it like this::

    page.my_component.wait_until("complex_component_present", **query_details)

Sub-Components and `_find_from_parent`
--------------------------------------

Often, you will find yourself with long and convoluted selectors, simply
because the element you want to find is in some heavily nested node, and you
have to repeat parts of your selector in many sub-components.

PyPCOM offers a solution to this that lets you simply search for a
sub-component's associated
:py:class:`~selenium.webdriver.remote.webelement.WebElement` within its parent
component's :py:class:`~selenium.webdriver.remote.webelement.WebElement` by
calling
:py:func:`~selenium.webdriver.remote.webelement.WebElement.find_element` on
that instead of the driver. This allows you to give the sub-component a locator
that is relative to its parent component's
:py:class:`~selenium.webdriver.remote.webelement.WebElement`, so you don't have
to keep repeating the common parts of the locator, and can instead create a
simpler, cleaner, and more appropriate locator than you might not have been
able to otherwise.

To use it, all you have to do is set `_find_from_parent` to `True` in the class
definition of the sub-component. The parent components don't need to be aware
of this, so long as they have a `_locator` of their own.

Simple Example
``````````````

Let's say you have the following collection of elements somewhere in your page:

.. code-block:: html

    <div class='some-area'>
        <div class='content-section'>
            <img src='iamges/myImage.png' />
            <p class='content'>Some text content.</p>
            <a href='something.html'>Some Link</a>
        </div>
    </div>

To reliably find these elements, you might have to use a very lengthy locator
involving references to both parent elements. For example::

    class MyImage(PC):
        _locator = (By.CSS_SELECTOR, "div.some-area div.content-section img")

    class SomeContent(PC):
        _locator = (By.CSS_SELECTOR, "div.some-area div.content-section p")

    class SomethingLink(PC):
        _locator = (By.CSS_SELECTOR, "div.some-area div.content-section a")

    class SomeContentSection(PC):
        _locator = (By.CSS_SELECTOR, "div.some-area div.content-section")
        my_image = MyImage()
        some_content = SomeContent()
        something_link = SomethingLink()

    class SomeArea(PC):
        _locator = (By.CSS_SELECTOR, "div.some-area")
        some_content_section = SomeContentSection()

If you had to do that for several elements throughout all of your pages, that
would get tedious very quickly and would involve a lott of repeating yourself.
Not to mention, this would also make all those locators fragile, and if they
break, it would take quite a while to fix each one.

Using `_find_from_parent` cuts out all that repetition and compartmentalizes
your locator logic::

    class MyImage(PC):
        _find_from_parent = True
        _locator = (By.TAG_NAME, "img")

    class SomeContent(PC):
        _find_from_parent = True
        _locator = (By.TAG_NAME, "p")

    class SomethingLink(PC):
        _find_from_parent = True
        _locator = (By.TAG_NAME, "a")

    class SomeContentSection(PC):
        _find_from_parent = True
        _locator = (By.CSS_SELECTOR, "div.content-section")
        my_image = MyImage()
        some_content = SomeContent()
        something_link = SomethingLink()

    class SomeArea(PC):
        _locator = (By.CSS_SELECTOR, "div.some-area")
        some_content_section = SomeContentSection()

For something a little more complex, check out :ref:`generic`, or the other
examples in :ref:`advanced`.

Deferring Attribute Lookups (Or "How does it do that?")
-------------------------------------------------------

Why Descriptors?
````````````````

PyPCOM works using descriptors for the components, but the only things it
really uses that for are making sure a reference to the `driver` and each
component's parent component/page is accessible, and to allow for convenient
value setting.

PyPCOM needs to make sure that, before it does anything, as a component is
referenced (either through `__get__` or `__set__`), it grabs the reference to
the `driver` from the managing instance, storing a reference to both the driver
and the instance in the component itself so that they can be referenced later
on. For example, if you were to reference something like::

    page.some_component.another_component = "some text"

`some_component` would be referenced through `__get__` and get a reference to
the driver from `page`. It would also store a reference to `page` as its
parent. `another_component` would then be referenced through `__set__` and get
a reference to the driver from `some_component`. It would also store a
reference to `some_component` as its parent.

Descriptors also means classes will be used, so you can define custom behavior,
inherit behavior from other components, and re-use components as much as you
want.

How does it support selenium methods/attributes like it does?
`````````````````````````````````````````````````````````````

PyPCOM relies on the default attribute lookup behavior of objects in Python. If
a class instance, or the class itself does not have a certain attribute
defined, then Python calls the object's `__getattr__` method (assuming it has
one defined).

For components, when you reference an attribute of them, if the component
instance has no such attribute, and neither does its class, then the component
instance attempts to find its associated
:py:class:`~selenium.webdriver.remote.webelement.WebElement` and get the
attribute from there. If the
:py:class:`~selenium.webdriver.remote.webelement.WebElement` doesn't have that
attribute, then PyPCOM will tell you that the component doesn't have the
attribute. If the component doesn't have a `_locator` defined, or the
:py:class:`~selenium.webdriver.remote.webelement.WebElement` can't be located,
PyPCOM will raise an appropriate error.

Because there is a finite, established set of
:py:class:`~selenium.webdriver.remote.webelement.WebElement` attributes, PyPCOM
assumes that you must be looking for a component's attributes if it can't find
them on the :py:class:`~selenium.webdriver.remote.webelement.WebElement`. As a
result, when it can't find an attribute, the error it raises will tell you that
the component was the one without the attribute. This does not mean that it
didn't try to find the attribute on the
:py:class:`~selenium.webdriver.remote.webelement.WebElement`
