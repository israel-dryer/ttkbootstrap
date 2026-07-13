Scrollbar
=========

``Scrollbar`` is the native ttk scrollbar that drives another widget's view
(``ttk.Scrollbar``), themed by ttkbootstrap. This page is the complete
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
       :ref:`Styling options <scrollbar-styling>` for the available styles.
   * - ``orient``
     - ``str``
     - The layout direction: ``"horizontal"`` or ``"vertical"``.
   * - ``command``
     - ``callable``
     - The scrolled widget's ``xview``/``yview`` method, called when the user
       drags the thumb or clicks the trough/arrows.
   * - ``cursor``
     - ``str``
     - The mouse cursor over the scrollbar (see :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the scrollbar accepts keyboard focus during traversal.

Methods
-------

.. py:method:: set(first, last)
   :noindex:

   Set the thumb to span the fractions ``first``..``last``; wired as the
   scrolled widget's ``xscrollcommand``/``yscrollcommand``.

   :returns: ``None``.

.. py:method:: get()
   :noindex:

   Return the current ``(first, last)`` fractions.

   :rtype: tuple

.. py:method:: delta(deltax, deltay)
   :noindex:

   Return the fractional change a pixel movement of ``(deltax, deltay)``
   would cause.

   :rtype: float

.. py:method:: fraction(x, y)
   :noindex:

   Return the fraction (0..1) corresponding to a pixel coordinate.

   :rtype: float

.. _scrollbar-styling:

Styling options
----------------

This section is for changing how the scrollbar *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``Scrollbar(style=...)``.

.. include:: /reference/api/_style/scrollbar.rst

Shared capabilities
-------------------

``Scrollbar`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Scrollbar catalog page </widgets/scrollbar>` — usage, screenshots, and
  examples.
- `Tk ttk::scrollbar manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_scrollbar.htm>`__
  — the canonical upstream reference (Tcl 8.6).
