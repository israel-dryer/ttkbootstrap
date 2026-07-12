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

``bootstyle`` sets the combobox's **accent** — the border, the focus ring, and the
dropdown arrow — from the semantic colors:

.. code-block:: python

   ttk.Combobox(app, values=["Red", "Green", "Blue"], bootstyle="success")

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
   :doc:`Style Reference › Combobox </reference/style-reference/combobox>` and its
   companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>`
   guide document the hand-styling surface.
