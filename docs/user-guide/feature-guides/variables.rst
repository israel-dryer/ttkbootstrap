Variables
=========

A **variable object** is tkinter's link between your data and your widgets: bind
a widget to a variable and the two stay in sync — set the variable and the widget
updates, edit the widget and the variable updates. The
:doc:`State & variables </user-guide/foundations/state-and-variables>` foundations
page covers binding and reading; this guide goes deeper into the variable types,
**traces** (reacting to changes), and the patterns they enable.

The variable classes
--------------------

Four classes cover the value types, re-exported from ttkbootstrap (they are the
tkinter classes — import from ``tkinter`` if you prefer). The class you choose
decides what ``.get()`` returns:

.. list-table::
   :header-rows: 1
   :widths: 22 20 58

   * - Class
     - ``.get()`` type
     - Typical use
   * - ``StringVar``
     - ``str``
     - Entry / Label text.
   * - ``IntVar``
     - ``int``
     - Whole numbers; a Checkbutton's on/off value; a Radiobutton group's choice.
   * - ``BooleanVar``
     - ``bool``
     - A Checkbutton's checked state.
   * - ``DoubleVar``
     - ``float``
     - Floating-point values; a Scale's position.

Create with an optional initial ``value``; read and write with ``.get()`` and
``.set()``:

.. code-block:: python

   count = ttk.IntVar(value=0)
   count.set(count.get() + 1)

.. note::

   A numeric variable coerces on read: ``IntVar.get()`` raises ``TclError`` if the
   bound widget holds text that isn't a valid integer (an empty or half-typed
   entry, say). Guard the read, or use a ``StringVar`` and convert yourself, when
   the widget can hold an in-progress value.

Reacting to changes with traces
-------------------------------

A **trace** runs a callback whenever the variable is read, written, or deleted.
``trace_add(mode, callback)`` attaches one; the mode is ``"write"`` (the usual
choice), ``"read"``, or ``"unset"``:

.. code-block:: python

   name = ttk.StringVar()

   def on_write(var_name, index, mode):
       print("changed to", name.get())

   name.trace_add("write", on_write)

The callback receives three positional arguments — the internal variable name, an
index (used only for old-style array variables, normally ``""``), and the mode.
You rarely need them, so the idiom is to swallow them with ``*_``:

.. code-block:: python

   name.trace_add("write", lambda *_: refresh())

Managing traces
~~~~~~~~~~~~~~~

``trace_add`` returns an id, and ``trace_info()`` lists the traces on a variable:

.. code-block:: python

   trace_id = name.trace_add("write", refresh)
   name.trace_info()      # [(('write',), '…refresh')]

Most traces live for the whole program and need no cleanup. When one must stop —
typically because its callback closes over a widget you're about to destroy —
remove it with the id so it doesn't fire against a dead widget:

.. code-block:: python

   name.trace_remove("write", trace_id)

Patterns
--------

**A computed field.** Trace the inputs and recompute a derived value on every
change — a live total, a character counter, a full-name label:

.. code-block:: python

   first, last = ttk.StringVar(), ttk.StringVar()
   full = ttk.StringVar()

   def recompute(*_):
       full.set(f"{first.get()} {last.get()}".strip())

   first.trace_add("write", recompute)
   last.trace_add("write", recompute)

   ttk.Entry(app, textvariable=first).pack()
   ttk.Entry(app, textvariable=last).pack()
   ttk.Label(app, textvariable=full).pack()      # updates as you type

**Enable on condition.** A trace is the clean way to gate a control on state — a
Submit button that enables only when a box is checked:

.. code-block:: python

   agree = ttk.BooleanVar()
   submit = ttk.Button(app, text="Continue", bootstyle="primary")
   submit.state(["disabled"])

   agree.trace_add("write",
                   lambda *_: submit.state(["!disabled" if agree.get() else "disabled"]))

**Validate as you type.** For input validation specifically, ttkbootstrap ships
dedicated helpers rather than hand-rolled traces — see
:doc:`Input validation </user-guide/feature-guides/validation>`.

``LocaleVar`` — a variable that re-translates
---------------------------------------------

ttkbootstrap ships one specialized variable, :class:`~ttkbootstrap.LocaleVar`. It
is a ``StringVar`` whose text is a translation key: bind a widget to it and the
text re-translates itself automatically whenever the app's locale changes. It's a
concrete instance of the same observer pattern — the variable listens for the
``<<LocaleChanged>>`` event and updates every widget bound to it:

.. code-block:: python

   greeting = ttk.LocaleVar(app, "Hello")        # first arg is the master
   ttk.Label(app, textvariable=greeting).pack()  # follows the locale

See :doc:`Localization </user-guide/feature-guides/localization>` for the full
localization subsystem.

.. seealso::

   :doc:`State & variables </user-guide/foundations/state-and-variables>` for the
   binding basics, and the :doc:`Variables reference </reference/variables>` for
   the ``StringVar`` / ``IntVar`` / … API and the numeric-coercion gotcha.
