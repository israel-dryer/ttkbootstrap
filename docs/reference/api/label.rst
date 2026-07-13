Label
=====

``Label`` is the native ttk widget that displays a line or block of
read-only text, an image, or both (``ttk.Label``), themed by ttkbootstrap.
This page is the complete reference for its options, methods, and styling.

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
       :ref:`Styling options <label-styling>` for the available styles.
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
     - The text shown on the label.
   * - ``textvariable``
     - ``Variable``
     - A ``StringVar`` whose value is shown as the text and tracked live.
   * - ``image``
     - ``PhotoImage``
     - An image to display in place of, or beside, the text.
   * - ``compound``
     - ``str``
     - How text and image are combined: ``"none"``, ``"left"``, ``"right"``,
       ``"top"``, ``"bottom"``, or ``"center"``.
   * - ``font``
     - ``str | Font``
     - The font for the text.
   * - ``foreground``
     - ``str``
     - The text color.
   * - ``background``
     - ``str``
     - The label's background color.
   * - ``anchor``
     - ``str``
     - How content is positioned in extra space, e.g. ``"center"``, ``"w"``,
       ``"e"``.
   * - ``justify``
     - ``str``
     - Alignment for multi-line text: ``"left"``, ``"center"``, or ``"right"``.
   * - ``wraplength``
     - ``int``
     - The width, in pixels, at which text wraps to a new line.
   * - ``underline``
     - ``int``
     - The character index to underline (for a keyboard mnemonic), or ``-1``.
   * - ``width``
     - ``int``
     - The requested width in characters (negative sets a minimum).
   * - ``padding``
     - ``int | tuple``
     - Extra space around the content, in pixels (a single value, or per-side).
   * - ``relief``
     - ``str``
     - The border style, e.g. ``"flat"``, ``"raised"``, ``"sunken"``, ``"groove"``,
       ``"ridge"``.
   * - ``borderwidth``
     - ``int``
     - The width of the border, in pixels.
   * - ``state``
     - ``str``
     - ``"normal"`` or ``"disabled"``.
   * - ``cursor``
     - ``str``
     - The mouse cursor over the label (see :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the label accepts keyboard focus during traversal.

.. _label-styling:

Styling options
---------------

This section is for changing how the label *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``Label(style=...)``.

.. include:: /reference/api/_style/label.rst

Shared capabilities
-------------------

``Label`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Label catalog page </widgets/label>` — usage, screenshots, and
  examples.
- `Tk ttk::label manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_label.htm>`__
  — the canonical upstream reference (Tcl 8.6).
