Radiobutton
===========

``Radiobutton`` is the native ttk one-of-many selector that shares a variable
with its siblings (``ttk.Radiobutton``), themed by ttkbootstrap. This page is
the complete reference for its options, methods, and styling.

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
       :ref:`Styling options <radiobutton-styling>` for the available styles.
   * - ``icon``
     - ``str``
     - **Constructor keyword.** A Bootstrap Icons glyph name (e.g.
       ``"gear-fill"``) shown on the widget; theme-aware — it follows the
       foreground color and states. See the
       :doc:`Icons guide </user-guide/feature-guides/icons>`.
   * - ``icon_size``
     - ``int``
     - **Constructor keyword.** The glyph size in pixels (scaled for high-DPI).
   * - ``icon_only``
     - ``bool``
     - **Constructor keyword.** Show only the glyph (hide the text) and pad the
       widget into a square. Default ``False``.
   * - ``text``
     - ``str``
     - The label shown beside the button.
   * - ``textvariable``
     - ``Variable``
     - A ``StringVar`` whose value is shown as the label and tracked live.
   * - ``variable``
     - ``Variable``
     - The variable shared by all radiobuttons in the group.
   * - ``value``
     - ``any``
     - The value written to ``variable`` when this button is selected.
   * - ``command``
     - ``callable``
     - The function called when this button is selected.
   * - ``image``
     - ``PhotoImage``
     - An image to display in place of, or beside, the text.
   * - ``compound``
     - ``str``
     - How text and image are combined: ``"none"``, ``"left"``, ``"right"``,
       ``"top"``, ``"bottom"``, or ``"center"``.
   * - ``underline``
     - ``int``
     - The character index to underline (for a keyboard mnemonic), or ``-1``.
   * - ``width``
     - ``int``
     - The requested width in characters (negative sets a minimum).
   * - ``padding``
     - ``int | tuple``
     - Extra space around the label, in pixels (a single value, or per-side).
   * - ``state``
     - ``str``
     - ``"normal"`` or ``"disabled"``. For finer control use the ``state`` method
       (see :doc:`Capabilities </reference/capabilities/index>`).

Methods
-------

.. py:method:: invoke()
   :noindex:

   Select this button (write its ``value`` into ``variable``) and run its
   ``command``.

   :returns: the command's return value.

.. _radiobutton-styling:

Styling options
---------------

This section is for changing how the radiobutton *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``Radiobutton(style=...)``.

.. include:: /reference/api/_style/radiobutton.rst

Shared capabilities
-------------------

``Radiobutton`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Radiobutton catalog page </widgets/radiobutton>` — usage, screenshots,
  and examples.
- `Tk ttk::radiobutton manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_radiobutton.htm>`__
  — the canonical upstream reference (Tcl 8.6).
