Tableview
=========

``Tableview`` is a data-table widget that ttkbootstrap ships (``ttk.Tableview``)
— a themed :doc:`Treeview </widgets/treeview>` wrapped with sorting, filtering,
search, pagination, and CSV export, driven from column and row data. This page is the complete
lookup reference.

Rows and columns are represented by ``TableRow`` and ``TableColumn`` objects,
which the ``get_*`` / ``insert_*`` methods and the ``tablerows`` / ``tablecolumns``
properties return. Columns are addressed by integer index or by **cid** (the
column id), rows by index or by **iid** (the row id).

Options
-------

All options are passed to the constructor.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``bootstyle``
     - ``str``
     - The accent color of headers, selection, and controls — one of
       ``primary``, ``secondary``, ``success``, ``info``, ``warning``,
       ``danger``, ``light``, ``dark``.
   * - ``coldata``
     - ``list``
     - The columns, each a heading string or a dict of column settings
       (``text``, ``image``, ``command``, ``anchor``, ``width``, ``minwidth``,
       ``stretch``).
   * - ``rowdata``
     - ``list``
     - The rows, each an iterable whose length matches the number of columns.
   * - ``paginated``
     - ``bool``
     - Whether to page the data with a navigation bar below the table. Default
       ``False``.
   * - ``pagesize``
     - ``int``
     - Rows per page when ``paginated`` is true. Default ``10``.
   * - ``searchable``
     - ``bool``
     - Whether to add a search bar above the table (press Return to search).
       Default ``False``.
   * - ``yscrollbar``
     - ``bool``
     - Whether to add a vertical scrollbar. Default ``False``.
   * - ``autofit``
     - ``bool``
     - Whether to size columns to their content on load. Default ``False``.
   * - ``autoalign``
     - ``bool``
     - Whether to align numeric columns right and others left, based on the
       first record. Default ``True``.
   * - ``stripecolor``
     - ``tuple``
     - A ``(background, foreground)`` pair used to stripe even rows; either may
       be ``None``. Accepts color names, hex, or ``bootstyle`` keywords. Default
       ``None``.
   * - ``height``
     - ``int``
     - How many rows appear in the viewport. Default ``10``.
   * - ``delimiter``
     - ``str``
     - The delimiter used when exporting to CSV. Default ``","``.
   * - ``disable_right_click``
     - ``bool``
     - Whether to disable the built-in right-click menus. Default ``False``.
   * - ``on_select``
     - ``callable``
     - A callback invoked when the selection changes, receiving the list of
       selected ``TableRow`` objects. Default ``None``.
   * - ``iid_field``
     - ``int | str``
     - A column index or header name whose value becomes each row's iid, instead
       of an auto-generated one. Default ``None``.

Methods
-------

Loading data
~~~~~~~~~~~~

.. py:method:: build_table_data(coldata, rowdata)
   :noindex:

   Replace all columns and rows with the given data.

   :returns: ``None``.

.. py:method:: load_table_data(clear_filters=False)
   :noindex:

   Render the current data into the table, optionally clearing filters first.

   :returns: ``None``.

.. py:method:: unload_table_data()
   :noindex:

   Remove all rendered rows from the view (the underlying data is retained).

   :returns: ``None``.

.. py:method:: purge_table_data()
   :noindex:

   Erase all table and column data.

   :returns: ``None``.

.. py:method:: fill_empty_columns(fillvalue='')
   :noindex:

   Pad short rows so every row has a value in every column.

   :returns: ``None``.

Rows
~~~~

.. py:method:: insert_row(index='end', values=[], reload=True)
   :noindex:

   Insert a row at ``index`` (or ``"end"`` to append).

   :raises ValueError: if ``values`` is empty.
   :returns: the new row.
   :rtype: TableRow

.. py:method:: insert_rows(index, rowdata)
   :noindex:

   Insert each row of ``rowdata`` after ``index``.

   :returns: ``None``.

.. py:method:: delete_row(index=None, iid=None, visible=True)
   :noindex:

   Delete a single row by index or iid.

   :returns: ``None``.

.. py:method:: delete_rows(indices=None, iids=None, visible=True)
   :noindex:

   Delete multiple rows by index or iid (all rows if none given).

   :returns: ``None``.

.. py:method:: get_row(index=None, visible=False, filtered=False, iid=None)
   :noindex:

   Return one row by index or iid.

   :rtype: TableRow

.. py:method:: get_rows(visible=False, filtered=False, selected=False)
   :noindex:

   Return rows — all, or only the visible / filtered / selected subset.

   :rtype: list[TableRow]

.. py:method:: move_selected_row_up()
   :noindex:

   Move the selected rows up one position in the data set.

   :returns: ``None``.

.. py:method:: move_selected_row_down()
   :noindex:

   Move the selected rows down one position in the data set.

   :returns: ``None``.

.. py:method:: move_selected_rows_to_top()
   :noindex:

   Move the selected rows to the top of the data set.

   :returns: ``None``.

.. py:method:: move_selected_rows_to_bottom()
   :noindex:

   Move the selected rows to the bottom of the data set.

   :returns: ``None``.

.. py:method:: hide_selected_rows()
   :noindex:

   Hide the currently selected rows.

   :returns: ``None``.

Columns
~~~~~~~

.. py:method:: insert_column(index, text='', image='', command='', anchor='w', width=200, minwidth=20, stretch=False)
   :noindex:

   Insert a column at ``index``.

   :param anchor: cell alignment — one of ``"nw"``, ``"n"``, ``"ne"``, ``"w"``,
      ``"center"``, ``"e"``, ``"sw"``, ``"s"``, ``"se"``.
   :returns: the new column.
   :rtype: TableColumn

