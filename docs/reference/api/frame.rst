Frame
=====

``Frame`` is the native ttk rectangular container for grouping and laying out
other widgets (``ttk.Frame``), themed by ttkbootstrap. For usage and examples,
see the :doc:`Frame catalog page </widgets/frame>`; this page is the complete
reference for its options, methods, and styling.

.. note::

   Python's standard library documents ``ttk.Frame`` only briefly. The
   canonical upstream source is the
   `Tk ttk::frame manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_frame.htm>`__
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
       :ref:`Styling options <frame-styling>` for the available styles.
   * - ``padding``
     - ``int | tuple``
     - Extra space inside the frame's border, in pixels (a single value, or
       per-side).
   * - ``borderwidth``
     - ``int``
     - The width of the frame's border, in pixels.
   * - ``relief``
     - ``str``
     - The border decoration: ``"flat"``, ``"raised"``, ``"sunken"``,
       ``"solid"``, ``"ridge"``, or ``"groove"``.
   * - ``width``
     - ``int``
     - The requested width in pixels. Ignored unless geometry propagation is
       turned off.
   * - ``height``
     - ``int``
     - The requested height in pixels. Ignored unless geometry propagation is
       turned off.
   * - ``cursor``
     - ``str``
     - The mouse cursor over the frame (see :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the frame accepts keyboard focus during traversal.

.. _frame-styling:

Styling options
---------------

This section is for changing how the frame *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``Frame(style=...)``.

.. include:: /reference/api/_style/frame.rst

Shared capabilities
-------------------

``Frame`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Frame catalog page </widgets/frame>` — usage, screenshots, and
  examples.
- `Tk ttk::frame manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_frame.htm>`__
  — the canonical upstream reference (Tcl 8.6).
