.. _pages:

Pages
=====

While Components represent the heart and soul of this POM, Pages are what
everything builds to. Pages are what you'll be using in your tests directly
(with some exceptions depending on what's needed), while Components are the
structures that manage the inner workings of the pages, doing all the heavy
lifting. But Pages provide the API that reads like the general behaviors taking
place.

For example, if it's a login page, then your Page should have a `login()`
method that fills out the login form and submits it.

The Pages themselves are what make your tests readable and allow you to tuck
away all the complicated actions involved with a "simple" behavior, so the only
thing left is a single method that reads like a sentence.

The Page classes themselves are the top level of the descriptor hierarchy.
Where Components can be both manager classes and descriptor classes, Pages can
(and should) only be managers, managing the upper most Component structures.

What they look like will vary greatly depending on the page they are meant for,
but here's a quick example for a login page:

.. code-block:: python

    class LoginPage(Page):

        login_form = LoginForm()

        def login(self, username: str, password: str):
            self.login_form.fill_out(username, password)
            self.login_form.submit()
