Arranging widgets
=================

Creating a widget does not make it appear. A widget only shows up once a
**geometry manager** places it inside its parent. tkinter has three, and you
pick one per container based on the shape of the layout:

- **pack** — stack widgets in a row or a column. Best for simple, one-direction
  layouts (a toolbar, a vertical stack of controls).
- **grid** — arrange widgets in rows and columns, like a table. Best for forms
  and anything that should line up in two dimensions.
- **place** — position a widget at exact coordinates. Best for overlays and the
  rare pixel-perfect case; you rarely need it.

Each manager is a method on the widget: ``.pack()``, ``.grid()``, ``.place()``.

.. admonition:: One manager per container

   Do not mix ``pack`` and ``grid`` on children of the *same* parent — the two
   negotiate size differently and tkinter will hang trying to reconcile them.
   Different containers can use different managers freely; nesting frames is the
   normal way to combine layouts.

pack
----

``pack`` places each widget against one side of the remaining space. The default
side is ``"top"``, so successive ``pack`` calls stack downward:

.. code-block:: python

   ttk.Button(app, text="One").pack()
   ttk.Button(app, text="Two").pack()

Common options: ``side`` (``"top"``/``"bottom"``/``"left"``/``"right"``),
``fill`` (``"x"``/``"y"``/``"both"`` — grow to fill its allotted space),
``expand`` (claim leftover space), and ``padx``/``pady`` (outer spacing):

.. code-block:: python

   ttk.Entry(app).pack(side="left", fill="x", expand=True, padx=5)
   ttk.Button(app, text="Go").pack(side="left", padx=5)

See the tkinter `Pack geometry manager
<https://docs.python.org/3/library/tkinter.html#tkinter.Pack>`__ reference for
the complete list of options.

grid
----

``grid`` assigns each widget a ``row`` and ``column``. Widgets snap into a table
that sizes itself to its contents:

.. code-block:: python

   ttk.Label(app, text="Name").grid(row=0, column=0, sticky="w", padx=5, pady=5)
   ttk.Entry(app).grid(row=0, column=1, padx=5, pady=5)

Useful options: ``sticky`` (which edges the widget clings to — combine
``"n"``/``"s"``/``"e"``/``"w"``, e.g. ``"ew"`` to stretch horizontally),
``columnspan``/``rowspan``, and ``padx``/``pady``. To let a column or row absorb
extra space when the window resizes, give it weight:

.. code-block:: python

   app.columnconfigure(1, weight=1)   # column 1 grows with the window

See the tkinter `Grid geometry manager
<https://docs.python.org/3/library/tkinter.html#tkinter.Grid>`__ reference for
the complete list of options.

place
-----

``place`` positions a widget by coordinate or by relative fraction of its
parent. Reach for it only when the other two cannot express the layout:

.. code-block:: python

   badge.place(relx=1.0, rely=0.0, anchor="ne")   # pin to the top-right corner

See the tkinter `Place geometry manager
<https://docs.python.org/3/library/tkinter.html#tkinter.Place>`__ reference for
the complete list of options.

Fluent geometry
---------------

In ttkbootstrap, ``pack``, ``grid``, and ``place`` (and their ``*_configure``
spellings) **return the widget**, so you can create and place it in one
expression:

.. code-block:: python

   save = ttk.Button(app, text="Save", bootstyle="success").pack(side="left")

``save`` is the button. With stock tkinter these methods return ``None``, so you
would have to create the widget on one line and place it on the next whenever you
need to keep a reference.

A small form
------------

pack and grid together — an outer frame packed to fill the window, a form laid
out inside it with grid:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Sign in")

   form = ttk.Frame(app, padding=20)
   form.pack(fill="both", expand=True)
   form.columnconfigure(1, weight=1)

   ttk.Label(form, text="Email").grid(row=0, column=0, sticky="w", pady=5)
   ttk.Entry(form).grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)

   ttk.Label(form, text="Password").grid(row=1, column=0, sticky="w", pady=5)
   ttk.Entry(form, show="•").grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)

   ttk.Button(form, text="Sign in", bootstyle="primary").grid(
       row=2, column=1, sticky="e", pady=(10, 0))

   app.mainloop()
