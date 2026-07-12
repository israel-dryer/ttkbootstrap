Listbox
=======

``Listbox`` is tkinter's list of selectable text lines (``tk.Listbox``), themed
by ttkbootstrap. Lines are addressed by integer index (0-based) or the special
index ``"end"`` / ``"active"``. This page is the complete reference for its own
options and methods; the shared widget methods are under
:doc:`Capabilities </reference/capabilities/index>`.

.. note::

   Python's standard library doesn't document ``tk.Listbox`` in full. This
   reference is maintained by ttkbootstrap. The canonical upstream source is the
   `Tk listbox manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/listbox.htm>`__
   (Tcl 8.6).

Options
-------

.. rubric:: ttkbootstrap

.. list-table::
   :widths: 26 74

   * - ``autostyle``
     - **Constructor only.** ``True`` (default) paints the listbox with the
       active theme and repaints on a theme switch; ``False`` opts out.

.. rubric:: Content and selection

.. list-table::
   :widths: 26 74

   * - ``listvariable``
     - A ``StringVar`` holding the list items as a Tcl list — keeps the widget
       and the variable in sync.
   * - ``selectmode``
     - ``"browse"`` (single, default), ``"single"``, ``"multiple"``, or
       ``"extended"`` (click-drag / Shift / Ctrl ranges).
   * - ``selectbackground`` / ``selectforeground`` / ``selectborderwidth``
     - Appearance of selected lines.
   * - ``activestyle``
     - How the active line is marked: ``"underline"``, ``"dotbox"``, or
       ``"none"``.
   * - ``exportselection``
     - Whether the selection is exported to the X selection / clipboard.

.. rubric:: Text and size

.. list-table::
   :widths: 26 74

   * - ``font``
     - The font for the lines.
   * - ``foreground`` (``fg``) / ``background`` (``bg``)
     - Text and surface colors.
   * - ``disabledforeground``
     - Text color when the widget's ``state`` is ``"disabled"``.
   * - ``justify``
     - Line alignment: ``"left"``, ``"center"``, ``"right"``.
   * - ``width`` / ``height``
     - Requested size in **characters** and **lines** (``0`` fits the content).

.. rubric:: Border and behavior

.. list-table::
   :widths: 26 74

   * - ``borderwidth`` (``bd``) / ``relief``
     - 3-D border width and style.
   * - ``highlightthickness`` / ``highlightcolor`` / ``highlightbackground``
     - The focus highlight around the widget.
   * - ``state``
     - ``"normal"`` or ``"disabled"``.
   * - ``cursor`` / ``takefocus`` / ``setgrid``
     - Mouse cursor (see :doc:`Cursors </reference/cursors>`); focus
       participation; whether the window resizes in whole lines.
   * - ``xscrollcommand`` / ``yscrollcommand``
     - Callbacks connecting the listbox to scrollbars.

Methods
-------

Content
~~~~~~~

.. py:method:: insert(index, *elements)
   :noindex:

   Insert one or more lines before ``index``.

   :param index: the position, or ``"end"`` to append.
   :param elements: the strings to add.
   :returns: ``None``.

.. py:method:: delete(first, last=None)
   :noindex:

   Delete the lines from ``first`` through ``last`` (or a single line).

   :returns: ``None``.

.. py:method:: get(first, last=None)
   :noindex:

   Return the text of a line, or a tuple of lines over a range.

   :returns: one line's text, or a tuple for a range.
   :rtype: str | tuple[str, ...]

.. py:method:: size()
   :noindex:

   Return the number of lines.

   :rtype: int

Indices
~~~~~~~

.. py:method:: index(index)
   :noindex:

   Resolve an index expression to an integer line number.

   :rtype: int

.. py:method:: nearest(y)
   :noindex:

   Return the index of the visible line nearest a y pixel coordinate.

   :rtype: int

.. py:method:: see(index)
   :noindex:

   Scroll so the line at ``index`` is visible.

   :returns: ``None``.

.. py:method:: activate(index)
   :noindex:

   Make the line at ``index`` the active one (the keyboard-navigation cursor).

   :returns: ``None``.

Selection
~~~~~~~~~

.. py:method:: curselection()
   :noindex:

   Return the indices of the currently selected lines.

   :rtype: tuple[int, ...]

.. py:method:: selection_set(first, last=None)
   :noindex:

   Select a line, or a range of lines. Alias: ``select_set``.

   :returns: ``None``.

.. py:method:: selection_clear(first, last=None)
   :noindex:

   Deselect a line or range. Alias: ``select_clear``.

   :returns: ``None``.

.. py:method:: selection_includes(index)
   :noindex:

   Report whether the line at ``index`` is selected. Alias: ``select_includes``.

   :rtype: bool

.. py:method:: selection_anchor(index)
   :noindex:

   Set the selection anchor — the fixed end of a range selection. Alias:
   ``select_anchor``.

   :returns: ``None``.

Per-line appearance
~~~~~~~~~~~~~~~~~~~

.. py:method:: itemconfigure(index, **options)
   :noindex:

   Set (or query) the appearance of one line. Alias: ``itemconfig``.

   :param options: ``background``, ``foreground``, ``selectbackground``,
      ``selectforeground``.
   :returns: the option spec when queried with a single option name, else
      ``None``.

.. py:method:: itemcget(index, option)
   :noindex:

   Return one per-line option.

Scrolling
~~~~~~~~~

.. py:method:: yview(*args)
   :noindex:

   Query or set the vertical view; usually wired to a scrollbar via
   ``yscrollcommand``. ``xview`` is the horizontal counterpart, and both have
   ``*_moveto(fraction)`` and ``*_scroll(number, what)`` variants.

   :returns: with no args, the visible fraction ``(first, last)``; else ``None``.
   :rtype: tuple | None

.. py:method:: scan_mark(x, y)
   :noindex:

   Record a starting point for a fast drag-scroll.

   :returns: ``None``.

.. py:method:: scan_dragto(x, y)
   :noindex:

   Scroll the view relative to the ``scan_mark`` point.

   :returns: ``None``.

Shared capabilities
-------------------

``Listbox`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection. These are
documented under :doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- `Tk listbox manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/listbox.htm>`__
  — the canonical upstream reference (Tcl 8.6).
