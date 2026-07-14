Variables
=========

A **variable** is a typed value holder that binds to a widget: set the variable
and the widget updates; edit the widget and the variable updates. Pass one as
``textvariable=`` (an Entry, Label, or Combobox), as ``variable=`` (a Checkbutton,
Radiobutton, or Scale), and read it back with ``.get()``. The
:doc:`Variables guide </user-guide/feature-guides/variables>` shows them in use;
this page is the API spec.

The variable classes
--------------------

Each class wraps a value of one Python type and coerces ``get()`` to it. The base
``Variable`` is untyped; the four typed subclasses differ only in the type
``get()`` returns and their default value. All share one constructor and the same
methods.

.. list-table::
   :header-rows: 1
   :widths: 24 20 56

   * - Class
     - ``get()`` type
     - Default value
   * - ``Variable``
     - ``str``
     - ``""``
   * - ``StringVar``
     - ``str``
     - ``""``
   * - ``IntVar``
     - ``int``
     - ``0``
   * - ``DoubleVar``
     - ``float``
     - ``0.0``
   * - ``BooleanVar``
     - ``bool``
     - ``False``

.. py:class:: StringVar(master=None, value=None, name=None)
   :noindex:

   A variable holding a ``str`` — the usual choice for an Entry or Label.
   ``IntVar``, ``DoubleVar``, ``BooleanVar``, and the untyped ``Variable`` share
   this constructor and every method below.

   :param master: the root or a widget; inferred from the default root if omitted.
   :param value: the initial value (the class default if omitted).
   :param name: the underlying Tcl variable name; auto-generated if omitted.

Reading and writing
-------------------

.. py:method:: get()
   :noindex:

   Return the current value, coerced to the class's type.

   :rtype: str | int | float | bool

   .. note::

      ``IntVar.get()`` and ``DoubleVar.get()`` raise ``tkinter.TclError`` when the
      bound widget's text isn't a valid number — an empty or half-typed Entry, for
      instance. Catch it or validate the field (see the :doc:`Error handling
      </user-guide/how-to/error-handling>` recipe and :doc:`Validation
      </reference/validation>`).

.. py:method:: set(value)
   :noindex:

   Set the value; every widget bound to the variable updates immediately.

   :param value: the new value.
   :returns: ``None``.

Reacting to changes
-------------------

.. py:method:: trace_add(mode, callback)
   :noindex:

   Run ``callback`` whenever the variable is written, read, or unset — the way to
   react to a bound widget changing without a per-widget ``command``.

   :param mode: ``"write"``, ``"read"``, or ``"unset"`` (or a list of them).
   :param callback: called as ``callback(name, index, op)``; the arguments are
      rarely needed — read the variable with ``.get()`` inside.
   :returns: a trace id, for :py:meth:`trace_remove`.
   :rtype: str

.. py:method:: trace_remove(mode, cbname)
   :noindex:

   Remove a trace added with :py:meth:`trace_add`.

   :param mode: the mode the trace was added with.
   :param cbname: the trace id returned by ``trace_add``.
   :returns: ``None``.

.. py:method:: trace_info()
   :noindex:

   List the traces currently on the variable.

   :returns: a list of ``(mode_list, cbname)`` pairs.
   :rtype: list

LocaleVar
---------

.. py:class:: LocaleVar(master=None, src="", name=None)
   :noindex:

   ttkbootstrap's ``StringVar`` subclass whose value **re-translates itself** when
   the application locale changes (it listens for the ``<<LocaleChanged>>`` event).
   ``src`` is the source string to translate. Use it for label text that should
   follow the active locale — see :doc:`Localization </reference/localization>`.

See also
--------

- :doc:`Variables guide </user-guide/feature-guides/variables>` — binding
  variables to widgets, traces, and the numeric-coercion gotcha.
- :doc:`Validation </reference/validation>` — checking what the user types.
- `tkinter Variable classes
  <https://docs.python.org/3/library/tkinter.html#coupling-widget-variables>`__ —
  the upstream reference.
