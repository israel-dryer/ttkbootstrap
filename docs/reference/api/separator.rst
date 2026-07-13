Separator
=========

``Separator`` is the native ttk thin horizontal or vertical dividing line
(``ttk.Separator``), themed by ttkbootstrap. For usage and examples, see the
:doc:`Separator catalog page </widgets/separator>`; this page is the complete
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
       :ref:`Styling options <separator-styling>` for the available styles.
   * - ``orient``
     - ``str``
     - The layout direction: ``"horizontal"`` or ``"vertical"``.
   * - ``cursor``
     - ``str``
     - The mouse cursor over the separator (see :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the separator accepts keyboard focus during traversal.

.. _separator-styling:

Styling options
----------------

This section is for changing how the separator *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``Separator(style=...)``.

.. include:: /reference/api/_style/separator.rst

Shared capabilities
-------------------

``Separator`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Separator catalog page </widgets/separator>` — usage, screenshots, and
  examples.
- `Tk ttk::separator manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_separator.htm>`__
  — the canonical upstream reference (Tcl 8.6).
