Combobox
========

A **combobox** is a text entry with a dropdown list of choices. ``Combobox`` is
the native ``ttk.Combobox``, styled with ``bootstyle=``. This page covers offering
choices, reacting to a selection, the pick-only vs. editable modes, then the
``bootstyle`` color and states.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A combobox in light and dark themes, closed and with its dropdown list open.

Usage
-----

Pass the choices as ``values=`` and bind the selection to a ``StringVar`` with
``textvariable=``. Read it with ``.get()``:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()

   color = ttk.StringVar()
   ttk.Combobox(app, textvariable=color, values=["Red", "Green", "Blue"]).pack(padx=10, pady=10)

   ttk.Button(app, text="Use", command=lambda: print(color.get()), bootstyle="primary").pack()

   app.mainloop()

Give the variable an initial ``value`` to preselect an item, or call ``.set()`` /
``.current(index)`` to select one programmatically:

.. code-block:: python

   color.set("Green")                  # by value
   combo.current(0)                    # by index -> "Red"

Reacting to a selection
-----------------------

To run code the moment the user picks an item, bind the ``<<ComboboxSelected>>``
virtual event:

.. code-block:: python

   def on_pick(event):
       print("picked", color.get())

   combo.bind("<<ComboboxSelected>>", on_pick)

``<<ComboboxSelected>>`` fires only when the user **picks** from the list — not
when they type into an editable combobox. To catch typed values too, also trace
the variable. ``combo.current()`` with no argument returns the index of the
selected value, or ``-1`` if the current text isn't one of ``values`` — the clean
way to tell a picked value from a typed-in one.

Keeping the list fresh
----------------------

Pass ``postcommand=`` to refresh ``values`` just before the dropdown opens — for a
recent-items or live list — and ``height=`` to cap how many rows show before the
list scrolls:

.. code-block:: python

   def refresh():
       combo.configure(values=["Red", "Green", "Blue"])

   combo = ttk.Combobox(app, textvariable=color, postcommand=refresh, height=8)

Because ``postcommand`` runs each time the list is about to open, it can build the
choices from the *current* state — including another widget's selection. That's how
you make a **dependent (cascading) dropdown**, e.g. a city list filtered by the
selected country:

.. code-block:: python

   cities = {"France": ["Paris", "Lyon"], "Japan": ["Tokyo", "Osaka"]}

   def city_choices():
       city_combo.configure(values=cities.get(country.get(), []))

   city_combo = ttk.Combobox(app, textvariable=city, postcommand=city_choices)

Pick-only vs. editable
----------------------

By default the user can also *type* into a combobox. Set ``state="readonly"`` to
make it **pick-only** — the value is always one of your ``values``, which is what
you usually want for a fixed set of choices:

.. code-block:: python

   ttk.Combobox(app, values=["Small", "Medium", "Large"], state="readonly")

Leave the state default to let the user type a value that isn't in the list — an
editable combobox, useful for a "recent / or type your own" field.

Color
-----

Like the other inputs, ``bootstyle`` sets the combobox's **focus color**: the
border is a neutral hairline at rest and shows the accent color when the field has
focus (and ``danger`` when a validation rule fails). The dropdown arrow keeps a
constant color across styles.

.. code-block:: python

   ttk.Combobox(app, values=["Red", "Green", "Blue"], bootstyle="success")

The open dropdown is a classic ``tk`` listbox, not a ttk widget. ttkbootstrap
colors it to match the current theme, but it does **not** take the combobox's
``bootstyle`` accent — so a colored field shows a neutral dropdown, which is
expected.

States
------

**Disabled** greys the whole widget out; **readonly** (above) keeps it usable as a
pick-only control:

.. code-block:: python

   combo.state(["disabled"])           # greyed out, no interaction
   combo.state(["readonly"])           # pick-only, not typeable
   combo.state(["!disabled"])          # re-enable

API & reference
---------------

``Combobox`` is the native ``ttk.Combobox`` — ttkbootstrap adds ``bootstyle=`` but
no other Python API. For its constructor and options (``values``,
``textvariable``, ``state``, ``height``, ``postcommand``, …) and the ``get`` /
``set`` / ``current`` methods, see the
`tkinter.ttk.Combobox <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Combobox>`__
reference.

.. seealso::

   :doc:`Entry <entry>` for a plain text field and :doc:`Spinbox <spinbox>` for a
   stepper over an ordered range. Want to restyle the combobox yourself? The
   :ref:`Combobox's styling options <combobox-styling>` and its
   companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>`
   guide document the hand-styling surface.
