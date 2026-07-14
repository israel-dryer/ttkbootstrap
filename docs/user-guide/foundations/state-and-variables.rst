State & variables
=================

Widgets that hold a value — entries, checkbuttons, radiobuttons, scales — can be
bound to a **variable object** instead of you reading and writing the widget
directly. A variable is the single source of truth for that value: set the
variable and the widget updates; the user edits the widget and the variable
updates. This two-way link is how tkinter keeps your data and your UI in sync.

.. note::

   This page covers the essentials. For the variable types in depth, traces (read
   / write / unset) and their cleanup, and patterns like computed fields, see the
   :doc:`Variables guide </user-guide/feature-guides/variables>`.

Binding a widget to a variable
------------------------------

Create a variable, then hand it to the widget through the option that fits:
``textvariable`` for text-bearing widgets (Entry, Label), ``variable`` for
selection controls (Checkbutton, Radiobutton, Scale). Read and write with
``.get()`` and ``.set()``:

.. code-block:: python

   name = ttk.StringVar(value="Ada")

   ttk.Entry(app, textvariable=name).pack()
   ttk.Label(app, textvariable=name).pack()   # mirrors the entry live

   name.set("Grace")                          # entry and label both update

The variable classes are re-exported from ttkbootstrap — ``ttk.StringVar``,
``ttk.IntVar``, ``ttk.BooleanVar``, ``ttk.DoubleVar`` — and the class you pick
determines what ``.get()`` returns:

- ``StringVar`` — text (entries, labels).
- ``IntVar`` — whole numbers; a Checkbutton's on/off value; a Radiobutton choice.
- ``BooleanVar`` — ``True``/``False`` (a Checkbutton's checked state).
- ``DoubleVar`` — floating-point numbers (a Scale's position).

Reacting to changes
-------------------

To run code whenever a variable changes, attach a **trace**. The callback fires
on every write — handy for live updates like enabling a button or refreshing a
summary. Swallow the three callback arguments with ``*_``:

.. code-block:: python

   name.trace_add("write", lambda *_: print("value is now", name.get()))

Traces come in read/write/unset modes and can be removed again for cleanup — see
the :doc:`Variables guide </user-guide/feature-guides/variables>`.

A worked example
----------------

A checkbutton drives a boolean, and a trace enables the submit button only when
the box is checked:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Terms")

   agree = ttk.BooleanVar()
   submit = ttk.Button(app, text="Continue", bootstyle="primary")
   submit.state(["disabled"])                 # ttk state flags — see The widget model

   def refresh(*_):
       submit.state(["!disabled" if agree.get() else "disabled"])

   agree.trace_add("write", refresh)

   ttk.Checkbutton(app, text="I accept the terms", variable=agree,
                   bootstyle="round toggle").pack(padx=20, pady=(20, 10))
   submit.pack(padx=20, pady=(0, 20))

   app.mainloop()

.. seealso::

   - :doc:`Variables guide </user-guide/feature-guides/variables>` — the full
     picture.
   - :doc:`Localization </user-guide/feature-guides/localization>` — ``LocaleVar``,
     a variable that re-translates itself when the locale changes.
