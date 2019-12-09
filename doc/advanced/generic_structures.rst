.. _generic:

Generic Component structures
============================

Let's say you have a common structure for your form control elements in all
your forms where each field has an `<input>` element and a `<label>` bundled
inside its own `<div>`. It would look something like this:

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

That XPATH would locate a `<div>` that both has a single class of `form-field`
and also contains an `<input>` with the desired `id`. It won't find the
`<input>` itself; it just finds the right `<div>` that contains it. But that's
intended. This way we know we found the element that contains only that
`<input>` and its `<label>`, and we can let the `FormField` class hold all the
common logic.

