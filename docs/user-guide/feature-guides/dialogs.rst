Dialogs
=======

A **dialog** is a small pop-up window for a single interaction — telling the user
something, asking a yes/no question, or collecting one value. ttkbootstrap ships
themed dialogs that replace tkinter's plain stdlib ones, reached through two
facades:

- **Messagebox** — *tell* the user something, or *ask* a fixed question (OK,
  yes/no, retry/cancel).
- **Querybox** — *get a value* back: a string, a number, a date, a font, a color.

Every dialog is **modal** (it blocks the rest of the app until dismissed) and
**returns its result directly** from the call — no callbacks to wire up. All the
names below are re-exported at the top level, so ``ttk.Messagebox`` and
``from ttkbootstrap import Messagebox`` both work.

Messagebox — tell and ask
-------------------------

Each method is a one-line call that pops the dialog, blocks until the user
answers, and **returns the label of the button they pressed** — or ``None`` if
they dismissed it with *Escape* or the window's ✕:

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap import Messagebox

   app = ttk.App()

   answer = Messagebox.yesno("Save changes before closing?", "Confirm")
   if answer == "Yes":
       save()

The two families:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Method
     - Shows
   * - ``show_info`` / ``show_warning`` / ``show_error`` / ``show_question``
     - A message with the matching icon and an **OK** button.
   * - ``ok`` / ``okcancel`` / ``yesno`` / ``yesnocancel`` / ``retrycancel``
     - The named choice buttons; the return value is the one pressed.

The first positional argument is the ``message``; the second is the ``title``.
Everything else is **keyword-only** — most importantly ``parent``, which centers
the dialog over a window and ties its modality to it:

.. code-block:: python

   Messagebox.show_error("The file could not be opened.", "Error", parent=app)

Pass your own ``buttons`` to a Messagebox as ``"label:bootstyle"`` strings; the
returned value is still whichever label was clicked:

.. code-block:: python

   choice = Messagebox.show_question(
       "Apply changes to all items?", "Apply",
       buttons=["Cancel:secondary", "This one:primary", "All:success"],
   )

.. note::

   The return value is the button's **displayed** text. With localization active
   the labels are translated, so a bare ``== "Yes"`` can miss — compare against
   the same source string you passed, or drive off the button *position*. See
   :doc:`Localization </user-guide/feature-guides/localization>`.

Querybox — get a value
----------------------

Where a Messagebox returns a button, a **Querybox** returns a **typed value** —
or ``None`` if the user cancels:

.. code-block:: python

   from ttkbootstrap import Querybox

   name = Querybox.get_string("What is your name?", "Name")
   if name is not None:                 # None means they cancelled
       greet(name)

.. list-table::
   :header-rows: 1
   :widths: 46 54

   * - Method
     - Returns (or ``None`` on cancel)
   * - ``get_string(prompt, title)``
     - the entered ``str`` (an empty submit is ``""``, *not* ``None``).
   * - ``get_integer(prompt, title, minvalue=, maxvalue=)``
     - an ``int``, range-checked.
   * - ``get_float(prompt, title, minvalue=, maxvalue=)``
     - a ``float``, range-checked.
   * - ``get_item(prompt, title, items=[...])``
     - the chosen ``str`` from ``items``.
   * - ``get_date(parent, ...)``
     - a ``datetime.date`` from a calendar popup.
   * - ``get_font(parent)``
     - a ``tkinter.font.Font``.
   * - ``get_color(parent, initialcolor=)``
     - a ``ColorChoice`` (see below).

The number pickers validate for you — a value outside ``minvalue``/``maxvalue``
keeps the dialog open until it is corrected or cancelled:

.. code-block:: python

   age = Querybox.get_integer("Age?", "Sign up", minvalue=0, maxvalue=130)

.. note::

   ``None`` unambiguously means *cancelled*. Always check for it before using the
   result — the value pickers never raise on cancel, they return ``None``.

The pickers
~~~~~~~~~~~

``get_date``, ``get_font``, and ``get_color`` open richer choosers. Note their
first argument is the ``parent`` window (the dialog centers on it):

.. code-block:: python

   from datetime import date

   d = Querybox.get_date(app, title="Pick a date", start_date=date.today())

   font = Querybox.get_font(app)         # a tkinter.font.Font, usable as font=font

``get_color`` returns a ``ColorChoice`` — a named tuple with the same color in
three models, so you can take whichever you need:

.. code-block:: python

   c = Querybox.get_color(app, initialcolor="#3498db")
   if c is not None:
       print(c.hex)      # '#RRGGBB'
       print(c.rgb)      # (r, g, b), each 0–255
       print(c.hsl)      # (h 0–360, s 0–100, l 0–100)

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A Messagebox yes/no and a Querybox color picker side by side, both in the
   active theme.

``filedialog`` — the one you still reach for stdlib
---------------------------------------------------

The **one** standard dialog ttkbootstrap does *not* replace is the file dialog:
open, save, and choose-directory use the **native OS** dialog, which you want —
so call tkinter's :mod:`tkinter.filedialog` directly. Each returns the chosen
path as a string, or an empty string ``""`` if cancelled:

.. code-block:: python

   from tkinter import filedialog

   path = filedialog.askopenfilename(
       title="Open",
       filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
   )
   if path:                              # "" means cancelled
       open(path).read()

   save_to = filedialog.asksaveasfilename(defaultextension=".txt")
   folder = filedialog.askdirectory()

The other stdlib dialogs (``messagebox``, ``simpledialog``, ``colorchooser``,
the font chooser) *are* superseded — reach for ``Messagebox`` / ``Querybox``
above instead, so they match your theme.

Building your own dialog
------------------------

The facades are built on the ``MessageDialog`` and ``QueryDialog`` classes, which
you can use directly when you need more control — for instance to place the
dialog yourself or run it **without blocking**. Construct one, then call
``show(position=...)`` and read ``.result``:

.. code-block:: python

   dialog = ttk.MessageDialog("Delete this record?", buttons=["Cancel", "Delete:danger"])
   dialog.show()                # modal; blocks until a button is pressed
   if dialog.result == "Delete":
       delete()

``MessageDialog`` also accepts a ``command`` — a plain zero-argument callable run
when a button is pressed — for a fire-and-forget dialog you do not block on.

For a fully bespoke dialog (your own widgets and layout), build a ``Toplevel``
and make it modal yourself; the :doc:`Multiple windows how-to
</user-guide/how-to/multiple-windows>` walks through a reusable modal that
returns a value.

.. seealso::

   :doc:`Windows & high-DPI </user-guide/feature-guides/windows>` for the focus,
   modality, and lifecycle mechanics the dialogs are built on;
   :doc:`Input validation </user-guide/feature-guides/validation>` for validating
   fields in a form dialog; and the :doc:`Multiple windows how-to
   </user-guide/how-to/multiple-windows>` for rolling your own.
