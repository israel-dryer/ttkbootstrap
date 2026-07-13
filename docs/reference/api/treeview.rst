Treeview
========

``Treeview`` is the native ttk multi-column tree/table of items
(``ttk.Treeview``), themed by ttkbootstrap. For usage and examples, see the
:doc:`Treeview catalog page </widgets/treeview>`; this page is the complete
reference for its options, methods, and styling.

Options
-------

Each option can be set in the constructor and changed later with ``configure()``.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``bootstyle``
     - ``str``
     - **Constructor keyword.** An accent color, optionally with a variant. See
       :ref:`Styling options <treeview-styling>` for the available styles.
   * - ``columns``
     - ``list``
     - The identifiers of the data columns, beyond the implicit tree column.
   * - ``displaycolumns``
     - ``list``
     - Which columns to display, and in what order (or ``"#all"``).
   * - ``show``
     - ``str``
     - Which parts to show: ``"tree"``, ``"headings"``, or both.
   * - ``selectmode``
     - ``str``
     - ``"extended"``, ``"browse"``, or ``"none"``.
   * - ``height``
     - ``int``
     - The number of rows visible before scrolling.
   * - ``padding``
     - ``int | tuple``
     - Extra space around the contents, in pixels (a single value, or per-side).
   * - ``xscrollcommand``
     - ``callable``
     - A callback connecting the tree to a horizontal scrollbar.
   * - ``yscrollcommand``
     - ``callable``
     - A callback connecting the tree to a vertical scrollbar.

Methods
-------

Items are addressed by a string **iid**. The tree column is ``"#0"``; data
columns are addressed by name or by position as ``"#N"``.

Items
~~~~~

.. py:method:: insert(parent, index, iid=None, **kw)
   :noindex:

   Insert an item under ``parent`` at ``index``. ``kw`` includes ``text``,
   ``values``, ``image``, ``open``, and ``tags``.

   :returns: the new item's iid.
   :rtype: str

.. py:method:: delete(*items)
   :noindex:

   Delete the given items (and their descendants).

   :returns: ``None``.

.. py:method:: item(item, option=None, **kw)
   :noindex:

   Query or set an item's options.

.. py:method:: set(item, column=None, value=None)
   :noindex:

   Get or set the value of one cell.

.. py:method:: exists(item)
   :noindex:

   Return whether ``item`` is present in the tree.

   :rtype: bool

.. py:method:: see(item)
   :noindex:

   Open and scroll the tree so ``item`` is visible.

   :returns: ``None``.

Structure
~~~~~~~~~

.. py:method:: get_children(item=None)
   :noindex:

   Return the ids of ``item``'s children (default: the roots).

   :rtype: tuple

.. py:method:: set_children(item, *newchildren)
   :noindex:

   Replace ``item``'s children with ``newchildren``.

   :returns: ``None``.

.. py:method:: parent(item)
   :noindex:

   Return the id of ``item``'s parent (empty string for a root item).

   :rtype: str

.. py:method:: index(item)
   :noindex:

   Return ``item``'s position among its siblings.

   :rtype: int

.. py:method:: next(item)
   :noindex:

   Return the id of ``item``'s next sibling.

   :rtype: str

.. py:method:: prev(item)
   :noindex:

   Return the id of ``item``'s previous sibling.

   :rtype: str

.. py:method:: move(item, parent, index)
   :noindex:

   Move ``item`` to a new ``parent`` at ``index``.

   :returns: ``None``.

.. py:method:: detach(*items)
   :noindex:

   Remove items from the tree display without deleting them.

   :returns: ``None``.

.. py:method:: reattach(item, parent, index)
   :noindex:

   Re-insert a previously detached item.

   :returns: ``None``.

Selection
~~~~~~~~~

.. py:method:: selection()
   :noindex:

   Return the ids of the currently selected items.

   :rtype: tuple

.. py:method:: selection_set(*items)
   :noindex:

   Replace the selection with ``items``.

   :returns: ``None``.

.. py:method:: selection_add(*items)
   :noindex:

   Add ``items`` to the selection.

   :returns: ``None``.

.. py:method:: selection_remove(*items)
   :noindex:

   Remove ``items`` from the selection.

   :returns: ``None``.

.. py:method:: selection_toggle(*items)
   :noindex:

   Toggle whether each of ``items`` is selected.

   :returns: ``None``.

Columns and headings
~~~~~~~~~~~~~~~~~~~~~

.. py:method:: column(column, option=None, **kw)
   :noindex:

   Query or set a column's options — ``width``, ``minwidth``, ``anchor``, and
   ``stretch``.

.. py:method:: heading(column, option=None, **kw)
   :noindex:

   Query or set a heading's ``text``, ``image``, ``anchor``, and ``command``.

.. py:method:: identify_region(x, y)
   :noindex:

   Return which region of the treeview is under the pixel coordinate
   ``(x, y)`` — e.g. ``"heading"``, ``"cell"``, ``"tree"``, or ``"separator"``.
   Related methods narrow to one axis or element: ``identify_column(x)``,
   ``identify_row(y)``, and ``identify_element(x, y)``.

   :rtype: str

Tags
~~~~

.. py:method:: tag_configure(tagname, option=None, **kw)
   :noindex:

   Query or set display options (e.g. ``foreground``, ``background``) applied
   to items carrying ``tagname``.

.. py:method:: tag_bind(tagname, sequence=None, callback=None)
   :noindex:

   Bind an event ``sequence`` to items carrying ``tagname``.

.. py:method:: tag_has(tagname, item=None)
   :noindex:

   Return whether ``item`` carries ``tagname``, or (if ``item`` is omitted)
   all items that do.

   :rtype: bool or tuple

Scrolling
~~~~~~~~~

.. py:method:: xview(*args)
   :noindex:

   Query or set the horizontal view; usually wired to a scrollbar. Has
   ``xview_moveto(fraction)`` and ``xview_scroll(number, what)`` variants.

.. py:method:: yview(*args)
   :noindex:

   Query or set the vertical view; usually wired to a scrollbar. Has
   ``yview_moveto(fraction)`` and ``yview_scroll(number, what)`` variants.

.. _treeview-styling:

Styling options
---------------

This section is for changing how the treeview *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``Treeview(style=...)``.

.. include:: /reference/api/_style/treeview.rst

Shared capabilities
-------------------

``Treeview`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Treeview catalog page </widgets/treeview>` — usage, screenshots, and
  examples.
- `Tk ttk::treeview manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_treeview.htm>`__
  — the canonical upstream reference (Tcl 8.6).
