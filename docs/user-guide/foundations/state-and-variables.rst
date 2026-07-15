Variables & reactivity
======================

Widgets that hold a value — entries, checkbuttons, radiobuttons, scales — can be
bound to a **variable object** instead of you reading and writing the widget
directly. A variable is the single source of truth for that value: set the
variable and the widget updates; the user edits the widget and the variable
updates. That two-way link — plus running code when a value changes — is
**reactivity**: your interface follows your data instead of you wiring every
update by hand.

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

ttkbootstrap provides four variable classes — ``ttk.StringVar``, ``ttk.IntVar``,
``ttk.BooleanVar``, ``ttk.DoubleVar`` — and the class you pick determines what
``.get()`` returns:

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

Reactivity in one screen: an entry feeds a variable, a trace recomputes a second
variable from it, and a label bound to that one updates live as you type — no
widget is read or refreshed by hand.

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Reactivity")

   name = ttk.StringVar()
   greeting = ttk.StringVar(value="Hello there!")

   def greet(*_):
       who = name.get().strip()
       greeting.set(f"Hello, {who}!" if who else "Hello there!")

   name.trace_add("write", greet)            # recompute whenever name changes

   ttk.Entry(app, textvariable=name).pack(padx=20, pady=(20, 8))
   ttk.Label(app, textvariable=greeting, bootstyle="primary").pack(padx=20, pady=(0, 20))

   app.mainloop()

.. seealso::

   - :doc:`Variables guide </user-guide/feature-guides/variables>` — the full
     picture.
   - :doc:`Localization </user-guide/feature-guides/localization>` — ``LocaleVar``,
     a variable that re-translates itself when the locale changes.
