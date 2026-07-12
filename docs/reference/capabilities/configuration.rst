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
   :returns: when called with a single option name and no value, the option's
      spec ``(name, dbName, dbClass, default, current)``; otherwise ``None``.

.. py:method:: cget(key)
   :noindex:

   Return the current value of one option. Equivalent to ``widget["option"]``.

   :param str key: the option name.
   :returns: the option's current value (always as a string from Tk; cast as
      needed).

.. py:method:: keys()
   :noindex:

   List the names of the options this widget accepts.

   :returns: the option names.
   :rtype: list[str]
