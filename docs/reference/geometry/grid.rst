Grid
====

The **grid** geometry manager places a widget in a row/column grid in its
parent. This page is the method spec; :doc:`Arranging widgets
</user-guide/foundations/arranging-widgets>` teaches when to reach for grid.

In ttkbootstrap ``grid`` (and ``grid_configure``) return the widget, so
construction and placement can be chained.

The canonical upstream reference is the Tk
`grid <https://www.tcl-lang.org/man/tcl8.6/TkCmd/grid.htm>`__ manual page
(Tcl 8.6).

Options
-------

Every option below is a keyword argument to ``grid()``.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``row`` / ``column``
     - ``int``
     - The cell to occupy (0-based). ``column`` defaults to ``0``; ``row``
       defaults to the first empty row.
   * - ``rowspan`` / ``columnspan``
     - ``int``
     - How many rows / columns the widget covers. Default ``1``.
   * - ``sticky``
     - ``str``
     - Which sides of the cell the widget sticks to — any combination of
       ``"nsew"``. Opposite pairs stretch the widget; the default centers it
       at its natural size.
   * - ``padx`` / ``pady``
     - ``int | tuple``
     - External space around the widget, in pixels. A ``(left, right)`` /
       ``(top, bottom)`` tuple pads the two sides differently.
   * - ``ipadx`` / ``ipady``
     - ``int``
     - Internal padding added to the widget's own size, in pixels.
   * - ``in_``
     - ``Widget``
     - Grid inside a container other than the parent (the container must be
       the parent or one of its descendants). Rarely needed.

Placing a widget
----------------

.. py:method:: grid(**options)
   :noindex:

   Place the widget in a cell (or span of cells), using the options above.
   Alias: ``grid_configure``.

   :returns: the widget (ttkbootstrap), for chaining.

.. py:method:: grid_forget()
   :noindex:

   Unmap the widget and forget its grid options.

   :returns: ``None``.

.. py:method:: grid_remove()
   :noindex:

   Unmap the widget but **remember** its options, so a later ``grid()`` with no
   arguments restores it in place.

   :returns: ``None``.

.. py:method:: grid_info()
   :noindex:

   Return the widget's current grid options.

   :rtype: dict

Configuring the container
-------------------------

These are called on the **parent** to shape its rows and columns — most
importantly ``weight``, which decides how leftover space is shared when the
window resizes.

.. py:method:: columnconfigure(index, **options)
   :noindex:

   Configure a column of this container's grid. Alias:
   ``grid_columnconfigure``.

   :param index: the column number (or a list of them).
   :param options: ``weight`` (share of extra space), ``minsize``, ``pad``,
      ``uniform`` (columns sharing a group grow together).
   :returns: the current settings when queried, else ``None``.

.. py:method:: rowconfigure(index, **options)
   :noindex:

   Configure a row of this container's grid. Alias: ``grid_rowconfigure``. Takes
   the same options as :py:meth:`columnconfigure`.

   :param index: the row number (or a list of them).
   :returns: the current settings when queried, else ``None``.

.. py:method:: grid_propagate(flag=None)
   :noindex:

   Get or set whether this container resizes to fit its gridded children. Set
   ``False`` to keep a fixed size.

   :param bool flag: the new setting; omit to query.
   :returns: the current setting when queried, else ``None``.

.. py:method:: grid_size()
   :noindex:

   Return the container's grid size as ``(columns, rows)``.

   :rtype: tuple[int, int]

.. py:method:: grid_slaves(row=None, column=None)
   :noindex:

   Return the widgets this container manages with grid, optionally filtered to a
   row and/or column.

   :rtype: list

.. py:method:: grid_location(x, y)
   :noindex:

   Return the ``(column, row)`` cell that covers a pixel coordinate.

   :rtype: tuple[int, int]

.. py:method:: grid_bbox(column=None, row=None, col2=None, row2=None)
   :noindex:

   Return the bounding box ``(x, y, width, height)`` of a cell or a span of
   cells, in pixels.

   :rtype: tuple[int, int, int, int]

.. py:method:: grid_anchor(anchor=None)
   :noindex:

   Get or set where the whole grid is anchored inside the container when it is
   larger than the grid.

   :param anchor: an anchor like ``"center"`` or ``"nw"``; omit to query.
