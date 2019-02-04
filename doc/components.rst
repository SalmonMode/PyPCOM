..  _components:

Components
==========

These are the heart of soul of this framework.

At a very basic level, components are just classes that have a locator for a
specific element, and get used as descriptors in pages or other components. When
referenced, they can be treated as though you are referencing the
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

If you want to add sub-components to it, it's identical to adding a component to
the page class. You just need to add it like a decorator::

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

This approach will likely change in the future to provide a more convenient hook
to override, but any additional hook will not break a custom `__set__`
implementation if it copies the current one.

Waiting
-------

Waiting is simple, too. You can either call :py:func:`PageComponent.wait_until()`
or :py:func:`PageComponent.wait_until_not()` on the component you want to
perform the wait on, and pass it a string for the condition you want to wait
for. The three available conditions are `"present"`, `"visible"`, and
`"clickable"`. More will be added soon, along with a system for passing custom
condition callables.

Here's a quick example of its usage::

    page.component.wait_until("visible", timeout=5)

Sub-Components and `_find_from_parent`
--------------------------------------

Often, you will find yourself with long and convoluted selectors, simply because
the element you want to find is in some heavily nested node, and you have to
repeat parts of your selector in many sub-components.

PyPCOM offers a solution to this that lets you simply search for a
sub-component's associated
:py:class:`~selenium.webdriver.remote.webelement.WebElement` within its parent
component's :py:class:`~selenium.webdriver.remote.webelement.WebElement` by
calling :py:func:`~selenium.webdriver.remote.webelement.WebElement.find_element`
on that instead of the driver. This allows you to give the sub-component a
locator that is relative to its parent component's
:py:class:`~selenium.webdriver.remote.webelement.WebElement`, so you don't have
to keep repeating the common parts of the locator, and can instead create a
simpler, cleaner, and more appropriate locator than you might not have been able
to otherwise.

To use it, all you have to do is set `_find_from_parent` to `True` in the class
definition of the sub-component. The parent components don't need to be aware of
this, so long as they have a `_locator` of their own.

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

To reliably find these elements, you might havee to use a involving references
to both parent elements. For example::

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

Advanced Example
````````````````

This also allows for making complex, generic component structures that can be
re-used in several places. Let's say you have a common structure for your form
control elements in all your forms where each field has an `<input>` element and
a `<label>` bundled inside its own `<div>`. It would look something like this:

.. code-block:: html

    <div class='form-field'>
        <label for='first-name'>First Name:</label>
        <input id='first-name' name='first-name' />
    </div>
    <div class='form-field'>
        <label for='last-name'>Last Name:</label>
        <input id='last-name' name='last-name' />
    </div>

This would be tedious to have to define a label and input component for every
field in your site. But you could create a generic structure like this that you
could reuse::

    class Label(PC):
        _find_from_parent = True
        _locator = (By.TAG_NAME, "label")

    class Input(PC):
        _find_from_parent = True
        _locator = (By.TAG_NAME, "input")

    class FormField(PC):
        label = Label()
        input = Input()

        def __set__(self, instance, value):
            self._parent = instance
            self.driver = self._parent.driver
            self.input = value

With that, you could just inherit from `FormField` to make a new class for
each field, and it would even let you assign a value to the input by setting the
field component itself (i.e. `page.form.my_field = "something"`). You could even
get a little fancy with the locator to make sure you always find the right
field `<div>`::

    class FirstNameField(FormField):
        _locator = (
            By.XPATH,
            (
                "//div[contains(concat(' ', @class, ' '), ' form-field ')]"
                "[input[@id='first-name']]"
            ),
        )

    class LastNameField(FormField):
        _locator = (
            By.XPATH,
            (
                "//div[contains(concat(' ', @class, ' '), ' form-field ')]"
                "[input[@id='last-name']]"
            ),
        )

That XPATH would locate a `<div>`` that both has a single class of `form-field`,
and also contains an `<input>` with the desired `id`. It won't find the
`<input>` itself; it just finds the right `<div>` that contains it. But that's
intended. This way we know we found the element that contains only that
`<input>` and its `<label>`, and we can let the `FormField` class hold all the
common logic.

Deferring Attribute Lookups (Or "How does it do that?")
-------------------------------------------------------

Why Descriptors?
````````````````

PyPCOM works using descriptors for the components, but the only things it really
uses that for are making sure a reference to the `driver` and each component's
parent component/page is accessible, and to allow for convenient value setting.

PyPCOM needs to make sure that, before it does anything, as a component is
referenced (either through `__get__` or `__set__`), it grabs the reference to
the `driver` from the managing instance, storing a reference to both the driver
and the instance in the component itself so that they can be referenced later
on. For example, if you were to reference something like::

    page.some_component.another_component = "some text"

`some_component` would be referenced through `__get__` and get a reference to
the driver from `page`. It would also store a reference to `page` as its parent.
`another_component` would then be referenced through `__set__` and get a
reference to the driver from `some_component`. It would also store a reference
to `some_component` as its parent.

Descriptors also means classes will be used, so you can define custom behavior,
inherit behavior from other components, and re-use components as much as you
want.

How does it support selenium methods/attributes like it does?
`````````````````````````````````````````````````````````````

PyPCOM relies on the default attribute lookup behavior of objects in Python. If
a class instance, or the class itself does not have a certain attribute defined,
then Python calls the object's `__getattr__` method (assuming it has one
defined).

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