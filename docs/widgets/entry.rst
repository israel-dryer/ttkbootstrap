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

You can also work with the text directly, by **character position**. An entry
numbers positions from ``0`` — before the first character — and the string
``"end"`` is the position past the last. ``insert(index, text)`` adds text at a
position; ``delete(first, last)`` removes the characters between two:

.. code-block:: python

   entry.insert(0, "default")          # insert before the first character
   entry.insert("end", "!")            # append after the last
   entry.delete(0, "end")              # remove everything from 0 to the end

Positions beyond ``0`` and ``"end"`` let you work relative to the cursor and the
selection: ``"insert"`` is the cursor, ``"sel.first"`` / ``"sel.last"`` bound the
current selection, and ``"@x"`` is the character under pixel *x*. Out-of-range
indices round to the nearest legal position, so bounds checks are rarely needed:

.. code-block:: python

   entry.icursor("end")                # move the cursor to the end
   entry.selection_range(0, "end")     # select all the text
   if entry.selection_present():       # is anything selected?
       entry.delete("sel.first", "sel.last")

A password field
----------------

``show=`` replaces every typed character with a mask, for passwords and secrets:

.. code-block:: python

   ttk.Entry(app, show="•", bootstyle="primary")

The variable still holds the real text — only the display is masked. (Text the
user *copies* out of a masked field is the mask characters, not the real value.)

Validating input
----------------

Attach a validation rule with the :class:`~ttkbootstrap.Validation` helpers:

.. code-block:: python

   from ttkbootstrap import Validation

   email = ttk.Entry(app)
   email.pack(padx=10, pady=10)
   Validation.regex(email, r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

By default the rule runs when the entry **loses focus**. If the value passes,
nothing changes; if it fails, the entry takes on a ``danger``-colored border that
stays until the value becomes valid again — so the field flags itself only after
the user leaves it, not on every keystroke. Pass ``when=`` to validate at a
different time (for example ``when="key"`` to check as they type).

Two things worth knowing: a failed check puts the entry in the ``invalid`` state —
the state the ``danger`` border maps to, readable with
``entry.instate(["invalid"])`` — and validation does **not** re-run when you change
the value through the bound ``textvariable`` from code (only user edits and focus
trigger it). The full rule set, custom rules, and the ``when=`` options are covered
in the :doc:`Input validation guide </user-guide/feature-guides/validation>`.

Color
-----

On an entry, ``bootstyle`` sets the **focus color**. At rest the border is a
neutral hairline; when the field takes focus, the border shows the accent color
you chose. (A failed validation rule overrides it with a ``danger`` border — see
`Validating input`_.)

.. code-block:: python

   ttk.Entry(app, bootstyle="primary")     # border turns primary on focus

An entry has no solid/outline variants — it is always a bordered field, and the
color is the focus accent, not a persistent fill.

States
------

Two states matter for an entry. **Disabled** greys it out and blocks all
interaction; **readonly** lets the user select and copy the text but not change
it:

.. code-block:: python

   entry.state(["disabled"])           # greyed out, no interaction
   entry.state(["readonly"])           # selectable, not editable
   entry.state(["!disabled", "!readonly"])   # back to normal

When you attach validation, a failed check adds a third state: **invalid**.
Validation sets and clears it for you, and it is what the ``danger`` border maps
to — read it with ``entry.instate(["invalid"])`` (see `Validating input`_).

Reference
---------

``Entry`` is the native ``ttk.Entry``; ttkbootstrap adds only the ``bootstyle``
keyword.

- :doc:`Entry API reference </reference/api/entry>` — every option and method.
- :ref:`Entry styling options <entry-styling>` — restyle it yourself, with the
  :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide.

.. seealso::

   - :doc:`Combobox <combobox>` — an entry with a dropdown of choices.
   - :doc:`Spinbox <spinbox>` — an entry with a numeric stepper.
