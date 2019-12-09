.. _iterables:

Iterable Structures
===================

Sometimes you'll have some sort of structure that either doesn't have
universally consistent series of data, or it just has an immense number of
items. For example, a table of data with many rows.

Just building out all the components for each possible item in the series
would be either extremely difficult (if not impossible), or just plain tedious.
Luckily, there's a better way.

First, let's say we have a table of cars, where each row is an individual car,
and their make, model, year, and color are provided, each in their own column.
In this table, you can select each row, and delete them, thus deleting the
record of that car. There's also a form just before this table, through which,
new cars can be added to the table. Let's also say that every time the page is
loaded, the table is empty, so if we want to have any cars listed, we have to
add them ourselves.

.. rubric:: The HTML

Here's some example HTML to represent this (let's also assume there's magic
JavaScript that will just make this work flawlessly):

.. literalinclude:: /example_code/car_table.html
    :language: html

.. rubric:: The Tests

Now that we have the table's HTML, we can get started on the code. To figure
what our bottom-level code should be, let's look at how we want the tests to
look. Here's one example of how these could look:

.. literalinclude:: /example_code/ideal_car_tests.py
    :language: python

That looks pretty straightforward and easy to read, but the question is how to
achieve that. To find out, let's keep working backwards.

.. rubric:: The Page

We can start by looking at the page class itself. This serves as the top-level
abstraction for how we interact with the page in terms of behavior, so it's
important that it provides us with a readable and useable API. It should have
methods that fully describe what were doing, so anyone reading it can follow
along:

.. literalinclude:: /example_code/car_table_page.py
    :language: python

.. rubric:: The Add Form

The code is starting to take shape, and this is pretty self-explainatory, so
let's dig deeper, and look into how the cars get added:

.. literalinclude:: /example_code/add_car_form_components.py
    :language: python

Now it's starting to get a bit more complicated, as it combines multiple
advanced concepts. It first uses a generic component that overrides the normal
`__set__` and `_el` logic so that `Select` can be used while the API it
provides remains consistent with other form control elements. Further down, it
uses a custom wait function that has it rely on its parent (in this case, the
page itself) to see if the number of shown cars has changed.

This last step where it waits for the change in car count is essential so that
anything leveraging that `add_car` method doesn't have to worry about any race
conditions created by JavaScript that hasn't had a chance to run (i.e. a change
was made to the DOM, so the thing changing it should wait for the DOM change to
complete before moving on).

.. rubric:: The Table

This is only one half of the page, though, so let's look at the other half and
see what's going on inside the table component itself:

.. literalinclude:: /example_code/car_table_components.py
    :language: python

This does a small trick where instances of `CarItem` are given a reference to
the driver, their parent table component, and an index for the row they
represent. They aren't hooked up like a normal descriptor-based component,
but they don't need to be as the driver and parent reference was passed down
explicitely. All the parent table component needs to do is figure out how many
items (i.e. rows) it has, and create that many instances of `CarItem`, giving
each one the appropriate index (i.e. 0 to n), a reference to itself, and the
driver. That's all the information each instance needs to still function
properly (this is also why the `_locator` is a `property`).

Down at the bottom, there's also `car_items` and `cars`, each one providing
something similar, but very different. Having `car_items` on its own gives us
an easy means to access those components in the DOM, and giving them their own
properties that have meaningful values allows us to get fancier.

.. rubric:: The Car

With that in mind, let's take a look at the final chunk of code, and see the
custom data types and enumerators that make this whole operation tick:

.. literalinclude:: /example_code/car.py
    :language: python

This lets us consider each car's data independently of any implementation that
uses this data by giving those implementations a means to store and work with
the data in a common shape. We no longer have to worry about how a specific
method will be expecting the information for a given car, how a method might
return such information, or how to compare one car to another, because it's all
handled through this class, and the supporting classes are enumerators to help
streamline the development process. They act as a common language for every
piece to talk to the others with, and allow us to write such simple tests as
the ones above.

The `__eq__` in particular helps with several aspects of this example. It
allows the comparisons with the instances of `CarItem`, which in turns allows
for things like `self.car_items.index(car)`, because Python leverages `__eq__`
for a lot of common operations.