.. py:method:: delete_column(index=None, cid=None, visible=True)
   :noindex:

   Delete a single column by index or cid.

   :returns: ``None``.

.. py:method:: delete_columns(indices=None, cids=None, visible=True)
   :noindex:

   Delete multiple columns by index or cid (all columns if none given).

   :returns: ``None``.

.. py:method:: get_column(index=None, visible=False, cid=None)
   :noindex:

   Return one column by index or cid.

   :rtype: TableColumn

.. py:method:: move_column_left(cid=None)
   :noindex:

   Move a column one position to the left.

   :returns: ``None``.

.. py:method:: move_column_right(cid=None)
   :noindex:

   Move a column one position to the right.

   :returns: ``None``.

.. py:method:: move_column_to_first(cid=None)
   :noindex:

   Move a column to the leftmost position.

   :returns: ``None``.

.. py:method:: move_column_to_last(cid=None)
   :noindex:

   Move a column to the rightmost position.

   :returns: ``None``.

.. py:method:: hide_selected_column(cid=None)
   :noindex:

   Detach a column from the table (it can be restored with
   :py:meth:`show_selected_column`).

   :returns: ``None``.

.. py:method:: show_selected_column(cid=None)
   :noindex:

   Re-attach a previously hidden column.

   :returns: ``None``.

.. py:method:: align_column_left(cid=None)
   :noindex:

   Left-align a column's cell text. ``align_column_center`` and
   ``align_column_right`` are the other two.

   :returns: ``None``.

.. py:method:: align_heading_left(cid=None)
   :noindex:

   Left-align a column's heading text. ``align_heading_center`` and
   ``align_heading_right`` are the other two.

   :returns: ``None``.

.. py:method:: autoalign_columns()
   :noindex:

   Align every column by its data type — numbers right, everything else left.

   :returns: ``None``.

.. py:method:: autofit_columns()
   :noindex:

   Size every visible column to fit its content.

   :returns: ``None``.

Sorting
~~~~~~~

.. py:method:: sort_column_data(cid=None, sort=None)
   :noindex:

   Sort the rows by a column.

   :param sort: ``0`` / ``None`` to sort ascending, ``1`` to sort descending.
   :returns: ``None``.

.. py:method:: reset_column_sort()
   :noindex:

   Restore the rows to their original insertion order.

   :returns: ``None``.

Filtering and search
~~~~~~~~~~~~~~~~~~~~~

.. py:method:: search_table_data(criteria, *columns)
   :noindex:

   Show only rows matching ``criteria`` (case-insensitive), optionally limited to
   the given columns.

   :returns: ``None``.

.. py:method:: filter_column_to_value(cid=None, value=None)
   :noindex:

   Show only rows whose value in a column equals ``value``.

   :returns: ``None``.

.. py:method:: filter_to_selected_rows()
   :noindex:

   Show only the currently selected rows.

   :returns: ``None``.

.. py:method:: reset_row_filters()
   :noindex:

   Remove all row filters and unhide every row.

   :returns: ``None``.

.. py:method:: reset_column_filters()
   :noindex:

   Remove all column filters and unhide every column.

   :returns: ``None``.

.. py:method:: reset_table()
   :noindex:

   Remove every filter and column sort at once.

   :returns: ``None``.

Pagination
~~~~~~~~~~

.. py:method:: goto_first_page()
   :noindex:

   Show the first page of data. ``goto_last_page``, ``goto_next_page``, and
   ``goto_prev_page`` navigate the others.

   :returns: ``None``.

.. py:method:: goto_page()
   :noindex:

   Show the page entered in the page-number box.

   :returns: ``None``.

Export
~~~~~~

.. py:method:: export_all_records()
   :noindex:

   Export every record to a CSV file (opens a save dialog).
   ``export_current_page``, ``export_current_selection``, and
   ``export_records_in_filter`` export the matching subset instead.

   :returns: ``None``.

.. py:method:: save_data_to_csv(headers, records, delimiter=',')
   :noindex:

   Write ``headers`` and ``records`` to a chosen CSV file.

   :returns: ``None``.

Appearance
~~~~~~~~~~

.. py:method:: apply_table_stripes(stripecolor)
   :noindex:

   Stripe even-numbered rows with a ``(background, foreground)`` pair; either may
   be ``None``.

   :returns: ``None``.

Properties
~~~~~~~~~~

.. py:attribute:: tablecolumns
   :noindex:

   All columns, in order. ``tablecolumns_visible`` is the visible subset.

   :type: list[TableColumn]

.. py:attribute:: tablerows
   :noindex:

   All rows. ``tablerows_visible`` and ``tablerows_filtered`` are the visible and
   filtered subsets.

   :type: list[TableRow]

.. py:attribute:: cidmap
   :noindex:

   A mapping of cid to ``TableColumn``. ``iidmap`` maps iid to ``TableRow``.

   :type: dict

.. py:attribute:: is_filtered
   :noindex:

   Whether a filter is currently active.

   :type: bool

.. py:attribute:: pagesize
   :noindex:

   The number of records shown per page.

   :type: int

.. py:attribute:: searchcriteria
   :noindex:

   The current search string.

   :type: str

Shared capabilities
-------------------

``Tableview`` is a ``Frame`` subclass, so it also has the methods every widget
inherits — configuration, placement, event binding, lifecycle, focus, and
introspection. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Tableview catalog page </widgets/tableview>` — usage, screenshots, and
  examples.
- :doc:`Treeview </widgets/treeview>` — the native ttk tree/table widget it
  builds on.
