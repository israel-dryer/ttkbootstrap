Sizegrip
========

``Sizegrip`` is the native ttk resize handle for the bottom-right corner of a
window (``ttk.Sizegrip``), themed by ttkbootstrap. This page is the
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
       :ref:`Styling options <sizegrip-styling>` for the available styles.
   * - ``cursor``
     - ``str``
     - The mouse cursor over the sizegrip (see :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the sizegrip accepts keyboard focus during traversal.

.. _sizegrip-styling:

Styling options
----------------

This section is for changing how the sizegrip *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``Sizegrip(style=...)``.

.. include:: /reference/api/_style/sizegrip.rst

Shared capabilities
-------------------

``Sizegrip`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Sizegrip catalog page </widgets/sizegrip>` — usage, screenshots, and
  examples.
- `Tk ttk::sizegrip manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_sizegrip.htm>`__
  — the canonical upstream reference (Tcl 8.6).
