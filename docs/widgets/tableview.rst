Tableview
=========

A **tableview** is a data table — rows and columns with built-in sorting, an
optional search bar, and pagination. ``Tableview`` is a ttkbootstrap widget (a
real class with its own API, imported as ``ttk.Tableview``). This page covers
building one from data, the search and pagination options, adding and reading
rows, reacting to a selection, then the ``bootstyle`` color.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A tableview with column headers, several rows, a search bar, and pagination
   controls, in light and dark themes.

Usage
-----

Give it ``coldata`` (the column headings) and ``rowdata`` (a list of rows, each a
list of cell values). Click a header to sort by that column:

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.widgets import Tableview

   app = ttk.App()

   table = Tableview(
       app,
       coldata=["Name", "Role", "Age"],
       rowdata=[
           ["Ada Lovelace", "Engineer", 36],
           ["Grace Hopper", "Admiral", 85],
           ["Alan Turing", "Cryptographer", 41],
       ],
       bootstyle="primary",
   )
   table.pack(fill="both", expand=True, padx=10, pady=10)

   app.mainloop()

``coldata`` entries can also be dictionaries (``{"text": "Age", "width": 60,
"anchor": "e"}``) for per-column width, alignment, and more.

Search and pagination
---------------------

For a large table, turn on the search bar and page the rows:

.. code-block:: python

   Tableview(
       app,
       coldata=["Name", "Role", "Age"],
       rowdata=rows,
       searchable=True,          # a search bar above the table (Enter to filter)
       paginated=True,           # page controls below it
       pagesize=10,              # rows per page
   )

Adding and reading rows
-----------------------

``insert_row`` adds a row (it refreshes the view for you); ``get_rows`` returns the
rows, and ``get_rows(selected=True)`` just the selected ones:

.. code-block:: python

   table.insert_row("end", ["Katherine Johnson", "Mathematician", 101])

   for row in table.get_rows():
       print(row.values)                 # each row's cell values

   selected = table.get_rows(selected=True)

``delete_row`` removes one, and ``build_table_data(coldata, rowdata)`` replaces the
whole dataset.

Reacting to a selection
-----------------------

Pass ``on_select=`` a callback to run when the selection changes — it receives the
list of selected rows:

.. code-block:: python

   def on_select(rows):
       print("selected", [r.values for r in rows])

   Tableview(app, coldata=cols, rowdata=rows, on_select=on_select)

Color
-----

``bootstyle`` colors the header, selection, and accents from the semantic palette;
``stripecolor`` sets an alternating row tint:

.. code-block:: python

   Tableview(app, coldata=cols, rowdata=rows, bootstyle="info")

API & reference
---------------

``Tableview`` ships a large API — ``TableColumn`` / ``TableRow`` objects, sorting,
filtering, CSV export, and programmatic selection — beyond what this page covers.
The full class reference on the :doc:`Widgets API page </reference/api/widgets>`
is pending a docstring cleanup; until then, read the methods in the source
(``ttkbootstrap.widgets.tableview``).

.. seealso::

   :doc:`Build your first app </user-guide/getting-started/build-your-first-app>`
   builds a form that feeds a ``Tableview``, and the ``Treeview`` widget for the
   native tree/table it is built on.
