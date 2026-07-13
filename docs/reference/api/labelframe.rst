Labelframe
==========

``Labelframe`` is the native ttk :doc:`frame </reference/api/frame>` with a
caption drawn into its border (``ttk.Labelframe``), themed by ttkbootstrap. This page is the complete reference for its options, methods, and styling. Mind
the capitalization: ``ttk.Labelframe`` (lowercase **f**) is this themed ttk
widget, while ``ttk.LabelFrame`` (capital **F**) is the classic
:doc:`tk widget </reference/api/tklabelframe>`.

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
       :ref:`Styling options <labelframe-styling>` for the available styles.
   * - ``text``
     - ``str``
     - The caption drawn into the border.
   * - ``labelwidget``
     - ``Widget``
     - A widget to use as the label in place of ``text``.
   * - ``labelanchor``
     - ``str``
     - Where the caption sits on the border: ``"nw"``, ``"n"``, ``"ne"``,
       ``"en"``, ``"e"``, and so on.
   * - ``underline``
     - ``int``
     - The character index in ``text`` to underline (for a mnemonic), or ``-1``.
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

.. _labelframe-styling:

Styling options
---------------

This section is for changing how the labelframe *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``Labelframe(style=...)``.

.. include:: /reference/api/_style/labelframe.rst

Shared capabilities
-------------------

``Labelframe`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Labelframe catalog page </widgets/labelframe>` — usage, screenshots, and
  examples.
- :doc:`LabelFrame </reference/api/tklabelframe>` — the classic ``tk.LabelFrame``.
- `Tk ttk::labelframe manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_labelframe.htm>`__
  — the canonical upstream reference (Tcl 8.6).
