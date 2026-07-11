State & variables
=================

Widgets that hold a value — entries, checkbuttons, radiobuttons, scales — can be
bound to a **variable object** instead of you reading and writing the widget
directly. A variable is the single source of truth for that value: set the
variable and the widget updates; the user edits the widget and the variable
updates. This two-way link is how tkinter keeps your data and your UI in sync.

The variable classes are re-exported from ttkbootstrap, so you can reach them as
``ttk.StringVar``, ``ttk.IntVar``, ``ttk.BooleanVar``, and ``ttk.DoubleVar``
(they are the tkinter classes — import them from ``tkinter`` if you prefer).

Binding a widget to a variable
------------------------------

Create a variable, then hand it to the widget through the option that fits:
``textvariable`` for text-bearing widgets (Entry, Label), ``variable`` for
selection controls (Checkbutton, Radiobutton, Scale):

.. code-block:: python

   name = ttk.StringVar(value="Ada")

   ttk.Entry(app, textvariable=name).pack()
   ttk.Label(app, textvariable=name).pack()   # mirrors the entry live

Read and write the value with ``.get()`` and ``.set()``:

.. code-block:: python

   name.get()          # -> "Ada"
   name.set("Grace")   # entry and label both update

Choose the class by value type
------------------------------

The class you pick determines what ``.get()`` returns:

- ``StringVar`` — text (entries, labels).
- ``IntVar`` — whole numbers; also the on/off value of a Checkbutton or the
  chosen value of a Radiobutton group.
- ``BooleanVar`` — ``True``/``False`` (a Checkbutton's checked state).
- ``DoubleVar`` — floating-point numbers (a Scale's position).

.. code-block:: python

   agree = ttk.BooleanVar()
   ttk.Checkbutton(app, text="I agree", variable=agree,
                   bootstyle="success-round-toggle").pack()

   agree.get()   # -> True once the box is checked

Reacting to changes
-------------------

To run code whenever a variable changes, attach a trace. The callback fires on
every write — useful for live validation, enabling a button, or updating a
summary:

.. code-block:: python

   def on_change(*_):
       print("value is now", name.get())

   trace_id = name.trace_add("write", on_change)

Most traces live for the life of the app and need no cleanup. When you do need to
stop reacting — say the callback closes over a widget you are about to destroy —
``trace_add`` returns an id you pass to ``trace_remove``:

.. code-block:: python

   name.trace_remove("write", trace_id)

A worked example
----------------

A checkbutton drives a boolean, and a trace enables the submit button only when
the box is checked:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Terms")

   agree = ttk.BooleanVar()
   submit = ttk.Button(app, text="Continue", bootstyle="primary", state="disabled")

   def refresh(*_):
       submit.configure(state="normal" if agree.get() else "disabled")

   agree.trace_add("write", refresh)

   ttk.Checkbutton(app, text="I accept the terms", variable=agree,
                   bootstyle="round-toggle").pack(padx=20, pady=(20, 10))
   submit.pack(padx=20, pady=(0, 20))

   app.mainloop()

``LocaleVar`` — a variable that re-translates
---------------------------------------------

ttkbootstrap ships one specialized variable, :class:`~ttkbootstrap.LocaleVar`. It
is a ``StringVar`` whose text is a translation key: bind a widget to it, and the
text re-translates itself automatically whenever the app's locale changes. It is
a concrete example of the same observer pattern — the variable listens for the
``<<LocaleChanged>>`` event and updates every widget bound to it:

.. code-block:: python

   greeting = ttk.LocaleVar(app, "Hello")
   ttk.Label(app, textvariable=greeting).pack()   # follows the locale

See :doc:`Localization </user-guide/feature-guides/localization>` for the full
localization subsystem.

.. seealso::

   The variable classes are standard tkinter. For the complete API, see
   `Variable classes <https://docs.python.org/3/library/tkinter.html#coupling-widget-variables>`__
   on python.org.
