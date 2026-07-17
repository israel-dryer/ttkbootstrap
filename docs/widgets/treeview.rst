Treeview
========

A **treeview** displays items in rows — as a hierarchical **tree**, a
multi-column **table**, or both at once. ``Treeview`` is the native
``ttk.Treeview``, styled with ``bootstyle=``. This page covers inserting items,
the tree/table/columns modes, reading and changing items, reacting to a
selection, sorting, row tags for color, then the ``bootstyle`` color and states.

.. image:: /_static/examples/treeview-hero-light.png
   :class: tb-screenshot-light
   :width: 390px
   :alt: A treeview with a file tree in the first column and data columns beside it — light theme

.. image:: /_static/examples/treeview-hero-dark.png
   :class: tb-screenshot-dark
   :width: 390px
   :alt: A treeview with a file tree in the first column and data columns beside it — dark theme

Usage
-----

Every row is an **item**. Add one with ``insert(parent, index, ...)`` — pass
``""`` as the parent for a top-level row, or another item's id to nest under it.
``insert`` returns the new item's id, which you use for everything else:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()

   tree = ttk.Treeview(app, bootstyle="info")
   tree.pack(fill="both", expand=True, padx=10, pady=10)

   src = tree.insert("", "end", text="src", open=True)   # a top-level row
   tree.insert(src, "end", text="app.py")                # nested under it
   tree.insert(src, "end", text="utils.py")
   tree.insert("", "end", text="README.md")

   app.mainloop()

``index`` is where among its siblings the row goes — ``"end"`` to append, ``0``
to insert first. ``open=True`` starts a parent expanded.

Tree, table, or both
--------------------

A treeview has a built-in first column (id ``"#0"``) that shows the tree — the
item ``text``, indentation, and expand arrows. Declare extra ``columns=`` to show
data beside it, and ``show=`` chooses which parts are visible:

- ``show="tree headings"`` (the default) — the tree column **and** the data
  columns, each with a heading.
- ``show="headings"`` — data columns only, no tree column: a plain **table**.
- ``show="tree"`` — the tree column only: a plain outline or list.

.. code-block:: python

   tree = ttk.Treeview(app, columns=("size", "modified"), show="headings")

   tree.heading("size", text="Size")            # column heading text
   tree.heading("modified", text="Modified")
   tree.column("size", width=80, anchor="e")    # width in px, cell alignment

   tree.insert("", "end", values=(1024, "today"))
   tree.insert("", "end", values=(512, "yesterday"))

Name the columns yourself in ``columns=`` and refer to each by that name in
``heading`` / ``column`` / ``values``. ``values`` fills the data columns in order;
``text`` fills the ``"#0"`` tree column. ``displaycolumns=`` reorders or hides the
data columns for display without changing ``columns=``, and ``column(name,
stretch=False)`` pins a column's width when the widget is resized (columns stretch
to share extra space by default).

Reading and changing items
--------------------------

``get_children(parent)`` returns the ids of a row's children (pass no argument for
the top level); ``item(id)`` returns everything about one row; ``set(id, column)``
reads or writes a single cell:

.. code-block:: python

   for iid in tree.get_children():
       print(tree.item(iid, "text"), tree.item(iid, "values"))

   tree.set(item_id, "size", 2048)        # write one cell
   size = tree.set(item_id, "size")       # read it back

``item(id, option=value)`` updates a row, ``move(id, parent, index)`` relocates
it, and ``delete(id)`` removes it (along with its children):

.. code-block:: python

   tree.item(item_id, text="renamed.py", open=True)
   tree.move(item_id, new_parent, 0)
   tree.delete(item_id)

To hide a row temporarily without losing it — filtering, say — ``detach(id)``
unlinks it from the tree (keeping its data), and ``reattach(id, parent, index)``
puts it back:

.. code-block:: python

   tree.detach(item_id)                    # remove from view, keep the item
   tree.reattach(item_id, "", "end")       # restore it at the top level

Reacting to a selection
-----------------------

Bind the ``<<TreeviewSelect>>`` virtual event to run code when the selection
changes; ``selection()`` returns the selected item ids:

