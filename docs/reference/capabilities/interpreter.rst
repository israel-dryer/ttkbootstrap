Interpreter
===========

Tkinter is a thin layer over a Tcl interpreter, and every widget carries a handle
to it. Most of the time that boundary is invisible. These methods are the places
you cross it deliberately: turning Tcl's values into Python ones, exposing a
Python function so Tcl can call it, and asking which Tk you are running on.

Converting Tk values
--------------------

Tk hands some values back as strings, and its idea of a boolean is broader than
Python's — ``"yes"``, ``"true"``, ``"1"`` and ``"on"`` are all true. These
helpers apply Tk's rules, so use them instead of ``int()`` or truth-testing a
string: in Python every non-empty string is truthy, **including** ``"0"`` and
``"false"``.

.. py:method:: getboolean(s)
   :noindex:

   Convert a Tk boolean to a Python ``bool``.

   :param s: a Tk boolean — ``"yes"``/``"no"``, ``"true"``/``"false"``,
      ``"on"``/``"off"``, ``1``/``0``.
   :returns: the value.
   :rtype: bool
   :raises ValueError: if ``s`` isn't a recognized boolean.

.. py:method:: getint(s)
   :noindex:

   Convert a Tk value to a Python ``int``.

   :param s: the value to convert.
   :rtype: int

.. py:method:: getdouble(s)
   :noindex:

   Convert a Tk value to a Python ``float``.

   :param s: the value to convert.
   :rtype: float

Exposing a callback to Tcl
--------------------------

A few Tk options take a *Tcl command name* rather than a Python callable — most
notably ``validatecommand``, which also needs substitution codes like ``%P``.
``register`` wraps a Python function as a Tcl command and gives you back its
name.

.. code-block:: python

   check = app.register(lambda proposed: proposed.isdigit())
   ttk.Entry(app, validate="key", validatecommand=(check, "%P"))

:doc:`Validation </user-guide/feature-guides/validation>` does this for you —
reach for ``register`` only when you are wiring a Tcl-level option by hand.

.. py:method:: register(func, subst=None, needcleanup=1)
   :noindex:

   Register a Python callable as a Tcl command.

   :param func: the callable to expose.
   :param subst: an optional callable applied to the arguments first.
   :param needcleanup: whether to delete the command when the widget is destroyed.
   :returns: the Tcl command name to hand to the option.
   :rtype: str

.. py:method:: deletecommand(name)
   :noindex:

   Delete a Tcl command created by ``register``, releasing the Python callable.
   Calling the name afterward raises ``TclError``.

   :param str name: the command name ``register`` returned.
   :returns: ``None``.

Which Tk is this
----------------

.. py:method:: info_patchlevel()
   :noindex:

   The exact Tk version behind this interpreter — useful when a feature is gated
   on it.

   :returns: a version tuple ``(major, minor, micro, releaselevel, serial)``;
      ``str()`` of it gives ``"8.6.17"``.

.. seealso::

   - :doc:`Configuration </reference/capabilities/configuration>` — reading option
     values, which is where Tk's types usually surface.
   - :doc:`Validation </user-guide/feature-guides/validation>` — the wrapper
     around ``register`` you normally want.
