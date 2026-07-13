Spinbox
=======

``Spinbox`` is the native ttk text field with up/down arrows for stepping
through numeric or listed values (``ttk.Spinbox``), themed by ttkbootstrap.
For usage and examples, see the :doc:`Spinbox catalog page </widgets/spinbox>`;
this page is the complete reference for its options, methods, and styling.

.. note::

   Python's standard library documents ``ttk.Spinbox`` only briefly. The
   canonical upstream source is the
   `Tk ttk::spinbox manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_spinbox.htm>`__
   (Tcl 8.6).

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
       :ref:`Styling options <spinbox-styling>` for the available styles.
   * - ``textvariable``
     - ``Variable``
     - A ``StringVar`` bound to the field's contents.
   * - ``from_``
     - ``float``
     - The minimum value in the numeric range.
   * - ``to``
     - ``float``
     - The maximum value in the numeric range.
   * - ``increment``
     - ``float``
     - The amount each arrow press steps the value.
   * - ``values``
     - ``list``
     - An explicit list of values to step through, instead of a numeric range.
   * - ``format``
     - ``str``
     - A printf-style format for the displayed value (e.g. ``"%.2f"``).
   * - ``wrap``
     - ``bool``
     - Whether stepping past either end wraps around to the other.
   * - ``command``
     - ``callable``
     - A callback run each time an arrow is pressed.
   * - ``show``
     - ``str``
     - A character to display instead of the real text (e.g. ``"*"`` for a
       password field).
   * - ``justify``
     - ``str``
     - Text alignment: ``"left"``, ``"center"``, or ``"right"``.
   * - ``font``
     - ``str | Font``
     - The font for the text.
   * - ``foreground``
     - ``str``
     - The text color.
   * - ``validate``
     - ``str``
     - When validation runs: ``"none"``, ``"focus"``, ``"focusin"``,
       ``"focusout"``, ``"key"``, or ``"all"``.
   * - ``validatecommand``
     - ``callable``
     - The callback that validates a proposed value; returns a boolean.
   * - ``invalidcommand``
     - ``callable``
     - The callback run when ``validatecommand`` returns false.
   * - ``state``
     - ``str``
     - ``"normal"``, ``"readonly"``, or ``"disabled"``.
   * - ``exportselection``
     - ``bool``
     - Whether the selection is exported to the clipboard/X selection.
   * - ``takefocus``
     - ``bool``
     - Whether the field accepts keyboard focus during traversal.
   * - ``width``
     - ``int``
     - The requested width in characters.
   * - ``xscrollcommand``
     - ``callable``
     - A callback connecting the field to a horizontal scrollbar.

Methods
-------

.. py:method:: set(value)
   :noindex:

   Set the field's contents to ``value``.

   :returns: ``None``.

.. py:method:: get()
   :noindex:

   Return the current text.

   :rtype: str

.. py:method:: insert(index, string)
   :noindex:

   Insert ``string`` before the character at ``index`` (``"end"`` appends).

   :returns: ``None``.

.. py:method:: delete(first, last=None)
   :noindex:

   Delete the characters from ``first`` through ``last`` (or a single one).

   :returns: ``None``.

.. py:method:: index(index)
   :noindex:

   Resolve an index expression (``"insert"``, ``"end"``, …) to an integer.

   :rtype: int

.. py:method:: icursor(index)
   :noindex:

   Move the insert cursor to ``index``.

   :returns: ``None``.

.. py:method:: selection_range(start, end)
   :noindex:

   Select the characters from ``start`` to ``end``. Aliased as
   ``select_range``; the ``selection_*`` / ``select_*`` family also has
   ``clear``, ``present``, ``adjust``, ``from``, and ``to``.

   :returns: ``None``.

.. py:method:: xview(*args)
   :noindex:

   Query or set the horizontal view; usually wired to a scrollbar. Has
   ``xview_moveto(fraction)`` and ``xview_scroll(number, what)`` variants.

.. _spinbox-styling:

Styling options
---------------

This section is for changing how the spinbox *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``Spinbox(style=...)``.

.. include:: /reference/api/_style/spinbox.rst

Shared capabilities
-------------------

``Spinbox`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Spinbox catalog page </widgets/spinbox>` — usage, screenshots, and
  examples.
- `Tk ttk::spinbox manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_spinbox.htm>`__
  — the canonical upstream reference (Tcl 8.6).