.. code-block:: python

   def on_select(event):
       for iid in tree.selection():
           print("selected", tree.item(iid, "text"))

   tree.bind("<<TreeviewSelect>>", on_select)

``selection_set(id)`` selects an item from code, and ``focus(id)`` moves the
keyboard focus to it. ``selectmode=`` sets how many rows the user can select —
``"extended"`` (the default: multi-select with Shift/Ctrl), ``"browse"`` (one at a
time), or ``"none"``. Adjust a multi-selection from code with ``selection_add`` /
``selection_remove`` / ``selection_toggle`` (``selection_set`` replaces it).
**Focus and selection are separate**: ``focus(id)`` sets the single active row the
keyboard drives, which needn't be part of the selection.

Bind ``<<TreeviewOpen>>`` / ``<<TreeviewClose>>`` to react when a parent is
expanded or collapsed — the hook for **lazy-loading** a node's children the first
time it opens (``tree.focus()`` is the row being opened):

.. code-block:: python

   tree.bind("<<TreeviewOpen>>", lambda event: load_children(tree.focus()))

Finding what was clicked
------------------------

To turn a click into a target — for a right-click context menu, say — map the
pointer to a row and region. ``identify_row(y)`` returns the item id under a pixel,
and ``identify_region(x, y)`` says which part was hit (``"heading"``, ``"cell"``,
``"tree"``, or ``"separator"``):

.. code-block:: python

   def on_right_click(event):
       row = tree.identify_row(event.y)
       if row:
           tree.selection_set(row)         # select the row under the pointer
       # ...then pop your context menu

   tree.bind("<Button-3>", on_right_click)  # <Button-2> on macOS

Sorting on a heading
--------------------

A heading can run a callback when clicked — wire it to re-sort the rows. Read each
row's cell, sort the ids, and ``move`` them into the new order:

.. code-block:: python

   def sort_by(column, descending):
       rows = [(tree.set(iid, column), iid) for iid in tree.get_children("")]
       rows.sort(reverse=descending)
       for index, (_, iid) in enumerate(rows):
           tree.move(iid, "", index)
       # flip the direction for the next click on this heading
       tree.heading(column, command=lambda: sort_by(column, not descending))

   tree.heading("size", text="Size", command=lambda: sort_by("size", False))

Cell values come back from ``set`` as **strings**, so this sorts as text. For a
numeric column, convert in the sort key instead — ``rows.sort(key=lambda r:
int(r[0]), reverse=descending)``.

.. note::

   For a data table that already has click-to-sort headers, a search bar, and
   pagination built in, use the :doc:`Tableview <tableview>` widget — it wraps a
   treeview and does this for you.

Coloring rows with tags
-----------------------

Attach one or more **tags** to an item, then style a tag with ``tag_configure``
to color, highlight, or re-font every row that carries it:

.. code-block:: python

   tree.tag_configure("overdue", background="#f8d7da")

   tree.insert("", "end", values=("Invoice #12", "past due"), tags=("overdue",))

A tag can set ``foreground`` and ``font`` too, not only ``background``. When a row
carries two tags with conflicting styles, the one **configured first** takes
priority. Tags are the way to give rows conditional appearance — flagged rows,
groups, alternating stripes — without touching the widget's base style.

Color
-----

``bootstyle`` colors the headings and the selection highlight from the semantic
palette:

.. code-block:: python

   ttk.Treeview(app, columns=("size",), bootstyle="primary")

States
------

**Disabled** greys the widget and stops interaction:

.. code-block:: python

   tree.state(["disabled"])            # greyed out
   tree.state(["!disabled"])           # re-enable

Reference
---------

``Treeview`` is the native ``ttk.Treeview``; ttkbootstrap adds only the
``bootstyle`` keyword.

- :doc:`Treeview API reference </reference/api/treeview>` — every option and
  method (``insert`` / ``item`` / ``set`` / ``selection`` / ``detach`` /
  ``identify_row`` …).
- :ref:`Treeview styling options <treeview-styling>` — restyle it yourself, with
  the :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide.

.. seealso::

   - :doc:`Tableview <tableview>` — a ready-made data table built on the treeview.
