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
