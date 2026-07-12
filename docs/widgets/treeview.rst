Treeview
========

A **treeview** displays items in rows — as a hierarchical **tree**, a
multi-column **table**, or both at once. ``Treeview`` is the native
``ttk.Treeview``, styled with ``bootstyle=``. This page covers inserting items,
the tree/table/columns modes, reading and changing items, reacting to a
selection, sorting, row tags for color, then the ``bootstyle`` color and states.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A treeview in light and dark themes, showing a tree on the left column and
   several data columns beside it.

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
``text`` fills the ``"#0"`` tree column.

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
keyboard focus to it.

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

Tags are the way to give rows conditional appearance — flagged rows, groups,
alternating stripes — without touching the widget's base style.

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

API & reference
---------------

``Treeview`` is the native ``ttk.Treeview`` — ttkbootstrap adds ``bootstyle=`` but
no other Python API. For the full set of methods (``insert``, ``item``, ``set``,
``move``, ``delete``, ``heading``, ``column``, ``selection``, ``tag_configure``,
``see``, ``bbox``, …) and options, see the
`tkinter.ttk.Treeview <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview>`__
reference.

.. seealso::

   :doc:`Tableview <tableview>` for a ready-made data table built on the
   treeview. Want to restyle it yourself? The
   :doc:`Style Reference › Treeview </reference/style-reference/treeview>` and the
   :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide document
   the hand-styling surface.
