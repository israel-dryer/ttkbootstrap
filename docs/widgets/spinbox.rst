Spinbox
=======

A **spinbox** is an entry with up/down arrows for stepping through a range of
values. ``Spinbox`` is the native ``ttk.Spinbox``, styled with ``bootstyle=``.
This page covers stepping over a numeric range, stepping through a list, reacting
to the arrows, then the ``bootstyle`` color and states.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A numeric spinbox and a list spinbox in light and dark themes, showing the
   up/down arrows.

Usage
-----

Give a numeric range with ``from_``, ``to``, and ``increment`` (the step per
arrow click), and bind the value to a variable:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()

   quantity = ttk.IntVar(value=1)
   ttk.Spinbox(app, from_=1, to=10, increment=1, textvariable=quantity).pack(padx=10, pady=10)

   ttk.Button(app, text="Order", command=lambda: print(quantity.get()), bootstyle="primary").pack()

   app.mainloop()

``from_`` has a trailing underscore because ``from`` is a Python keyword; ``to``
and ``increment`` do not. Read the value with the bound variable's ``.get()`` or
the spinbox's own ``.get()`` (which returns a string).

Stepping through a list
-----------------------

Pass ``values=`` instead of a range to step through a fixed list. Add
``wrap=True`` so it cycles from the last item back to the first:

.. code-block:: python

   ttk.Spinbox(app, values=["Small", "Medium", "Large"], wrap=True)

Reacting to the arrows
----------------------

``command=`` runs each time the user clicks an arrow — handy to recompute
something as the value steps:

.. code-block:: python

   def on_step():
       print("now", quantity.get())

   ttk.Spinbox(app, from_=0, to=100, increment=5, textvariable=quantity, command=on_step)

``command`` fires only for the arrows, not for typing; to react to typed edits too,
trace the variable (see :doc:`State & variables
</user-guide/foundations/state-and-variables>`).

Color
-----

Like the other inputs, ``bootstyle`` sets the spinbox's **focus color**: the
border is a neutral hairline at rest and shows the accent color when the field has
focus (and ``danger`` when a validation rule fails). The stepper arrows keep a
constant color across styles.

.. code-block:: python

   ttk.Spinbox(app, from_=0, to=10, bootstyle="info")

States
------

**Disabled** greys the whole widget out; **readonly** lets the arrows still step
the value but blocks typing:

.. code-block:: python

   spin.state(["disabled"])            # greyed out, no interaction
   spin.state(["readonly"])            # arrows work, not typeable
   spin.state(["!disabled", "!readonly"])   # back to normal

API & reference
---------------

``Spinbox`` is the native ``ttk.Spinbox`` — ttkbootstrap adds ``bootstyle=`` but
no other Python API. For its constructor and options (``from_``, ``to``,
``increment``, ``values``, ``wrap``, ``textvariable``, ``command``, ``format``,
…) see the
`tkinter.ttk.Spinbox <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Spinbox>`__
reference.

.. seealso::

   :doc:`Entry <entry>` for a plain text field and :doc:`Combobox <combobox>` for
   a dropdown of choices. Want to restyle the spinbox yourself? The
   :ref:`Spinbox's styling options <spinbox-styling>` and its
   companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>`
   guide document the hand-styling surface.
