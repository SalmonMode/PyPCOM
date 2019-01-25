.. pypcom documentation master file, created by
   sphinx-quickstart on Fri Jun  1 12:44:15 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyPCOM - Python Page Component Object Model
===========================================

PyPCOM is a component based Page Object Model meant to work with Selenium_, that
allows you to break up your pages into logical components with their own
namespace and functionality, while still allowing you to treat every component
as if it were an element. In this model, there is no distinction between a
component and an element. Every component is a class containing its own locator
along with its sub-components and any extra methods you wish to add in.

It even allows you to shorten and simplify the locators you use for sub-
components by letting you have the sub-component search within its parent-
component only. That way you don't have to worry about having incredibly long,
fragile, and hard-to-maintain locators.

Everything is based around classes and descriptors, so the components you make
can be easily inherited from to extend their functionality or reused. This also
makes writing fixtures and tests easier because you can focus more on the
behavior and state of each components, and abstract the cumbersome
details into the code of each component. 

Debugging, abstraction, and documentation are all also easier because you now
have the capability to deal with the different sections of a page individually
and can compartmentalize the logic into different classes and methods.

Are you using a framework with templates to build your frontend, and/or have a
lot of common strutures in the HTML? You can use this model to create component
templates yourself, enabling faster, easier, and more manageable page object
development.

Quick Example
-------------

Login pages are very common, and the functionality is almost always the same.
You can almost always expect a username field, a password field, and a submit
button. Submitting the form should be a straightforward task. So here's how
PyPCOM can be used to set up this structure::

    class Username(PageComponent):
        _find_from_parent = True
        _locator = (By.ID, "username")

    class Password(PageComponent):
        _find_from_parent = True
        _locator = (By.ID, "password")
    
    class LoginForm(PageComponent):
        username = Username()
        password = Password()
        _locator = (By.ID, "loginForm")
        def fill_out(self, username, password, **kwargs):
            self.username = username
            self.password = password

    class LoginPage(Page):
        form = LoginForm()
        def login(self, **credentials):
            self.form.fill_out(**credentials)
            self.form.submit()

Notice that both `fill_out` and `submit` are called on `self.form` inside
`LoginPage`'s `login` method. This is possible because you are able to treat
components both as components with custom defined methods, as well as
:py:class:`~selenium.webdriver.remote.webelement.WebElement` objects. This is
because PyPCOM defers attribute lookups to the
:py:class:`~selenium.webdriver.remote.webelement.WebElement` object (assuming
it can be found) if the component doesn't have the relevant attribute itself.
However, if the :py:class:`~selenium.webdriver.remote.webelement.WebElement`
object doesn't have the attribute, then it shows the component as not having
that attribute.

"What about the fixture?"
^^^^^^^^^^^^^^^^^^^^^^^^^

The fixture would actually be quite easy to create, and it could be made to be
parameterizable. Assuming you're using pytest_, it would just look like this::

    @pytest.fixture
    def login(page, credentials):
        page.login(**credentials)

And with that, you have something that allows you to provide whatever
credentials you want. You can even change the page fixture to give you a
different page object that can handle whatever custom loggic is needed. The
`login` fixture can even be parametrized indirectly for other purposes.

"Couldn't I do that with a normal POM?"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes, but, because of the compartmentalized structure of this approach, if you
need to adjust how you log in because of a different login form (e.g. maybe
there's an additional field, or the locators are different), you can still use
almost everything the `LoginPage` class by inheriting from it and just
replacing the `form` component.

It may not seem like much of a benefit at this small of a scale, but for more
complex pages, it can save you a lot of effort and time.


.. toctree::
   :maxdepth: 4
   :caption: Contents:

   pypcom

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Selenium: http://seleniumhq.org/
.. _pytest: https://docs.pytest.org/