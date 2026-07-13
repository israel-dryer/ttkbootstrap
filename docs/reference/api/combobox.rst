Combobox
========

``Combobox`` is the native ttk drop-down list combined with an editable text
field (``ttk.Combobox``), themed by ttkbootstrap. For usage and examples, see
the :doc:`Combobox catalog page </widgets/combobox>`; this page is the
complete reference for its options, methods, and styling.

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
       :ref:`Styling options <combobox-styling>` for the available styles.
   * - ``textvariable``
     - ``Variable``
     - A ``StringVar`` bound to the field's contents.
   * - ``values``
     - ``list``
     - The list of choices shown in the drop-down.
   * - ``postcommand``
     - ``callable``
     - A callback run just before the drop-down list is posted.
   * - ``height``
     - ``int``
     - The maximum number of rows shown in the drop-down before it scrolls.
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

.. py:method:: current(newindex=None)
   :noindex:

   Return the index of the selected value in ``values``, or set it when
   ``newindex`` is given.

   :rtype: int

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

.. _combobox-styling:

Styling options
---------------

This section is for changing how the combobox *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``Combobox(style=...)``.

.. include:: /reference/api/_style/combobox.rst

Shared capabilities
-------------------

``Combobox`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Combobox catalog page </widgets/combobox>` — usage, screenshots, and
  examples.
- `Tk ttk::combobox manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_combobox.htm>`__
  — the canonical upstream reference (Tcl 8.6).
