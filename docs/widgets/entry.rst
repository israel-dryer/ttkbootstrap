Entry
=====

An **entry** is a single-line text field. ``Entry`` is the native ``ttk.Entry``,
styled with ``bootstyle=``. This page covers reading and writing its value,
masking a password, validating input, then the ``bootstyle`` color and states.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A labeled entry in light and dark themes, and the same entry with a
   ``danger``-red focus border when its value is invalid.

Usage
-----

Bind the entry to a **variable** with ``textvariable=`` — a ``StringVar`` that
stays in sync with what the user types. Read it with ``.get()``; ``.set()`` it to
change the field:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()

   name = ttk.StringVar()
   ttk.Entry(app, textvariable=name).pack(padx=10, pady=10)

   def greet():
       print("Hello,", name.get())

   ttk.Button(app, text="Greet", command=greet, bootstyle="primary").pack()

   app.mainloop()

You can also work with the text directly — ``insert`` adds at an index, ``delete``
removes a range, and ``"end"`` marks the far end:

.. code-block:: python

   entry.insert(0, "default")          # insert at the start
   entry.delete(0, "end")              # clear the whole field

A password field
----------------

``show=`` replaces every typed character with a mask, for passwords and secrets:

.. code-block:: python

   ttk.Entry(app, show="•", bootstyle="primary")

The variable still holds the real text — only the display is masked.

Validating input
----------------

Attach a validation rule and a value that fails it flags the entry with a
``danger`` border until it becomes valid again:

.. code-block:: python

   from ttkbootstrap import Validation

   email = ttk.Entry(app)
   email.pack(padx=10, pady=10)
   Validation.regex(email, r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

The rule set, custom rules, and when they fire are covered in the
:doc:`Input validation guide </user-guide/feature-guides/validation>`.

Color
-----

``bootstyle`` sets the entry's **accent** — the border and the focus ring — from
the semantic colors. Use it to tie an entry to a section's color, or to signal
state (``success``/``danger``) yourself:

.. code-block:: python

   ttk.Entry(app, bootstyle="success")
   ttk.Entry(app, bootstyle="danger")

An entry has no solid/outline variants — it is always a bordered field; the color
is the accent, shown most visibly when the field has focus.

States
------

Two states matter for an entry. **Disabled** greys it out and blocks all
interaction; **readonly** lets the user select and copy the text but not change
it:

.. code-block:: python

   entry.state(["disabled"])           # greyed out, no interaction
   entry.state(["readonly"])           # selectable, not editable
   entry.state(["!disabled", "!readonly"])   # back to normal

API & reference
---------------

``Entry`` is the native ``ttk.Entry`` — ttkbootstrap adds ``bootstyle=`` but no
other Python API. For its constructor and options (``textvariable``, ``show``,
``width``, ``justify``, ``state``, …) see the
`tkinter.ttk.Entry <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Entry>`__
reference.

.. seealso::

   :doc:`Combobox <combobox>` and :doc:`Spinbox <spinbox>` for entries with a
   dropdown or numeric stepper. Want to restyle the entry yourself? The
   :doc:`Style Reference › Entry </reference/style-reference/entry>` and its
   companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>`
   guide document the hand-styling surface.
