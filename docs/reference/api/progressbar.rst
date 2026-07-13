Progressbar
===========

``Progressbar`` is the native ttk horizontal or vertical bar that shows
progress (``ttk.Progressbar``), themed by ttkbootstrap. This page is the
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
       :ref:`Styling options <progressbar-styling>` for the available styles.
   * - ``orient``
     - ``str``
     - The layout direction: ``"horizontal"`` or ``"vertical"``.
   * - ``length``
     - ``int``
     - The requested size along the long axis, in pixels.
   * - ``mode``
     - ``str``
     - ``"determinate"`` (tracks ``value``) or ``"indeterminate"`` (animates
       back and forth).
   * - ``maximum``
     - ``float``
     - The value at which the bar is full.
   * - ``value``
     - ``float``
     - The current progress amount.
   * - ``variable``
     - ``Variable``
     - A ``DoubleVar``/``IntVar`` bound to ``value``.
   * - ``phase``
     - ``int``
     - Read-only animation phase, useful for driving custom indeterminate styles.
   * - ``cursor``
     - ``str``
     - The mouse cursor over the progress bar (see
       :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the progress bar accepts keyboard focus during traversal.

Methods
-------

.. py:method:: start(interval=None)
   :noindex:

   Begin auto-advancing (indeterminate mode) or animating; ``interval`` is
   the number of milliseconds between steps.

   :returns: ``None``.

.. py:method:: step(amount=None)
   :noindex:

   Increase ``value`` by ``amount`` (default ``1.0``), wrapping at ``maximum``.

   :returns: ``None``.

.. py:method:: stop()
   :noindex:

   Stop the animation started by ``start``.

   :returns: ``None``.

.. _progressbar-styling:

Styling options
---------------

This section is for changing how the progress bar *looks*. Define a style
with ``style.configure(...)`` (and ``style.map(...)`` for per-state colors),
then apply it with ``Progressbar(style=...)``.

.. include:: /reference/api/_style/progressbar.rst

Shared capabilities
-------------------

``Progressbar`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Progressbar catalog page </widgets/progressbar>` — usage,
  screenshots, and examples.
- `Tk ttk::progressbar manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_progressbar.htm>`__
  — the canonical upstream reference (Tcl 8.6).
