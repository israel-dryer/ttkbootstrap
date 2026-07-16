Configuration
=============

Every widget's appearance and behavior are held in named **options**, set at
construction and changed afterward with these methods. Each widget page lists the
options that widget accepts; the methods here are how you read and write them.

.. py:method:: configure(cnf=None, **options)
   :noindex:

   Set one or more options after construction. Alias: ``config``. The item
   syntax ``widget["option"] = value`` is equivalent to a one-option
   ``configure``.

   :param options: option/value pairs to set.
   :param cnf: an optional dict of options (merged with ``options``).
   :returns: with no arguments, a dict mapping every option name to its spec
      ``(name, dbName, dbClass, default, current)``; with a single option name and
      no value, that one option's spec; otherwise ``None``.
   :raises TclError: if an option is not one the widget accepts.

.. py:method:: cget(key)
   :noindex:

   Return the current value of one option. Equivalent to ``widget["option"]``.

   :param str key: the option name.
   :returns: the option's current value, as Tk holds it. The Python type follows
      the option — ``str`` for ``text``, ``int`` for ``width`` (even if set from a
      string), ``tuple`` for ``padding``. Options given an object, such as
      ``command`` or ``textvariable``, come back as the *name* Tk registered, not
      the callable or variable you passed.
   :raises TclError: if ``key`` is not an option the widget accepts.

.. py:method:: keys()
   :noindex:

   List the names of the options this widget accepts.

   :returns: the option names.
   :rtype: list[str]

A value read back is Tk's, so its type is Tk's too. To convert one — especially a
Tk boolean, where ``"no"`` and ``"0"`` are truthy strings to Python — use
``getboolean``/``getint``/``getdouble`` from
:doc:`Interpreter </reference/capabilities/interpreter>`.

The option database
-------------------

Tk has a second, older way to set option values: an **option database** of
patterns matched against widget names and classes, which supplies a default for
any option a widget wasn't given explicitly. The methods are ``option_add``,
``option_get``, ``option_clear`` and ``option_readfile``.

It is standard Tk, not ttk, so it does not reach a ttk widget at all — a ttk
Button has no ``background`` option to default; appearance there comes from the
theme and ``bootstyle``. It applies only to the classic tk widgets
(:doc:`Text </reference/api/text>`, :doc:`Canvas </reference/api/canvas>`,
:doc:`Listbox </reference/api/listbox>`, :doc:`Menu </reference/api/menu>`) — and
even there ttkbootstrap paints them with the active theme when they are created,
which overrides the database. To let it through, opt that widget out of theming:

.. code-block:: python

   app.option_add("*Text.background", "#fdf6e3")

   ttk.Text(app)                    # '#ffffff'  -- the theme wins
   ttk.Text(app, autostyle=False)   # '#fdf6e3'  -- the database wins

So it is rarely the right tool here: setting the option on the widget is clearer,
and theming already covers the job it was invented for. It is documented because
the tk widgets make it reachable, and you will meet it in older tkinter code. The
`Tk option manual <https://www.tcl-lang.org/man/tcl8.6/TkCmd/option.htm>`__ has
the pattern syntax and precedence rules.
