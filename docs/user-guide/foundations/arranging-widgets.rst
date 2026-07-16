Arranging widgets
=================

Creating a widget doesn't make it appear — a **geometry manager** has to place it
inside its parent first. This page is the map: which manager to choose, the rules
they all share, and the spacing model that goes with them.

Geometry managers
-----------------

tkinter has three managers, and you choose one per container based on the shape
of the layout:

- **grid** — rows and columns, like a table. The workhorse for forms and anything
  that lines up in two dimensions. Start here:
  :doc:`Layout with grid </user-guide/foundations/layout-with-grid>`.
- **pack** — stack widgets against a side. Ideal for toolbars, a column of
  controls, or a content area above a status bar:
  :doc:`Layout with pack </user-guide/foundations/layout-with-pack>`.
- **place** — exact coordinates, for overlays and the rare pixel-perfect case.
  You'll seldom need it; it's covered briefly on the pack page.

Two rules hold no matter which manager you use:

**One manager per container.** Don't mix ``grid`` and ``pack`` on children of the
*same* parent — they size things differently and tkinter will hang trying to
reconcile them.

**Nest frames to combine them.** Real windows are frames inside frames, each using
whichever manager fits that region — a toolbar packed along the top, a form
gridded inside the content area. Both tutorials build toward exactly that.

New here? Read :doc:`Layout with grid </user-guide/foundations/layout-with-grid>`
first — it's the manager you'll reach for most — then
:doc:`Layout with pack </user-guide/foundations/layout-with-pack>`.

.. _arranging-spacing:

Spacing
-------

Every gap in a well-spaced window comes from one of three layers, with
confusingly similar names. Fix the model once and spacing decisions become
mechanical.

**Around the widget.** ``padx`` and ``pady`` are the geometry manager's margin —
clear space between a widget and its neighbors. They are options to ``grid()``
and ``pack()``, identical in both, not options on the widget. A single number
pads both sides equally; a two-tuple pads each side on its own:

.. code-block:: python

   save.pack(side="left", padx=5)               # 5px on the left and the right
   close.pack(side="left", padx=(0, 5))         # nothing left, 5px right
   label.grid(row=0, column=0, pady=(10, 2))    # 10px above, 2px below

**Inside the widget.** ``padding`` is a widget option: interior space between a
ttk widget's edge and its content. It belongs to the widget, so it travels with
it wherever it is placed. One value pads all four sides, two read as
``(horizontal, vertical)``, four as ``(left, top, right, bottom)``:

.. code-block:: python

   form = ttk.Frame(app, padding=16)                       # 16px on all sides
   wide = ttk.Button(app, text="Wide", padding=(24, 2))    # wider, barely taller

Not every ttk widget has it — input widgets like ``Entry`` and ``Combobox`` take
their interior inset from the theme.

**The manager stretching the widget.** ``ipadx`` and ``ipady`` — also options to
``grid()`` and ``pack()`` — make a widget's allocation bigger than the size it
asked for. The effect looks like ``padding``, but the extra size belongs to that
one placement call rather than to the widget. On widgets that have ``padding``,
prefer it; ``ipadx``/``ipady`` earn their keep on the widgets that don't — the
classic way to make an ``Entry`` taller is ``ipady``:

.. code-block:: python

   search = ttk.Entry(form)
   search.pack(fill="x", ipady=4)     # a taller input

``place`` positions by coordinates and has no spacing options at all.

**Let the container own its margins.** Rather than repeating ``padx``/``pady`` on
every child, give the frame a ``padding`` and let the children pad only against
each other — one number to tune instead of a dozen:

.. code-block:: python

   form = ttk.Frame(app, padding=16)      # the frame owns the outer margin
   form.pack(fill="both", expand=True)

   ttk.Label(form, text="Email").grid(row=0, column=0, sticky="w", pady=4)
   ttk.Entry(form).grid(row=0, column=1, sticky="ew", pady=4)

This is the pattern every example in these docs uses.

.. note::

   The classic tk widgets blur the names: ``Text``, ``TkLabel`` and ``TkFrame``
   accept ``padx``/``pady`` as *widget options* — passed to the constructor, like
   ``padding`` — and there they mean the interior layer, not the manager's
   margin. On a themed ``Text`` the theme manages them; pass ``autostyle=False``
   to set your own (see :doc:`Text </widgets/text>`).
