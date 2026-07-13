Scale
=====

``Scale`` is the native ttk slider for choosing a numeric value from a range
(``ttk.Scale``), themed by ttkbootstrap. This page is the complete
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
       :ref:`Styling options <scale-styling>` for the available styles.
   * - ``from_``
     - ``float``
     - The value at one end of the scale's range.
   * - ``to``
     - ``float``
     - The value at the other end of the scale's range.
   * - ``value``
     - ``float``
     - The current value.
   * - ``variable``
     - ``Variable``
     - A ``DoubleVar`` (or ``IntVar``) bound to the current value.
   * - ``orient``
     - ``str``
     - The layout direction: ``"horizontal"`` or ``"vertical"``.
   * - ``length``
     - ``int``
     - The slider's length in pixels.
   * - ``command``
     - ``callable``
     - Called with the new value (as a string) whenever the slider moves.
   * - ``state``
     - ``str``
     - ``"normal"`` or ``"disabled"``.
   * - ``cursor``
     - ``str``
     - The mouse cursor over the scale (see :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the scale accepts keyboard focus during traversal.

Methods
-------

.. py:method:: get(x=None, y=None)
   :noindex:

   Return the current value, or the value at a pixel coordinate.

   :rtype: float

.. py:method:: set(value)
   :noindex:

   Set the value.

   :returns: ``None``.

.. py:method:: coords(value=None)
   :noindex:

   Return the pixel coordinates of the slider for ``value`` (default: the
   current value).

   :rtype: tuple

.. _scale-styling:

Styling options
---------------

This section is for changing how the scale *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``Scale(style=...)``.

.. include:: /reference/api/_style/scale.rst

Shared capabilities
-------------------

``Scale`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Scale catalog page </widgets/scale>` — usage, screenshots, and examples.
- `Tk ttk::scale manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_scale.htm>`__
  — the canonical upstream reference (Tcl 8.6).
